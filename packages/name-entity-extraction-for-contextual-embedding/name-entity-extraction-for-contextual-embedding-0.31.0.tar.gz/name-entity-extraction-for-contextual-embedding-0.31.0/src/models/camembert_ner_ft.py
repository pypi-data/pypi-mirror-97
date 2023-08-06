import glob
import json
import os
from pathlib import Path

import click
import torch
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim
import wandb
from dotenv import find_dotenv, load_dotenv
from numpy import mean
from sklearn.model_selection import KFold
from torch.nn import NLLLoss
from src.models.classifiers import classifier_factory
from src.models.utils import (
    init_tokenizer,
    save_model,
    monitor_output_example,
    monitor_model_eval,
    init_model,
    logger,
    log_classification_report,
    create_dataloader,
    empty_gpu,
)


# pylint: disable=too-many-arguments, too-many-locals


@click.command()
@click.option("--learning-rate", required=True)
@click.option("--classifier-name", required=True)
@click.option("--batch-size", required=True)
@click.option("--num-epochs", required=True)
@click.option("--folds", required=True)
@click.option("--model-name", required=True)
@click.option("--model-path", required=True)
@click.option("--dataset-path", required=True)
def main(
    learning_rate: float,
    batch_size: int,
    num_epochs: int,
    folds: int,
    model_name: str,
    model_path: str,
    dataset_path: str,
    classifier_name: str,
):
    """
    Args:
        classifier_name:
        learning_rate: the model's learning rate
        batch_size: size of the mini-batch
        num_epochs: epoch's number during training
        folds: we use K-fold to evaluate the model, insert the number of folds here
        model_name: the huggingface model name
        model_path: the saving path for the trained model, we record k model, k is a number of folds
        dataset_path: the path of the dataset
    """
    hyperparameter_defaults = dict(
        lr=float(learning_rate),
        batch_size=int(batch_size),
        num_epochs=int(num_epochs),
        folds=int(folds),
        model_name=model_name,
        model_path=model_path,
    )
    # monitor the model with wandb
    wandb.init(config=hyperparameter_defaults)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dataset = sorted(glob.glob(dataset_path + "/*.pickle"), key=os.path.getsize)
    metadata = json.load(open(glob.glob(dataset_path + "/*.json")[0], "r"))
    labels = metadata["labels"]
    num_labels = len(labels)
    logger.info("Using device: {}".format(device))
    logger.info("Using tokenizer from model : {}".format(model_name))
    tokenizer = init_tokenizer(hyperparameter_defaults["model_name"])
    criterion = nn.NLLLoss(
        weight=torch.Tensor([metadata["labels weights"][label] for label in labels]).to(
            device
        )
    )
    folds = KFold(n_splits=hyperparameter_defaults["folds"], shuffle=False)
    for id_fold, fold in enumerate(folds.split(dataset)):
        # for each fold with we iterate a training loop and a evaluation loop
        # we iterate a different evaluation and training batches, we compute the CV loss to
        # check the integrity of the corpus. We use small corpora to fine-tuning the model
        # with a small masking task to downstream to another task (NER, QA ...)
        # to a specialized domain.

        logger.info("beginning fold n°{}".format(id_fold + 1))
        model = init_model(hyperparameter_defaults["model_name"], device)
        classifier = classifier_factory(
            classifier_name,
            device,
            **{"zn_size": model.config.hidden_size, "num_labels": num_labels},
        )
        logger.info(f"using the following classifier configuration : {classifier}")
        parameters = list(model.parameters()) + list(classifier.parameters())
        optimizer = optim.Adam(parameters, lr=hyperparameter_defaults["lr"])
        eval_dataloader, train_dataloader = create_dataloader(
            dataset, fold, hyperparameter_defaults, tokenizer
        )
        wandb.watch(model)
        train_model(
            model,
            classifier,
            train_dataloader,
            optimizer,
            criterion,
            device,
            id_fold,
            hyperparameter_defaults["num_epochs"],
        )
        save_model(classifier, hyperparameter_defaults, id_fold, model, model_name)
        cv_loss, recall, precision, f1_score = eval_model(
            model, classifier, eval_dataloader, criterion, device, labels
        )
        # delete model to empty some space memory
        empty_gpu(model)

        # Monitor current fold
        wandb.log({"CV loss": cv_loss})
        wandb.log({"CV recall": recall})
        wandb.log({"CV precision": precision})
        wandb.log({"CV F1 score": f1_score})
        logger.info("🔎 evaluation is finished, here is the different metrics :")
        logger.info(f"cv recall : {recall}")
        logger.info(f"cv precision: {precision}")
        logger.info(f"cv F1 score: {f1_score}")
        logger.info(f"cv loss: {cv_loss}")


def compute_loss(
    predictions: torch.Tensor, targets: torch.Tensor, criterion: NLLLoss
) -> torch.Tensor:
    """
    this method is used to compute the loss of the model with the predicted tensor and
    the target tensor. We apply other operation to arrange tensor in order to select only
    the last hidden states of our model.
    Args:
        predictions: the predicted model vector
        targets: the targeted vector, it is a vector with just the masked tokens
        criterion: the loss function

    Returns:
        the loss score
    """
    rearranged_output = predictions.contiguous().view(
        predictions.shape[0] * predictions.shape[1], -1
    )
    rearranged_target = targets.contiguous().view(-1)
    loss = criterion(rearranged_output, rearranged_target)
    return loss


def train_model(
    model, classifier, dataloader, optimizer, criterion, device, id_fold, epochs
):
    """
    the model training loop
    Args:
        classifier:
        model: the transformer model
        dataloader: the pytorch dataloader
        optimizer: the pytorch optimizer
        criterion: the pytorch loss function
        device: the pytorch device
        id_fold: the fold id process in the main loop
        epochs: the number of epochs
    """
    model.train()
    classifier.train()
    epoch_loss = []
    logger.info("🎓 model training step is started")
    for epoch in range(epochs):
        logger.info(f"processing epochs {epoch + 1}/{epochs}")
        for batch in dataloader:
            optimizer.zero_grad()
            predictions = classifier(
                model(
                    input_ids=batch["tokens"].to(device),
                    attention_mask=batch["attention_mask"].to(device),
                ).last_hidden_state
            )
            predictions_scores = f.log_softmax(predictions, dim=2)
            loss = compute_loss(
                predictions_scores, batch["target"].to(device), criterion
            )
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            wandb.log({"loss {}".format(id_fold): loss.item()})
            epoch_loss.append(loss.item())
    logger.info("train epoch loss : {}".format(mean(epoch_loss)))
    logger.info("🎓 model training step is finished")


def eval_model(model, classifier, dataloader, criterion, device, labels):
    """
    the model evaluation loop
    Args:
        model: the transformer model
        dataloader: the pytorch dataloader
        criterion: the pytorch loss function
        device: the pytorch device
        classifier:
        labels:
    Returns:
        the mean epoch loss using to compute the CV score
    """
    model.eval()
    classifier.eval()
    epoch_loss = []
    evaluation_measure = {
        "recall": [],
        "precision": [],
        "F1 score": [],
        "pred_labels": [],
        "true_labels": [],
    }
    logger.info("model evaluation step is started")
    with torch.no_grad():
        batch = None
        for batch in dataloader:
            predictions = classifier(
                model(
                    input_ids=batch["tokens"].to(device),
                    attention_mask=batch["attention_mask"].to(device),
                ).last_hidden_state
            )
            predictions_scores = f.log_softmax(predictions, dim=2)
            loss = compute_loss(
                predictions_scores, batch["target"].to(device), criterion
            )
            epoch_loss.append(loss.item())
            precision, recall, f1_score = monitor_model_eval(
                predictions_scores.to("cpu"), batch
            )
            evaluation_measure["recall"].append(recall)
            evaluation_measure["precision"].append(precision)
            evaluation_measure["F1 score"].append(f1_score)
            evaluation_measure["true_labels"].append(batch["target"])
            evaluation_measure["pred_labels"].append(predictions_scores.to("cpu"))
    if batch is not None:
        monitor_output_example(batch, dataloader, labels, predictions_scores)
    log_classification_report(
        evaluation_measure["true_labels"], evaluation_measure["pred_labels"], labels
    )
    logger.info("model evaluation step is finished")
    return (
        mean(epoch_loss),
        mean(evaluation_measure["recall"]),
        mean(evaluation_measure["precision"]),
        mean(evaluation_measure["F1 score"]),
    )


if __name__ == "__main__":
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    # pylint: disable=no-value-for-parameter
    main()
