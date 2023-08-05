*** Settings ***
Documentation   Teste de uma biblioteca criada em Python
Default Tags    mylibcalc
Library         ../resources/MyLibCalculadora.py

Test Template   Realizar operações de cálculo

*** Test Cases ***
T1 - Calcular utilizando com os números   10  20  30  200
T2 - Calcular utilizando com os números   20  20  40  500


*** Keywords ***
Realizar operações de cálculo
    [Arguments]   ${a}  ${b}   ${soma}  ${mult}
    Some          ${a}  ${b}
    O resultado deve ser       ${soma}
    O resultado nao deve ser   ${mult}
    Multiplique   ${a}  ${b}
    O resultado deve ser       ${mult}
    O resultado nao deve ser   ${soma}