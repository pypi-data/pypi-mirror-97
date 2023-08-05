*** Settings ***
Library     FTSASeleniumLibrary
Library     String
Library     OperatingSystem
#Library     SikuliLibrary   mode=NEW
Variables   ../resources/locators.py

*** Variables ***
${PERFIL}
${IMAGE_DIR}  .${/}data${/}img

*** Keywords ***
Inicializando o servidor de imagens
    #SikuliLibrary.START SIKULI PROCESS
    #SikuliLibrary.ADD IMAGE PATH    ${IMAGE_DIR}
    LOG TO CONSOLE      Inicializando servidor de Images no diretório ${IMAGE_DIR}

Abro o navegador
    OPEN BROWSER        ${project.get('prop','URL')}    ${project.get('prop','BROWSER')}

Sou um "${nome_perfil}"
    ${nome_perfil}   CONVERT TO LOWER CASE   ${nome_perfil}
    SET SUITE VARIABLE   ${PERFIL}   ${nome_perfil}
    ${botao_login_novamente_presente}  RUN KEYWORD AND RETURN STATUS   ELEMENT SHOULD BE VISIBLE   ${botao_login_novamente}
    RUN KEYWORD IF  ${botao_login_novamente_presente}  CLICK ELEMENT   ${botao_login_novamente}
    #SikuliLibrary.HIGHLIGHT     botao_login_novamente.png   secs=1
    #SikuliLibrary.CLICK         botao_login_novamente.png

Autenticar-se com
    [Arguments]   ${cpf}   ${senha}
    ELEMENT SHOULD BE VISIBLE    ${campo_usuario}
    FTSASeleniumLibrary.INPUT TEXT   ${campo_usuario}   ${cpf}
    ELEMENT SHOULD BE VISIBLE    ${campo_senha}
    FTSASeleniumLibrary.INPUT TEXT   ${campo_senha}     ${senha}
    ELEMENT SHOULD BE VISIBLE    ${botao_entrar}
    CLICK ELEMENT   ${botao_entrar}

Informo os dados de autenticação do usuário
    ${cpf}     Catenate   SEPARATOR=_   ${PERFIL}  cpf
    ${senha}   Catenate   SEPARATOR=_   ${PERFIL}  senha
    Autenticar-se com  ${project.get('prop', '${cpf}')}  ${project.get('prop', '${senha}')}

Informo dados inválidos nos campos de autenticação
    [Arguments]         ${cpf}   ${senha}
    Autenticar-se com   ${cpf}   ${senha}

Verifico que a autenticação foi realizada com sucesso
    PAGE SHOULD CONTAIN  Sucesso ao se logar

Verifico que a autenticação não foi realizada
    PAGE SHOULD CONTAIN  Usuário ou senha inválidos

Verifico que a o botão entrar não está habilitado
    ELEMENT SHOULD BE DISABLED   ${botao_entrar}

Fecho o navegador
    CLOSE ALL BROWSERS

Fechando o servidor de imagens
    #SikuliLibrary.STOP REMOTE SERVER
    LOG TO CONSOLE    Finalizando servidor de Images no diretório ${IMAGE_DIR}