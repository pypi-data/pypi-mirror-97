*** Settings ***
Library         FTSARequestsLibrary
Library         JSONLibrary
Library         Collections

Resource        ../page_objects/OpenCloseSessionPage.robot

Test Setup      Setup Test Data
Test Teardown   Clean Test Data

*** Variables ***
${ID}           00000000892d8d82705bb9d2
# ID from       ./resources/objectId.html

*** Test Cases ***
POST User
    [Tags]  ct02
    # Call / Action
    ${body}         CREATE DICTIONARY   email=diegoquirino@gmail.com
    ...                                 password=Teste123#
    ...                                 firstName=Carlos Diego
    ...                                 lastName=Quirino Lima
    ...                                 role=5f3ed17c9cf96224bca96a92
    ...                                 _id=${ID}
    ${header}       CREATE DICTIONARY   Content-Type    application/json
    ${response}     POST REQUEST        MySession       /user       data=${body}    headers=${header}

    # Validations
    ${status_code}          CONVERT TO STRING       ${response.status_code}
    LOG TO CONSOLE          ${status_code}
    SHOULD BE EQUAL         ${status_code}          201
    ${body}                 TO JSON                 ${response.content}
    LOG TO CONSOLE          ${body}
    ${res_id}               GET VALUE FROM JSON     ${body}     $._id
    LOG TO CONSOLE          ${res_id}
    SHOULD NOT BE EMPTY     ${res_id[0]}
    SHOULD BE EQUAL         ${res_id[0]}            ${ID}

*** Keywords ***
Setup Test Data
    Abrir a seção REST/API

Clean Test Data
    CREATE SESSION  TearDownSession     ${project.get('prop','BASE_URL')}
    ${response}     DELETE REQUEST      TearDownSession       /user/${ID}
    LOG TO CONSOLE  ${response}
    Fechar a seção REST/API
