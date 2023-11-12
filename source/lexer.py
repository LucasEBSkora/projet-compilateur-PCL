from TypeToken import mots_cles, typeToken
from token import mots_cles, Token 

def lexer(source_code):
    tokens = []
    position = 0
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    chiffre = "0123456789"
    ident = alpha +chiffre+"_"
    while position < len(source_code):
        avancement = position
        lecture = " "
        #On teste d'abord si token
        for keyword in mots_cles:
            if source_code.startswith(keyword, position) and source_code[position + len(keyword)] not in ident:
                tokens.append(Token(mots_cles[keyword], keyword, position))
                position += len(keyword)
                break
        #Détection d'un nombre
            elif source_code[position] in chiffre:
                while source_code[avancement] in chiffre or source_code[avancement] == '.':
                    lecture = lecture + source_code[avancement]
                    avancement += 1
        #Détection d'une chaîne de caractères
            elif source_code[position] == '"':
                while source_code[avancement] in alpha or source_code[avancement] == " ":
                    lecture = lecture + source_code[avancement]
                    avancement += 1
        #Détection d'une variable
            elif source_code[position] in alpha:
                while source_code[avancement] in alpha :
                    lecture = lecture + source_code[avancement]
                    avancement += 1
        #Détection d'un commentaire
            elif source_code[position:position+1] == "--":
                while source_code[position] != "\n":
                    position += 1
        

        
                


    return tokens
