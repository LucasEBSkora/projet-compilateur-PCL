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
             "Ada.Text_IO" : typeToken.ADA,
             ";" : typeToken.SEMICOLON,
             "EOF" : typeToken.EOF,
             "," : typeToken.COMMA,
             ":" : typeToken.COLON,
             ":=" : typeToken.ASSIGN,
             "(" : typeToken.OPEN,
             ")" : typeToken.CLOSE
            }

class Token:
    def __init__(self, token_type, value, position):
        self.token_type = token_type
        self.value = value
        self.position = position


