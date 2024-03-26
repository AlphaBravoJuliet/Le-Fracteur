# Importation des modules nécessaires depuis Flask
from flask import Flask, render_template, request, jsonify

# Création de l'application Flask
app = Flask(__name__)

# Fonction pour vérifier la structure d'un IBAN
def verifier_structure_IBAN(IBAN):
    IBAN = IBAN.replace(" ", "")  # Suppression des espaces
    if len(IBAN) < 15:  # Vérification de la longueur minimale de l'IBAN
        return False
    IBAN_numerique = ''
    # Conversion des caractères alphabétiques en valeurs numériques selon le standard IBAN
    for char in IBAN[4:] + IBAN[:4]:
        if char.isalpha():
            IBAN_numerique += str(ord(char.upper()) - 55)
        else:
            IBAN_numerique += char
    somme_controle = int(IBAN_numerique) % 97  # Calcul de la somme de contrôle
    if somme_controle != 1:  # Vérification de la validité de la somme de contrôle
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

# Fonction pour décrypter une fraction continue en message
def decrypter(fraction):
    L = fraction_continue(*fraction)
    # Conversion des valeurs numériques en caractères ASCII
    string = "".join([chr(nombre) for nombre in L])
    return string

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
