*** Settings ***
Library         FTSARequestsLibrary
Library         JSONLibrary
Library         Collections

Resource        ../page_objects/OpenCloseSessionPage.robot

Test Setup      Abrir a seção REST/API
Test Teardown   Fechar a seção REST/API

*** Variables ***
${ID}           5f3ed17c9cf96224bca96a95

*** Test Cases ***
GET Users
    [Tags]  ct01
    # Call / Action
    ${response}         GET REQUEST     MySession   /user

    # Validations
    ${status_code}      CONVERT TO STRING       ${response.status_code}
    LOG TO CONSOLE      ${status_code}
    SHOULD BE EQUAL     ${status_code}          200
    ${body}             CONVERT TO STRING       ${response.content}
    LOG TO CONSOLE      ${body}
    SHOULD CONTAIN      ${body}                 test
    # Multiple data validation
    ${body}             TO JSON                 ${response.content}
    ${res_emails}       GET VALUE FROM JSON     ${body}     $.docs[:].email
    LOG TO CONSOLE      ${res_emails}
    SHOULD CONTAIN ANY  ${res_emails[0]}        test@account.com  test@admin.com  test@superadmin.com
    ${content_type_value}   GET FROM DICTIONARY     ${response.headers}     Content-Type
    LOG TO CONSOLE      ${content_type_value}
    SHOULD CONTAIN      ${content_type_value}   application/json

GET User (${ID})
    [Tags]  ct01
    # Call / Action
    ${response}         GET REQUEST     MySession   /user/${ID}

    # Validations
    ${status_code}      CONVERT TO STRING       ${response.status_code}
    LOG TO CONSOLE      ${status_code}
    SHOULD BE EQUAL     ${status_code}          200
    ${body}             CONVERT TO STRING       ${response.content}
    LOG TO CONSOLE      ${body}
    SHOULD CONTAIN      ${body}                 test@account.com
    ${body}             TO JSON                 ${response.content}
    ${test_id}          GET VALUE FROM JSON     ${body}    $.._id
    LOG TO CONSOLE      ${test_id}
    SHOULD BE EQUAL AS STRINGS  ${test_id[0]}   ${ID}
    ${content_type_value}   GET FROM DICTIONARY     ${response.headers}     Content-Type
    LOG TO CONSOLE      ${content_type_value}
    SHOULD CONTAIN      ${content_type_value}   application/json

