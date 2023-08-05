import os
import sys
import shutil
import unicodedata
from enum import Enum
from configparser import ConfigParser
from ftsa.cli.exceptions import NotFTSAProjectException


""" Diretórios da aplicação """
DIR_DATA = 'data'
DIR_IMAGES = f'{DIR_DATA}{os.sep}img'
DIR_FEATURES = 'features'
DIR_PAGE_OBJECTS = 'page_objects'
DIR_RESOURCES = 'resources'
DIR_COMMONS = 'commons'
FILE_PROJECT_PROPERTIES = 'project.properties'
FILE_GITIGNORE = '.gitignore'
FILE_MAIN_PY = 'main.py'
FILE_DOCKER_COMPOSE = 'docker-compose.yml'
FILE_DOCKERFILE = 'Dockerfile'
OS_LIB_BASE_DIR = f'Lib{os.sep}site-packages{os.sep}ftsa{os.sep}cli{os.sep}projects{os.sep}'
DIR_LIB_BASE_PROJECT = f'{OS_LIB_BASE_DIR}base_project'
DIR_LIB_SERVICE_PROJECT = f'{OS_LIB_BASE_DIR}services_project'
DIR_LIB_EXAMPLE_PROJECT = f'{OS_LIB_BASE_DIR}example_project'
DIR_LIB_COMMONS = f'{OS_LIB_BASE_DIR}{DIR_COMMONS}'
DIR_LIB_PROP_FILE = f'{OS_LIB_BASE_DIR}{DIR_COMMONS}{os.sep}{FILE_PROJECT_PROPERTIES}'


class Caps(Enum):
    FIRST = 1
    UPPER = 2
    LOWER = 3


def delete_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)


def delete_file(file):
    if os.path.isfile(file):
        os.remove(file)


def is_project_ftsa():
    if not os.path.isdir(os.path.join(os.getcwd(), DIR_DATA)) and \
            not os.path.isdir(os.path.join(os.getcwd(), DIR_IMAGES)) and \
            not os.path.isdir(os.path.join(os.getcwd(), DIR_FEATURES)) and \
            not os.path.isdir(os.path.join(os.getcwd(), DIR_PAGE_OBJECTS)) and \
            not os.path.isdir(os.path.join(os.getcwd(), DIR_RESOURCES)):
        raise NotFTSAProjectException('Você deve estar em um projeto FTSA para executar esta operação.')
    else:
        return True


def get_base_project_path():
    return os.path.join(sys.executable.split('python.exe')[0], DIR_LIB_BASE_PROJECT)


def get_service_project_path():
    return os.path.join(sys.executable.split('python.exe')[0], DIR_LIB_SERVICE_PROJECT)


def get_example_project_path():
    return os.path.join(sys.executable.split('python.exe')[0], DIR_LIB_EXAMPLE_PROJECT)


def get_commons_project_path():
    return os.path.join(sys.executable.split('python.exe')[0], DIR_LIB_COMMONS)


def get_commons_project_properties_file():
    return os.path.join(sys.executable.split('python.exe')[0], DIR_LIB_PROP_FILE)


def get_project_properties():
    project = ConfigParser()
    project.read(os.path.join(os.getcwd(), DIR_RESOURCES, FILE_PROJECT_PROPERTIES))
    return project


def get_properties_file(arquivo):
    prop = ConfigParser()
    prop.read(os.path.join(os.getcwd(), DIR_RESOURCES, f'{arquivo}.properties'))
    return prop


def sanitize(name, caps=Caps.LOWER, inn=' ', out='-'):
    name = unicodedata.normalize('NFD', name)
    name = name.encode('ascii', 'ignore')
    name = name.decode('utf-8')
    if caps == Caps.FIRST:
        name = name.title()
    elif caps == Caps.UPPER:
        name = name.upper()
    else:
        name = name.lower()
    return ''.join([c if c not in inn else out for c in name])
