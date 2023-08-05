import gc
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
from torch.utils.data import DataLoader
from tqdm import tqdm

from src.data.camembert_ner_dataset import CamemBertNerDataset
from src.models.classifiers import classifier_factory
from src.models.utils import init_tokenizer, save_model, monitor_output_example, \
    monitor_model_eval, init_model, logger, log_classification_report


# pylint: disable=too-many-arguments, too-many-locals
def compute_loss(predictions, targets, criterion=None):
    rearranged_output = predictions.contiguous().view(
        predictions.shape[0] * predictions.shape[1], -1)
    rearranged_target = targets.contiguous().view(-1)
    loss = criterion(rearranged_output, rearranged_target)
    return loss


def train_model(model, classifier, dataloader, optimizer, criterion, device, id_fold, epochs):
    model.train()
    classifier.train()
    epoch_loss = []
    logger.info('🎓 model training step is started')
    for epoch in tqdm(range(epochs), position=0, leave=False, desc='epoch'):
        logger.info("Starting epoch {}".format(epoch + 1))
        for batch in tqdm(dataloader, position=1, leave=False, desc='learning batch'):
            optimizer.zero_grad()

            predictions = classifier(
                model(input_ids=batch['tokens'].to(device),
                      attention_mask=batch['attention_mask'].to(device)).last_hidden_state
            )
            predictions_scores = f.log_softmax(predictions, dim=2)
            loss = compute_loss(predictions_scores, batch['target'].to(device), criterion)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            wandb.log({"loss {}".format(id_fold): loss.item()})
            epoch_loss.append(loss.item())

    logger.info('train epoch loss : {}'.format(mean(epoch_loss)))
    logger.info('🎓 model training step is finished')


def eval_model(model, classifier, dataloader, criterion, device, labels):
    model.eval()
    classifier.eval()
    epoch_loss = []
    evaluation_measure = {
        'recall': [],
        'precision': [],
        'F1 score': [],
        'pred_labels': [],
        'true_labels': [],
    }
    logger.info('model evaluation step is started')
    with torch.no_grad():
        batch = None
        for batch in dataloader:
            predictions = classifier(
                model(input_ids=batch['tokens'].to(device),
                      attention_mask=batch['attention_mask'].to(device)).last_hidden_state
            )
            predictions_scores = f.log_softmax(predictions, dim=2)
            loss = compute_loss(predictions_scores, batch['target'].to(device), criterion)
            epoch_loss.append(loss.item())
            precision, recall, f1_score = monitor_model_eval(predictions_scores, batch)
            evaluation_measure['recall'].append(recall)
            evaluation_measure['precision'].append(precision)
            evaluation_measure['F1 score'].append(f1_score)
            evaluation_measure['true_labels'].append(batch['target'])
            evaluation_measure['pred_labels'].append(predictions_scores)
    if batch is not None:
        monitor_output_example(batch, dataloader, labels, predictions_scores)
    log_classification_report(evaluation_measure['true_labels'],
                              evaluation_measure['pred_labels'], labels)
    logger.info('model evaluation step is finished')
    return mean(epoch_loss), mean(evaluation_measure['recall']), \
           mean(evaluation_measure['precision']), mean(evaluation_measure['F1 score'])


@click.command()
@click.option('--learning-rate', required=True)
@click.option('--batch-size', required=True)
@click.option('--num-epochs', required=True)
@click.option('--folds', required=True)
@click.option('--model-name', required=True)
@click.option('--model-path', required=True)
@click.option('--dataset-path', required=True)
def main(learning_rate,
         batch_size,
         num_epochs,
         folds,
         model_name,
         model_path,
         dataset_path):
    hyperparameter_defaults = dict(
        lr=float(learning_rate),
        batch_size=int(batch_size),
        num_epochs=int(num_epochs),
        folds=int(folds),
        model_name=model_name,
        model_path=model_path,
    )
    wandb.init(project="360-ner-task", config=hyperparameter_defaults)
    device = torch.device('cpu' if torch.cuda.is_available() else 'cpu')
    dataset = sorted(glob.glob(dataset_path + '/*.pickle'), key=os.path.getsize)
    metadata = json.load(open(glob.glob(dataset_path + '/*.json')[0], 'r'))
    labels = metadata['labels']
    num_labels = len(labels)
    logger.info("Using device: {}".format(device))
    logger.info("Using tokenizer from model : {}".format(model_name))
    tokenizer = init_tokenizer(hyperparameter_defaults['model_name'])
    criterion = nn.NLLLoss(weight=torch.Tensor([metadata['labels weights'][label]
                                                for label in labels]))
    folds = KFold(n_splits=hyperparameter_defaults['folds'], shuffle=False)
    for id_fold, fold in enumerate(folds.split(dataset)):
        logger.info('beginning fold n°{}'.format(id_fold + 1))
        model = init_model(hyperparameter_defaults['model_name'], device)
        classifier = classifier_factory('linear', device, **{'zn_size': model.config.hidden_size,
                                                             'num_labels': num_labels})
        logger.info(f'using the following classifier configuration : {classifier}')
        parameters = list(model.parameters()) + list(classifier.parameters())
        optimizer = optim.Adam(parameters, lr=hyperparameter_defaults['lr'])
        eval_dataloader, train_dataloader = create_dataloader(dataset, fold,
                                                              hyperparameter_defaults, tokenizer)
        wandb.watch(model)
        train_model(model, classifier, train_dataloader, optimizer, criterion, device, id_fold,
                    hyperparameter_defaults['num_epochs'])
        save_model(classifier, hyperparameter_defaults, id_fold, model, model_name)
        cv_loss, recall, precision, f1_score = eval_model(model, classifier,
                                                          eval_dataloader, criterion,
                                                          device, labels)
        # delete model to empty some space memory
        del model
        gc.collect()
        torch.cuda.empty_cache()

        # Monitor current fold
        wandb.log({"CV loss": cv_loss})
        wandb.log({"CV recall": recall})
        wandb.log({"CV precision": precision})
        wandb.log({"CV F1 score": f1_score})
        logger.info('🔎 evaluation is finished, here is the different metrics :')
        logger.info(f'cv recall : {recall}')
        logger.info(f'cv precision: {precision}')
        logger.info(f'cv F1 score: {f1_score}')
        logger.info(f'cv loss: {cv_loss}')


def create_dataloader(dataset, fold, hyperparameter_defaults, tokenizer):
    train_fold, eval_fold = fold
    train_fold = [dataset[file_index] for file_index in train_fold]
    eval_fold = [dataset[file_index] for file_index in eval_fold]
    train_dataset = CamemBertNerDataset(train_fold, tokenizer)
    eval_dataset = CamemBertNerDataset(eval_fold, tokenizer)
    train_dataloader = DataLoader(dataset=train_dataset,
                                  batch_size=hyperparameter_defaults["batch_size"],
                                  shuffle=False, drop_last=True,
                                  collate_fn=train_dataset.masked_lm_collate)
    eval_dataloader = DataLoader(dataset=eval_dataset,
                                 batch_size=hyperparameter_defaults["batch_size"],
                                 shuffle=False, drop_last=True,
                                 collate_fn=eval_dataset.masked_lm_collate)
    return eval_dataloader, train_dataloader


if __name__ == '__main__':
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    # pylint: disable=no-value-for-parameter
    main()
