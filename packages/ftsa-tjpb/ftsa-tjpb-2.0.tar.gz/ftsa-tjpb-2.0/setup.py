from setuptools import setup, find_packages
from ftsa.cli.modules.properties import VERSION, PACKAGE_NAME

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author='Carlos Diego Quirino Lima',
    author_email='diegoquirino@gmail.com',
    description='Framework de Teste de Sistemas Automatizado',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://gitlab.tjpb.jus.br/testes/ftsa-tjpb.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords='ftsa framework teste sistemas automatizado tjpb',
    packages=find_packages(exclude=['tests*']),
    package_data={'ftsa': [
        'config/*.properties',
        'cli/projects/**/*',
        'cli/projects/example_project/**/*',
        'cli/projects/example_project/data/**/*',
        'cli/projects/example_project/features/**/*',
        'cli/projects/base_project/**/*',
        'cli/projects/base_project/data/**/*',
        'cli/projects/base_project/features/**/*',
        'cli/projects/services_project/**/*',
        'cli/projects/services_project/data/**/*',
        'cli/projects/services_project/features/**/*',
        'cli/projects/commons/**/*',
        'cli/projects/commons/.gitignore',
        'cli/projects/services_project/**/*'
    ]},
    install_requires=[],
    entry_points={'console_scripts': [
        'ftsa = ftsa.cli.main:main'
    ]},
    platforms='windows linux',
)
