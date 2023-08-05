import ftsa.cli.modules.install_upgrade_parser as iup
import ftsa.cli.modules.run_report_parser as rep
import ftsa.cli.modules.init_parser as ini

from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    ''' Install parser '''
    install_parser = subparsers.add_parser('install', help='Instala TODAS as dependências do FTSA.')
    install_parser.set_defaults(handler=iup.install)

    ''' Upgrade parser '''
    upgrade_parser = subparsers.add_parser('upgrade', help='Atualiza TODAS as dependências do FTSA.')
    upgrade_parser.set_defaults(handler=iup.upgrade)

    ''' Report parser '''
    report_parser = subparsers.add_parser('report', help='Executa e gera o relatório de execução do projeto FTSA.')
    report_parser.add_argument('-p', '--parallel', help='Número de instâncias paralelas. Ex: 2 (duas) etc.')
    report_parser.add_argument('-i', '--include', action='append',
                               help='Informa as tags que devem ser incluídas. Ex: -i all')
    report_parser.add_argument('-e', '--exclude', action='append',
                               help='Informa as tags que devem ser excluídas. Ex: -e fe')
    report_parser.set_defaults(handler=rep.report)

    ''' Report Clear parser '''
    report_clear_parser = subparsers.add_parser('clear', help='Limpar arquivos e diretórios de relatório.')
    report_clear_parser.set_defaults(handler=rep.clear)

    ''' Run parser'''
    run_parser = subparsers.add_parser('run', help='Executa o projeto FTSA.')
    run_parser.add_argument('-p', '--parallel', help='Número de instâncias paralelas. Ex: 2 (duas) etc.')
    run_parser.add_argument('-i', '--include', action='append',
                            help='Informa as tags que devem ser incluídas. Ex: all')
    run_parser.add_argument('-e', '--exclude', action='append',
                            help='Informa as tags que devem ser excluídas. Ex: fe')
    run_parser.set_defaults(handler=rep.run)

    ''' Init parser '''
    init_parser = subparsers.add_parser('init', help='Inicializa um projeto FTSA (TJPB, básico, com login).')
    init_parser.add_argument('project_name', help='Informa o NOME do projeto FTSA.')
    init_parser.add_argument('-e', '--example', action='store_true',
                             help='Cria um projeto para o FTSA-TJPB (com exemplo).')
    init_parser.add_argument('-s', '--services', action='store_true',
                             help='Cria um projeto para o FTSA-Services (testes REST / API ou XML).')
    init_parser.set_defaults(handler=ini.init)

    ''' Execute command with args '''
    args = parser.parse_args()
    args.handler(args)
