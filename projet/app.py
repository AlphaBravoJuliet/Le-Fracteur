# Importation des modules nécessaires depuis Flask
from flask import Flask, render_template, request, jsonify

# Création de l'application Flask
app = Flask(__name__)

# Fonction pour vérifier la structure d'un IBAN
def verifier_structure_IBAN(IBAN):
    # Supprimer les espaces et les tirets de l'IBAN
    IBAN = IBAN.replace(" ", "").replace("-", "")

    # Vérifier la longueur de l'IBAN
    if len(IBAN) <= 18:
        return False

    # Vérifier les deux premiers caractères (code pays en majuscules)
    code_pays = IBAN[:2].upper()

    # Vérifier si le code pays contient uniquement des lettres majuscules
    if not code_pays.isalpha() or not code_pays.isupper():
        return False
    return True

# Fonction pour calculer la fraction continue d'un nombre rationnel
def fraction_continue(n, d):
    if d == 0:
        return []
    q = n // d
    r = n - q * d
    return [q] + fraction_continue(d, r)

# Fonction pour convertir une liste en fraction
def fraction(liste):
    n, d, num, den = 0, 1, 1, 0
    for u in liste:
        n, d, num, den = num, den, num * u + n, den * u + d
    return str(num) + "/" + str(den)

# Fonction pour encrypter un message en utilisant une fraction continue
def encrypter(message):
    L = [ord(letter) for letter in message]  # Conversion des caractères en valeurs ASCII
    return fraction(L)

# Fonction pour encrypter un message dans le format d'un IBAN
def encrypter_pour_IBAN(message):
    L = []
    # Conversion des caractères en valeurs numériques selon le standard IBAN
    for lettre in message:
        if 48 <= ord(lettre) <= 57:
            L.append(ord(lettre) - ord("0") + 1)
        elif 65 <= ord(lettre) <= 90:
            L.append(ord(lettre) - ord("A") + 11)
    return fraction(L)

# Fonction pour décrypter un message dans le format d'un IBAN
def decrypter_pour_IBAN(fraction):
    L = fraction_continue(*fraction)
    message = ""
    # Conversion des valeurs numériques en caractères selon le standard IBAN
    for nombre in L:
        if 1 <= nombre <= 10:
            message += str(nombre - 1)
        elif 11 <= nombre <= 36:
            message += chr(ord("A") + nombre - 11)
    return message

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour l'encryptage d'un message
@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    message = data['message']
    # Vérification de la structure de l'IBAN avant encryptage
    if verifier_structure_IBAN(message):
        encrypted_fraction = encrypter_pour_IBAN(message)
        return jsonify({'encrypted_fraction': encrypted_fraction})
    else:
        return jsonify({'error': 'Structure IBAN invalide.'}), 400

# Route pour le décryptage d'une fraction continue
@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    fraction_text = data['fraction']
    fraction = [int(part) for part in fraction_text.split('/')]
    decrypted_message = decrypter_pour_IBAN(fraction)
    return jsonify({'decrypted_message': decrypted_message})

# Point d'entrée de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
