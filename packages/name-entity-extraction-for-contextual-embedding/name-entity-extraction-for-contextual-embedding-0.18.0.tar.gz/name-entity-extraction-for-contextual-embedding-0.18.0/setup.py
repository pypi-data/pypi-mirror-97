from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

print(find_packages())
setup(
    name='name-entity-extraction-for-contextual-embedding',
    packages=find_packages(),
    version='0.18.0',
    description='a machine learning project for mlm task for contextual embedding',
    author='Simon Meoni',
    license='MIT',
    install_requires=requirements,
    entry_points='''
    [console_scripts]
    camembert_ner_ft=src.models.camembert_ner_ft:main
    make_dataset=src.data.make_dataset:main
    ''',
    package_data={
        "src": [
            "resources/log_config.ini",
        ]},
)
