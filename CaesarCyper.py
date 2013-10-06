'''
Created on Oct 5, 2013

@author: Paul
'''
import re

Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Operators = {  # Setup Opperators and their priorities. P-lease E-xcuse M-y D-ear A-unt S-ally
             "+" : 0,
             "-" : 0,
             "*" : 1,
             "/" : 1,
             "%" : 1,
             "^" : 2,
             "(" :-1,  # Turns out we definitely need paren here for comparisons against operators. HOWEVER they must have a lower priority 
             ")" :-1  # to allow for checking the stack order correctly. This is okay because paren are handled in a differently anyway.
}

def InfixToPostfix(EquationString):
    EquationString = EquationString.upper()
    EquationString = re.sub("(\s+)", "", EquationString)  # removing unnecessary spaces.
    Q = []
    Stk = []
    # ^(\d+) #Number at begging of string regex
    # ^([\+\*-\/\^%]) #Opperator at beggining of string regex
    # ^([\(\)]) #matchs oppening and closing paren.
    while len(EquationString) > 0:
        print("New iteration. Sanity check-\t\tQueue: {}, Stack: {}".format(Q, Stk))
        DigitSearch = re.search(r"^(\d+|N)", EquationString)  # tests for digit, OR variable N
        if (DigitSearch):
            EquationString = re.sub(r"^(\d+|N)", "", EquationString)
            print("Appending {} to Queue.".format(DigitSearch.group(1)))
            if DigitSearch.group(1) == "N":
                Q.append(DigitSearch.group(1))
            else:
                Q.append(int(DigitSearch.group(1)))
            continue
        OperatorSearch = re.search(r"^([\+\*-\/\^])", EquationString)
        if (OperatorSearch):
            EquationString = re.sub(r"^([\+\*-\/\^])", "", EquationString)
            op = OperatorSearch.group(1)
            while (len(Stk) > 0 and Operators[Stk[len(Stk) - 1]] >= Operators[op]):
                print("Comparing operators {0} and {1}".format(Stk[len(Stk) - 1], op))
                print("Poping {0} from Stack and appending to Queue.".format(Stk[len(Stk) - 1]))
                Q.append(Stk.pop())
            print("Pushing operator {0} to Stack.".format(op))
            Stk.append(op)
            continue
        ParenSearch = re.search(r"^([\(\)])", EquationString)
        if (ParenSearch):
            EquationString = re.sub(r"^([\(\)])", "", EquationString)
            if (ParenSearch.group(1) == "("):
                Stk.append(ParenSearch.group(1))
                print("Pushing ( to stack")
            else:  # right paren
                print("We have a )")
                while not Stk[len(Stk) - 1] == "(":
                    print("Popping {0} from stack and appending to q.".format(Stk[len(Stk) - 1]))
                    Q.append(Stk.pop())
                print("Popping and ditching {0}, because we don't need it anymore.".format(Stk[len(Stk) - 1]))
                Stk.pop()  # ditch the left paren
            continue
        print("Something has gone terribly wrong if this has been printed.")  # If we reach this line, something has probably gone wrong. http://www.youtube.com/watch?v=Q5cEAhjcv54
    while len(Stk) > 0:
        Q.append(Stk.pop())
    return Q

def ParseRPN(RpnArr, NValue):
    ParseStk = []
    for i in range(0, len(RpnArr)):
        if (RpnArr[i] == "N"):
            RpnArr[i] = NValue  # make the mathmatical subsititution here so we can correctly evaluate this equation.
        if (isinstance(RpnArr[i], int)):
            ParseStk.append(RpnArr[i])
        else:
            A = ParseStk.pop()
            B = ParseStk.pop()
            # I have recently researched a more Pythonic way of doing this,
            # however to implement it would be plagarism. (Which sucks because this is a homework assignment)
            # After I turn it in, I'll make this better. (http://stackoverflow.com/questions/1740726/python-turn-string-into-operator)
            if (RpnArr[i] == "+"):
                ParseStk.append(B + A)  # Order doesn't matter here, but putting B ahead of A is consitent with the other conditions.
            elif (RpnArr[i] == "-"):
                ParseStk.append(B - A)
            elif (RpnArr[i] == "*"):  # See immediately previous note.
                ParseStk.append(B * A)
            elif (RpnArr[i] == "/"):
                ParseStk.append(B / A)  # not forcing integer division for now.
            elif (RpnArr[i] == "%"):
                ParseStk.append(B % A)
            elif (RpnArr[i] == "^"):
                ParseStk.append(A ** B)  # This MUST be in reverse order to perform correctly
    return ParseStk[0]

eqn = "9 + N / ( 7 - 3 )"
rpn = InfixToPostfix(eqn)  # should be [9, "N", 7, 3, "-", "/", "+"]
print (rpn)
rslt = ParseRPN(rpn, 24)
print(rslt)  # the answer should be 15.
