from TypeToken import typeToken
from token import mots_cles, Token 
import re

identificateur_pattern = re.compile(r'^[a-zA-Z_]\w*$')


class Lexer:

    def lexer(source_code):
        tokens = []
        pastoken = []
        position = 0
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        chiffre = "0123456789"
        ident = alpha +chiffre+"_"
        while position < len(source_code):
            avancement = position
            lecture = ""
            #On teste d'abord si c'est un token
            for keyword in mots_cles:
                if source_code.startswith(keyword, position) and source_code[position + len(keyword)] not in ident:
                    tokens.append(Token(mots_cles[keyword], keyword, position))
                    pastoken.append(keyword)
                    position += len(keyword)
                    break
            #Sinon c'est peut-être un identificateur
            match = identificateur_pattern.match(source_code, position)
            if match:
                identificateur = match.group()
                tokens.append(typeToken.IDENTIFICATEUR)
                pastoken.append(identificateur)
                position = match.end()
            #Détection d'un nombre (proprement)
            elif source_code[position] in chiffre:
                while source_code[avancement] in chiffre :
                    lecture = lecture + source_code[avancement]
                    avancement += 1
                tokens.append(typeToken.ENTIER,typeToken.POINT,typeToken.ENTIER)
                pastoken.append(lecture)
                position += len(lecture)
            #Détection d'une chaîne de caractères
            elif source_code[position] == '"' or source_code[position] == "'":
                while source_code[avancement] != source_code[position]:
                    lecture = lecture + source_code[avancement]
                    avancement += 1
                tokens.append(typeToken.CARACTERE)
                pastoken.append(lecture)
                position += len(lecture)
            #Détection d'un commentaire
            elif source_code[position:position+1] == "--":
                while source_code[position] != "\n":
                    position += 1
            elif source_code[position] == '\n':
                position += 1
            else:
                for token in tokens:
                    print(token.type)
                print(f"caractere unconnu {source_code[position]} a {position}")
                exit(1)
        return tokens,pastoken

    def peek(self):
        # retourner le prochain token
        None
    def next(self):
        #retourner le prochain token et avancer dans la liste