*** Settings ***
Library         FTSARequestsLibrary
Library         JSONLibrary
Library         Collections

Resource        ../page_objects/OpenCloseSessionPage.robot

Test Setup      Setup Test Data
Test Teardown   Clean Test Data

*** Variables ***
${BASE_URL}     http://localhost:8080
${ID}           00000000892d8d82705bb9d7
# ID from       ./resources/objectId.html

*** Test Cases ***
PUT User
    [Tags]  ct03
    # Call / Action
    ${body}         CREATE DICTIONARY   firstName=Carlos Diego Modificado
    ...                                 lastName=Quirino Lima Modificado
    ${header}       CREATE DICTIONARY   Content-Type    application/json
    ${response}     PUT REQUEST         MySession       /user/${ID}     data=${body}    headers=${header}

    # Validations
    ${status_code}          CONVERT TO STRING       ${response.status_code}
    LOG TO CONSOLE          ${status_code}
    SHOULD BE EQUAL         ${status_code}          200
    ${body}                 TO JSON                 ${response.content}
    LOG TO CONSOLE          ${body}
    ${res_id}               GET VALUE FROM JSON     ${body}     $._id
    ${res_nome}             GET VALUE FROM JSON     ${body}     $.firstName
    ${res_sobrenome}        GET VALUE FROM JSON     ${body}     $.lastName
    LOG TO CONSOLE          ${res_id}
    SHOULD NOT BE EMPTY     ${res_id[0]}
    SHOULD BE EQUAL         ${res_id[0]}            ${ID}
    SHOULD BE EQUAL         ${res_nome[0]}          Carlos Diego Modificado
    SHOULD BE EQUAL         ${res_sobrenome[0]}     Quirino Lima Modificado

*** Keywords ***
Setup Test Data
    ${body}         CREATE DICTIONARY   email=diegoquirino@gmail.com
    ...                                 password=Teste123#
    ...                                 firstName=Carlos Diego
    ...                                 lastName=Quirino Lima
    ...                                 role=5f3ed17c9cf96224bca96a92
    ...                                 _id=${ID}
    ${header}       CREATE DICTIONARY   Content-Type    application/json
    CREATE SESSION  SetupSession        ${BASE_URL}
    ${response}     POST REQUEST        SetupSession    /user       data=${body}    headers=${header}
    LOG TO CONSOLE  ${response}
    Abrir a seção REST/API

Clean Test Data
    CREATE SESSION  TearDownSession     ${project.get('prop','BASE_URL')}
    ${response}     DELETE REQUEST      TearDownSession       /user/${ID}
    LOG TO CONSOLE  ${response}
    Fechar a seção REST/API
