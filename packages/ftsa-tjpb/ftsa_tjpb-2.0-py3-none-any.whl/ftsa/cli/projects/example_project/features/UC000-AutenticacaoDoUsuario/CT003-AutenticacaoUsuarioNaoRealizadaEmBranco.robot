*** Settings ***
Documentation   UC000: Autenticação do Usuário
Default Tags    all   web   uc000   fe

Resource        ../../page_objects/AutenticacaoUsuarioPage.robot
Library         DataDriver   ./../../data/CT003-dados.csv   encoding=utf8

Suite Setup     Inicializando o servidor de imagens
Test Setup      Abro o navegador
Test Teardown   Fecho o navegador
Suite Teardown  Fechando o servidor de imagens

Test Template   Autenticação não realizada para dados inválidos

*** Test Cases ***
Autenticação não realizada quando informo o CPF '${cpf}' e a senha '${senha}'

*** Keywords ***
Autenticação não realizada para dados inválidos
    [Arguments]   ${cpf}   ${senha}
    Given Sou um "Usuário Qualquer"
    When Informo dados inválidos nos campos de autenticação   ${cpf}   ${senha}
    Then Verifico que a o botão entrar não está habilitado