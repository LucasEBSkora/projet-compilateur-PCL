from TypeToken import typeToken
from token import mots_cles, Token 
import re
from __init__ import init

identificateur_pattern = re.compile(r'^[a-zA-Z_]\w*$')


class Tokens:

    def lexer(source_code):
        position = 0
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        chiffre = "0123456789"
        ident = alpha +chiffre+"_"
        ligne = 0
        cln = 0
        tokens = []
        while position < len(source_code):
            avancement = position
            lecture = ""
            #On teste d'abord si c'est un token
            for keyword in mots_cles:
                if source_code.startswith(keyword, position) and source_code[position + len(keyword)] not in ident:
                    tokens.append(Token(mots_cles[keyword], keyword, position))
                    tokens.append(keyword)
                    tokens.append(ligne)
                    position += len(keyword)
                    cln += len(keyword)
                    tokens.append(cln)
                    break
            #Sinon c'est peut-être un identificateur
            match = identificateur_pattern.match(source_code, position)
            if match:
                identificateur = match.group()
                tokens.append(typeToken.IDENTIFICATEUR)
                tokens.append(identificateur)
                tokens.append(ligne)
                position = match.end()
                cln += len(keyword)
                tokens.append(cln)
            #Détection d'un nombre (proprement)
            elif source_code[position] in chiffre:
                while source_code[avancement] in chiffre :
                    lecture = lecture + source_code[avancement]
                    avancement += 1
                tokens.append(typeToken.ENTIER)
                tokens.append(lecture)
                tokens.append(ligne)
                position += len(lecture)
                cln += len(lecture)
                tokens.append(cln)
            #Détection d'une chaîne de caractères
            elif source_code[position] == '"' or source_code[position] == "'":
                while source_code[avancement] != source_code[position]:
                    lecture = lecture + source_code[avancement]
                    avancement += 1
                tokens.append(typeToken.CARACTERE)
                tokens.append(lecture)
                tokens.append(ligne)
                position += len(lecture)
                cln += len(lecture)
                tokens.append(cln)
            #Détection d'un commentaire
            elif source_code[position:position+1] == "--":
                while source_code[position] != "\n":
                    position += 1
            elif source_code[position] == '\n':
                position += 1
                ligne += 1
                cln = 0
            else:
                for token in tokens:
                    print(token.type)
                print(f"caractere inconnu {source_code[position]} a {position}")
                exit(1)
        return tokens
    
    def peek(tokens):
        if not tokens:
            return None 
        else :
            return tokens[0:3]

    def next(tokens):
        if not tokens:
            return None 
        else :
            tok = tokens[0:3]
            tokens = tokens[4:]
            return tok