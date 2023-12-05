from TypeToken import typeToken

#Dictionaire mots clés 

mots_cles = {"access":    typeToken.ACCESS,
             "and":       typeToken.AND,
             "begin":     typeToken.BEGIN,
             "else":      typeToken.ELSE,
             "ifelse":    typeToken.ELSEIF,
             "end":       typeToken.END,
             "false":     typeToken.FALSE,
             "for":       typeToken.FOR,
             "function":  typeToken.FUNCTION,
             "if":        typeToken.IF,
             "in":        typeToken.IN,
             "is":        typeToken.IS,
             "loop":      typeToken.LOOP,
             "new":       typeToken.NEW,
             "not":       typeToken.NOT,
             "null":      typeToken.NULL,
             "or":        typeToken.OR,
             "out":       typeToken.OUT,
             "procedure": typeToken.PROCEDURE,
             "record":    typeToken.RECORD,
             "rem":       typeToken.REM,
             "return":    typeToken.RETURN,
             "reverse":   typeToken.REVERSE,
             "then":      typeToken.THEN,
             "true":      typeToken.TRUE,
             "type":      typeToken.TYPE,
             "use":       typeToken.USE,
             "while":     typeToken.WHILE,
             "with":      typeToken.WITH,
            }

class Token:
    def __init__(self, type, value, ligne, colomne):
        self.type = type
        self.value = value
        self.ligne = ligne
        self.colomne = colomne


