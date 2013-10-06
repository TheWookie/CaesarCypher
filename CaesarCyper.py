'''
Created on Oct 5, 2013

@author: Paul
'''
import re

def InfixToPostfix(EquationString):
    EquationString = EquationString.upper()
    #EquationString = re.sub("N", NValue, EquationString) #replace the variable with the actual N value.
    EquationString = re.sub("(\s+)", "", EquationString) #removing unnecessary spaces.
    
    Q = []
    Stk = []
    
    # ^(\d+) #Number at begging of string regex
    # ^([\+\*-\/\^%]) #Opperator at beggining of string regex
    # ^([\(\)]) #matchs oppening and closing paren.
    while len(EquationString) > 0:
        DigitSearch = re.search(r"^(\d+|N)", EquationString) #tests for digit, OR variable N
        if (DigitSearch):
            if DigitSearch.group(1) == "N":
                Q.append(DigitSearch.group(1))
            else:
                Q.append(int(DigitSearch.group(1)))
            EquationString = re.sub(r"^(\d+)", "", EquationString)
            continue
        OperatorSearch = re.search(r"^([\+\*-\/\^])", EquationString)
        if (OperatorSearch):
            Stk.append(OperatorSearch.group(1))
            EquationString = re.sub(r"^([\+\*-\/\^])", "", EquationString)
            continue
        #If we reach this line, something has probably gone wrong.
        pass
    return [Q, Stk]

def ParseRPN(RPN, NValue):
    ParseStk = []
    for i in range(0, len(RPN)):
        
    return

print(infixToPostfix("5 + 4"))
print(infixToPostfix("5 + 4 - 3"))