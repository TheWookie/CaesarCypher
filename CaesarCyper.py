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
             ")" :-1  # to allow for checking the stack order correctly. This is because Paren are not actually operators BUT we have to check against them in our stack. This does not cause any problems because we already have a separate case for handling paren, even though they both use the same stack.
}

def InfixToPostfix(EquationString):
    EquationString = EquationString.upper()
    EquationString = re.sub("(MOD)", "%", EquationString)
    EquationString = re.sub("(\s+)", "", EquationString)  # removing unnecessary spaces.
    Q = []
    Stk = []
    # ^(\d+) #Number at begging of string regex
    # ^([\+\*-\/\^%]) #Opperator at beggining of string regex
    # ^([\(\)]) #matchs oppening and closing paren.
    while len(EquationString) > 0:
        DigitSearch = re.search(r"^(\d+|P)", EquationString)  # tests for digit, OR variable N
        if (DigitSearch):
            EquationString = re.sub(r"^(\d+|P)", "", EquationString)
            if DigitSearch.group(1) == "P":
                Q.append(DigitSearch.group(1))
            else:
                Q.append(int(DigitSearch.group(1)))
            continue
        OperatorSearch = re.search(r"^([\+\*-\/\^%])", EquationString)
        if (OperatorSearch):
            EquationString = re.sub(r"^([\+\*-\/\^%])", "", EquationString)
            op = OperatorSearch.group(1)
            while (len(Stk) > 0 and Operators[Stk[len(Stk) - 1]] >= Operators[op]):
                Q.append(Stk.pop())
            Stk.append(op)
            continue
        ParenSearch = re.search(r"^([\(\)])", EquationString)
        if (ParenSearch):
            EquationString = re.sub(r"^([\(\)])", "", EquationString)
            if (ParenSearch.group(1) == "("):
                Stk.append(ParenSearch.group(1))
            else:  # right paren
                while not Stk[len(Stk) - 1] == "(":
                    Q.append(Stk.pop())
                Stk.pop()  # ditch the left paren
            continue
        #if you want to implement additional mathmatical functionality, this is the spot to start including it. Otherwise, this is an invalid infix equation.
        raise Exception("Not a valid infix equation. {0}".format(EquationString))  # If we reach this line, something has probably gone wrong. http://www.youtube.com/watch?v=Q5cEAhjcv54
    while len(Stk) > 0:
        Q.append(Stk.pop())
    return Q

def ParseRPN(RpnArr, PValue):
    RpnArr = list(RpnArr)  # we need a deep copy. If we don't we'll override P and it'll stay that way through the duration of our encryption.
    ParseStk = []
    for i in range(0, len(RpnArr)):
        if (RpnArr[i] == "P"):
            RpnArr[i] = PValue  # make the mathmatical subsititution here so we can correctly evaluate this equation.
        if (isinstance(RpnArr[i], int)):
            ParseStk.append(RpnArr[i])
        else:
            A = ParseStk.pop()
            B = ParseStk.pop()
            # I have recently researched a more Pythonic way of doing this,
            # however to implement it would be plagarism (because this is a homework assignment.)
            # After I turn it in, I'll make this better. (http://stackoverflow.com/questions/1740726/python-turn-string-into-operator)
            if (RpnArr[i] == "+"):
                ParseStk.append(B + A)  # Order doesn't matter here, but putting B ahead of A is consitent with the other conditions.
            elif (RpnArr[i] == "-"):
                ParseStk.append(B - A)
            elif (RpnArr[i] == "*"):  # See immediately previous note.
                ParseStk.append(B * A)
            elif (RpnArr[i] == "/"):
                ParseStk.append(B // A)  # Forcing integer division. Why? Because for this project (Caesar Cypher) we will need integers so we can index the alphabet.
            elif (RpnArr[i] == "%"):
                ParseStk.append(B % A)
            elif (RpnArr[i] == "^"):
                ParseStk.append(A ** B)  # This MUST be in reverse order to perform correctly
    return ParseStk[0]

def CaesarCypher(message, infix):
    message = message.upper()
    CypherText = ""
    PostFix = InfixToPostfix(infix)
    for i in range(0, len(message)):
        if (message[i] in Alphabet):
            index = Alphabet.index(message[i])
            newIndex = ParseRPN(PostFix, index)
            CypherText += Alphabet[newIndex]
        else:
            CypherText += message[i]  # If the character isn't part of our cypher, like a punctuation mark or a space, we'll just ignore it.
    return CypherText

def DemoCC(message, key, oppKey):
    message = CaesarCypher(message, key)
    print("{} -- {}".format(message, key))
    message = CaesarCypher(message, oppKey)
    print("{} -- {}".format(message, oppKey))
    print()
    return

DemoCC("The quick brown fox jumps over the lazy dog.", "(P+3) mod 26", "(P-3) mod 26")
DemoCC("The rain in spain stays mainly on the plane.", "(P+8) mod 26", "(P-8) mod 26")
DemoCC("Never gunna give you up, never going to let you down.", "(P+(256*12^3004/4+1)) mod 26", "(P-(256*12^3004/4+1)) mod 26")
