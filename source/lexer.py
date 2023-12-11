from TypeToken import typeToken
from Token import mots_cles, Token 
import re
from __init__ import init

identificateur_pattern = re.compile(r'^[a-zA-Z_]\w*$')


class Tokens:

    def __init__(self, source_code= None):
        if source_code is not None:
            self.lexer(source_code)
    
    def lexer(self, source_code):
        position = 0
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        chiffre = "0123456789"
        ident = alpha +chiffre+"_"
        ligne = 0
        cln = 0
        self.tokens = []
        while position < len(source_code):
            avancement = position
            lecture = ""
            #On teste d'abord si c'est un token
            for keyword in mots_cles:
                if not source_code.startswith(keyword, position):
                    continue
                if position + len(keyword) < len(source_code) and source_code[position + len(keyword)] not in ident:
                    self.tokens.append(Token(mots_cles[keyword], keyword, position))
                    self.tokens.append(keyword)
                    self.tokens.append(ligne)
                    position += len(keyword)
                    cln += len(keyword)
                    self.tokens.append(cln)
                    break
            #Sinon c'est peut-être un identificateur
            match = identificateur_pattern.match(source_code, position)
            if match:
                identificateur = match.group()
                self.tokens.append(typeToken.IDENTIFICATEUR)
                self.tokens.append(identificateur)
                self.tokens.append(ligne)
                position = match.end()
                cln += len(keyword)
                self.tokens.append(cln)
            #Détection d'un nombre (proprement)
            elif source_code[position] in chiffre:
                while source_code[avancement] in chiffre :
                    lecture = lecture + source_code[avancement]
                    avancement += 1
                self.tokens.append(typeToken.ENTIER)
                self.tokens.append(lecture)
                self.tokens.append(ligne)
                position += len(lecture)
                cln += len(lecture)
                self.tokens.append(cln)
            #Détection d'une chaîne de caractères
            elif source_code[position] == '"' or source_code[position] == "'":
                while source_code[avancement] != source_code[position]:
                    lecture = lecture + source_code[avancement]
                    avancement += 1
                self.tokens.append(typeToken.CARACTERE)
                self.tokens.append(lecture)
                self.tokens.append(ligne)
                position += len(lecture)
                cln += len(lecture)
                self.tokens.append(cln)
            #Détection d'un commentaire
            elif source_code[position:position+1] == "--":
                while source_code[position] != "\n":
                    position += 1
            elif source_code[position] == '\n':
                position += 1
                ligne += 1
                cln = 0
            else:
                for token in self.tokens:
                    print(token.type)
                print(f"caractere inconnu {source_code[position]} a {position}")
                exit(1)
    
    def peek(self):
        return self.tokens[0]

    def next(self):
        token = self.tokens[0]
        self.tokens = self.tokens[1:]
        return token