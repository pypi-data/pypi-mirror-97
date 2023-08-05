import os
from ftsa.cli.utils.files import delete_path, delete_file, is_project_ftsa, get_project_properties


RESULTS_DIRECTORIES = [
    'results',
    'output',
    'pabot_results',
    'report',
    'dist'
]

FILES = [
    '.pabotsuitenames',
    'log.html',
    'report.html',
    'output.xml'
]


def add_tags(args, tipo):
    if hasattr(args, tipo) and getattr(args, tipo) is not None:
        return ' '.join(['--' + tipo + ' ' + i for i in getattr(args, tipo)])
    return ''


def report(args):
    is_project_ftsa()
    clear(args)
    include = add_tags(args, 'include')
    exclude = add_tags(args, 'exclude')

    parallel = 1
    if hasattr(args, 'parallel') and getattr(args, 'parallel') is not None and int(getattr(args, 'parallel')) > 1:
        parallel = int(args.parallel)
    project = get_project_properties()
    try:
        quantity = project.get('prop', 'PARALLEL')
        if quantity is not None and int(quantity) > 1:
            parallel = int(project.get('prop', 'PARALLEL'))
            print(f'A propriedade PARALLEL foi definida no arquivo de propriedades: {parallel}')
    except:
        print('A propriedade PARALLEL não existe no arquivo de propriedades do projeto')

    options = f'--verbose --testlevelsplit'
    if hasattr(args, 'allure') and getattr(args, 'allure') is not None and getattr(args, 'allure'):
        os.system(f'pabot {options} --processes {parallel} --listener allure_robotframework '
                  f'--outputdir ./output {include}{exclude} --timestampoutputs ./features')
        os.system(f'allure serve ./output/allure')
    elif parallel == 1:
        os.system(f'robot -d ./output {include}{exclude} --timestampoutputs ./features')
    else:
        os.system(f'pabot {options} --processes {parallel} --outputdir ./output {include}{exclude} --timestampoutputs ./features')


def clear(args):
    is_project_ftsa()
    for directory in RESULTS_DIRECTORIES:
        delete_path(os.path.join(os.getcwd(), directory))
    for file in FILES:
        delete_file(os.path.join(os.getcwd(), file))


def run(args):
    report(args)
    clear(args)
