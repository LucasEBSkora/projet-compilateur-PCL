from TypeToken import mots_cles, typeToken
from token import mots_cles, Token 

def lexer(source_code):
    tokens = []
    position = 0

    while position < len(source_code):
        avancement = position
        a_lire = source_code[position]
        while a_lire not in mots_cles:
            a_lire = a_lire+source_code[avancement]
            avancement +=1
        # Exemple simplifié : recherche de mots-clés
        for keyword in mots_cles:
            if source_code.startswith(keyword, position):
                tokens.append(Token(mots_cles[keyword], keyword, position))
                position += len(keyword)
                break
        else:
            # Aucun mot-clé trouvé, déplacez-vous vers le prochain caractère
            position += 1

    return tokens
