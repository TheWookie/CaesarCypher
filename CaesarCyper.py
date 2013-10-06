'''
Created on Oct 5, 2013

@author: Paul
'''
import re

def infixToPostfix(EquationString):
    EquationString = re.sub("(\s+)", "", EquationString) #removing unnecessary spaces.
    
    Q = []
    Stk = []
    
    # ^(\d+) #Number at begging of string regex
    # ^([\+\*-\/\^%]) #Opperator at beggining of string regex
    # ^([\(\)]) #matchs oppening and closing paren.
    while (len(EquationString) > 0):
        DigitSearch = re.search(r"^(\d+)", EquationString)
        OperatorSearch = re.search(r"^([\+\*-\/\^])", EquationString)
        if (DigitSearch):
            Q.append(int(DigitSearch.group(1)))
            EquationString = re.sub(r"^(\d+)", "", EquationString)
            continue
        elif (OperatorSearch):
            Stk.append(OperatorSearch.group(1))
            EquationString = re.sub(r"^([\+\*-\/\^])", "", EquationString)
            continue
        pass
    return [Q, Stk]

print(infixToPostfix("5 + 4"))
print(infixToPostfix("5 + 4 - 3"))