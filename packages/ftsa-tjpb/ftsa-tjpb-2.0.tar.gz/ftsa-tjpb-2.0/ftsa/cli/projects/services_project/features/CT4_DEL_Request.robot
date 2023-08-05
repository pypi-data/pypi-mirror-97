*** Settings ***
Library         FTSARequestsLibrary
Library         JSONLibrary
Library         Collections

Resource        ../page_objects/OpenCloseSessionPage.robot

Test Setup      Setup Test Data
Test Teardown   Clean Test Data

*** Variables ***
${ID}           00000000892d8d82705bb9da
# ID from       ./resources/objectId.html

*** Test Cases ***
DEL User
    [Tags]  ct04
    # Call / Action
    ${response}     DELETE REQUEST  MySession       /user/${ID}

    # Validations
    ${status_code}          CONVERT TO STRING       ${response.status_code}
    LOG TO CONSOLE          ${status_code}
    SHOULD BE EQUAL         ${status_code}          204
    ${body}                 CONVERT TO STRING       ${response.content}
    LOG TO CONSOLE          ${body}
    SHOULD BE EMPTY         ${body}

*** Keywords ***
Setup Test Data
    ${body}         CREATE DICTIONARY   email=diegoquirino@gmail.com
    ...                                 password=Teste123#
    ...                                 firstName=Carlos Diego
    ...                                 lastName=Quirino Lima
    ...                                 role=5f3ed17c9cf96224bca96a92
    ...                                 _id=${ID}
    ${header}       CREATE DICTIONARY   Content-Type    application/json
    CREATE SESSION  SetupSession        ${project.get('prop','BASE_URL')}
    ${response}     POST REQUEST        SetupSession    /user       data=${body}    headers=${header}
    LOG TO CONSOLE  ${response}
    Abrir a seção REST/API

Clean Test Data
    Fechar a seção REST/API
