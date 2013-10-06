'''
Created on Oct 5, 2013

@author: Paul
'''
import re

Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Operators = "^*/+-"

def InfixToPostfix(EquationString):
    EquationString = EquationString.upper()
    # EquationString = re.sub("N", NValue, EquationString) #replace the variable with the actual N value.
    EquationString = re.sub("(\s+)", "", EquationString)  # removing unnecessary spaces.
    
    Q = []
    Stk = []
    
    # ^(\d+) #Number at begging of string regex
    # ^([\+\*-\/\^%]) #Opperator at beggining of string regex
    # ^([\(\)]) #matchs oppening and closing paren.
    while len(EquationString) > 0:
        DigitSearch = re.search(r"^(\d+|N)", EquationString)  # tests for digit, OR variable N
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
        # If we reach this line, something has probably gone wrong.
        pass
    return [Q, Stk]

def ParseRPN(RpnArr, NValue):
    ParseStk = []
    for i in range(0, len(RpnArr)):
        if (RpnArr[i] == "N"):
            RpnArr[i] = NValue  # make the mathmatical subsititution here so we can correctly evaluate this equation.
        if (isinstance(RpnArr[i], int)):
            ParseStk.append(RpnArr[i])
        else:
            if Operators.index(RpnArr[i]):
                A = ParseStk.pop()
                B = ParseStk.pop()
                # I have recently researched a more Pythonic way of doing this,
                # however to implement it would be plagarism. (This is a homework assignment)
                # After I turn it in, I'll make this better. (http://stackoverflow.com/questions/1740726/python-turn-string-into-operator)
                if (RpnArr[i] == "+"):
                    ParseStk.append(A + B)
                elif (RpnArr[i] == "-"):
                    ParseStk.append(B - A)
                elif (RpnArr[i] == "*"):
                    ParseStk.append(A * B)
                elif (RpnArr[i] == "/"):
                    ParseStk.append(B / A)
    return ParseStk[0]

# eqn = "5 + 4 - 3"
# rpn = InfixToPostfix(eqn)
# print(rpn)
# rpn = rpn[0] + rpn[1]
# print(rpn)
rpn = [9, "N", 7, 3, "-", "/", "+"]
rslt = ParseRPN(rpn, 24)
print(rslt) 
