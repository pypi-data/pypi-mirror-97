import os
import platform

DEPENDENCIES = [
    'robotframework',
    'allure-python-commons',
    'allure-pytest',
    'allure-behave',
    'allure-robotframework',
    'robotframework-pabot',
    'robotframework-seleniumlibrary',
    'robotframework-appiumlibrary',
    'robotframework-faker',
    'robotframework-datadriver',
    'robotframework-databaselibrary',
    'robotframework-SikuliLibrary',
    'robotframework-requests',
    'robotframework-jsonlibrary',
    'robotframework-sshlibrary',
    'robotframework-pdf2textlibrary',
    'pyautogui',
    'selenium',
    'webdrivermanager',
    'opencv-python',
    'jproperties',
    'requests',
    'jsonpath_rw',
    'jsonpath_rw_ext',
    'pandas',
    'numpy',
    'PyMySQL',
    'psycopg2',
    'cx_Oracle',
    'ftsa-tjpb-core'
]

BROWSERS = [
    'firefox',
    'chrome',
    'opera'
]


def run(up):
    for dependency in DEPENDENCIES:
        os.system(f'pip install {"--upgrade " if up else ""}{dependency}')
    for browser in BROWSERS:
        os.system(f'webdrivermanager {browser}')
    if platform.system() in 'Windows':
        os.system(f'webdrivermanager edge')
        os.system(f'webdrivermanager ie')
    os.system('npm install -g allure-commandline')
    os.system('npm install -g appium')


def install(args):
    run(False)


def upgrade(args):
    run(True)
