*** Settings ***
Library      JSONLibrary

*** Variables ***
${FILE}      ./data/ct05.json
# Lidando com JSON
# Documentação: https://github.com/robotframework-thailand/robotframework-jsonlibrary
# Find JSON path: http://jsonpathfinder.com
# JSON path: http://jsonpath.com

*** Test Cases ***
JSON manipulation keywords
    [Tags]  ct05
    ${json_obj}         LOAD JSON FROM FILE     ${FILE}
    LOG TO CONSOLE      ${json_obj}

    ${nome}             GET VALUE FROM JSON     ${json_obj}     $..firstName
    LOG TO CONSOLE      ${nome}
    SHOULD BE EQUAL     ${nome[0]}              Carlos Diego

    ${sobrenome}        GET VALUE FROM JSON     ${json_obj}     $..lastName
    LOG TO CONSOLE      ${sobrenome}
    SHOULD BE EQUAL     ${sobrenome[0]}         Quirino Lima

    ${email}            GET VALUE FROM JSON     ${json_obj}     $..email
    LOG TO CONSOLE      ${email}
    SHOULD BE EQUAL     ${email[0]}             diegoquirino@gmail.com

