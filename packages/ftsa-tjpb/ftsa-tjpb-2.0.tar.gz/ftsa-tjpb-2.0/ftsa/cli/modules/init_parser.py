import shutil
import os
from ftsa.cli.utils.files import sanitize, get_base_project_path, get_example_project_path, get_commons_project_path, \
                                 DIR_COMMONS, DIR_RESOURCES, FILE_PROJECT_PROPERTIES, is_project_ftsa, \
                                 get_service_project_path, FILE_GITIGNORE, FILE_MAIN_PY, FILE_DOCKERFILE


def init(args):
    if hasattr(args, 'project_name') and getattr(args, 'project_name') is not None:
        project_base_dir = sanitize(args.project_name)
        if hasattr(args, 'services') and getattr(args, 'services') is not None and getattr(args, 'services'):
            shutil.copytree(get_service_project_path(), project_base_dir)
        elif hasattr(args, 'example') and getattr(args, 'example') is not None and getattr(args, 'example'):
            shutil.copytree(get_example_project_path(), project_base_dir)
        else:
            shutil.copytree(get_base_project_path(), project_base_dir)
        os.chdir(project_base_dir)
        update(args, True)


def update(args, first = False):
    is_project_ftsa()
    if os.path.isdir(f'{DIR_COMMONS}'):
        shutil.rmtree(f'{DIR_COMMONS}')
    shutil.copytree(get_commons_project_path(), f'{DIR_COMMONS}')
    if first:
        shutil.move(f'{DIR_COMMONS}{os.sep}{FILE_PROJECT_PROPERTIES}',
                    f'{DIR_RESOURCES}{os.sep}{FILE_PROJECT_PROPERTIES}')
        shutil.move(f'{DIR_COMMONS}{os.sep}{FILE_GITIGNORE}',
                    f'{FILE_GITIGNORE}')
        shutil.move(f'{DIR_COMMONS}{os.sep}{FILE_MAIN_PY}',
                    f'{FILE_MAIN_PY}')
        shutil.move(f'{DIR_COMMONS}{os.sep}{FILE_DOCKERFILE}',
                    f'{FILE_DOCKERFILE}')
    if os.path.isdir(f'{DIR_COMMONS}'):
        shutil.rmtree(f'{DIR_COMMONS}')
