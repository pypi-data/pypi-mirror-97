*** Settings ***
Documentation   UC000: Login
Default Tags    all   web   uc000   ct002   fa

Resource        ../../page_objects/LoginPage.robot
Library         DataDriver   ./../../data/UC000-CT002-dados.csv   encoding=utf8

Suite Setup     Inicializo o servidor remoto
Test Setup      Abro o navegador
Test Teardown   Fecho o navegador
Suite Teardown  Finalizo o servidor remoto

Test Template   Autenticação realizada

*** Test Cases ***
# Data Driven for Test Template
Autenticação não realizada quando informo o CPF '${cpf}' e a senha '${senha}'

*** Keywords ***
Autenticação realizada
    [Arguments]    ${cpf}    ${senha}
    Given Sou um "Usuário Qualquer"
    When Informo dados inválidos nos campos de autenticação   ${cpf}   ${senha}
    Then Verifico que a autenticação não foi realizada