*** Settings ***
Documentation   UC000: Autenticação do Usuário
Default Tags    all   web   uc000   fb

Resource        ../../page_objects/AutenticacaoUsuarioPage.robot

Suite Setup     Inicializando o servidor de imagens
Test Setup      Abro o navegador
Test Teardown   Fecho o navegador
Suite Teardown  Fechando o servidor de imagens

Test Template   Autenticação realizada

*** Test Cases ***
# Data Driven for Test Template                                     #nome_perfil
Autenticação realizada com sucesso para o usuário Administrador     Administrador
Autenticação realizada com sucesso para o usuário Visitante         Visitante
Autenticação realizada com sucesso para o usuário Gestor            Gestor
Autenticação realizada com sucesso para o usuário Servidor          Servidor

*** Keywords ***
Autenticação realizada
    [Arguments]  ${nome_perfil}
    Given Sou um "${nome_perfil}"
    When Informo os dados de autenticação do usuário
    Then Verifico que a autenticação foi realizada com sucesso
