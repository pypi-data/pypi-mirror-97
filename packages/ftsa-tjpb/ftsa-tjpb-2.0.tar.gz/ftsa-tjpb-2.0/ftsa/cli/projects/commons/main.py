import os

if __name__ == '__main__':
    # print(f'{os.getcwd()}')
    os.system(f'ftsa report')

    # OR REMOTE
    # os.system(f'docker build -t ftsa-tjpb-image ./')
    # os.system(f'docker run --rm --name execucao_robot '
    #           f'-v "{os.getcwd()}":/opt/robotframework/tests '
    #           f'ftsa-tjpb-image '
    #           f'ftsa report')
