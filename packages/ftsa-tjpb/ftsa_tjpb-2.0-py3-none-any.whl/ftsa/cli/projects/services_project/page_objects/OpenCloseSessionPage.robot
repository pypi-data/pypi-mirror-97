*** Settings ***
Library     FTSARequestsLibrary
Variables   ../resources/locators.py

*** Variables ***
${ITEM_DE_BUSCA}

*** Keywords ***
Abrir a seção REST/API
    CREATE SESSION      url=${project.get('prop','APIURL')}       alias=${project.get('prop','APIALIAS')}

Fechar a seção REST/API
    DELETE ALL SESSIONS