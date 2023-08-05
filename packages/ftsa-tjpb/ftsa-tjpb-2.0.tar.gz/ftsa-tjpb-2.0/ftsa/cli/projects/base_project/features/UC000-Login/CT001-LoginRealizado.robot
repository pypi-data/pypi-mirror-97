*** Settings ***
Documentation   UC000: Login
Default Tags    all   web   uc000   ct001   fb

Resource        ../../page_objects/LoginPage.robot

Suite Setup     Inicializo o servidor remoto
Test Setup      Abro o navegador
Test Teardown   Fecho o navegador
Suite Teardown  Finalizo o servidor remoto

Test Template   Autenticação realizada

*** Test Cases ***
# Data Driven for Test Template                                     #nome_perfil
Autenticação realizada com sucesso para o usuário Administrador     Administrador
Autenticação realizada com sucesso para o usuário Servidor          Servidor

*** Keywords ***
Autenticação realizada
    [Arguments]  ${nome_perfil}
    Given Sou um "${nome_perfil}"
    When Informo os dados de autenticação do usuário
    Then Verifico que a autenticação foi realizada com sucesso