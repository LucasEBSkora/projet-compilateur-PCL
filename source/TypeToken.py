from enum import Enum

#Enum

class typeToken(Enum):
    ACCESS = 0
    AND = 1
    BEGIN = 2
    ELSE = 3
    ELSEIF = 4
    END = 5
    FALSE = 6
    FOR = 7 
    FUNCTION = 8
    IF = 9
    IN = 10
    IS = 11
    LOOP = 12
    NEW = 13
    NOT = 14
    NULL = 15
    OR = 16
    OUT = 17
    PROCEDURE = 18
    RECORD = 19
    REM = 20
    RETURN = 21
    REVERSE = 22
    THEN = 23
    TRUE = 24
    TYPE = 25
    USE = 26
    WHILE = 27
    WITH = 28
    EQ = 29 # =
    NE = 30 # /=
    LT = 31 # < 
    LE = 32 # <=
    GE = 33 # >= 
    GT = 34 # >
    MINUS = 35 # -
    PLUS = 36 # +
    MUL = 37 # *
    DIV = 37 # /
    POINT = 38 # . (accès) 
    AFFECT = 39 # :=
    ENTIER = 40
    CARACTERE = 41
    IDENTIFICATEUR = 42
    ADA = 43 #"Ada.Text_IO"
    SEMICOLON = 44 #;
    EOF = 45
    COMMA = 46 #,
    COLON = 47 #:
    CHARACTER_APOSTROFE_VAL = 48 #character'val
    PARENG = 49 #(
    PAREND = 50 #)
    DEUXPOINTS = 51 #..
