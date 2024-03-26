// Fonction pour simuler un clic sur le lien "Accueil"
window.onload = function() {
    document.querySelector('.menu li a[href="#home"]').click();
};

// Fonction pour convertir une chaîne de caractères en liste de nombres
function convertirChaineEnListe(inputString) {
    var listeResultat = [];

    for (var i = 0; i < inputString.length; i++) {  
        var codeChar = inputString.charCodeAt(i);

        // Gestion des lettres minuscules (a: 1, b: 2, ..., z: 26)
        if (codeChar >= 97 && codeChar <= 122) {
            listeResultat.push(codeChar - 96); 
        }
        // Gestion des lettres majuscules (A: 27, B: 28, ..., Z: 52)
        else if (codeChar >= 65 && codeChar <= 90) {
            listeResultat.push(codeChar - 64 + 26); 
        }
        // Gestion des nombres (0: 53, 1: 54, ..., 9: 62)
        else if (codeChar >= 48 && codeChar <= 57) {
            listeResultat.push(codeChar - 21); 
        }
        // Gestion de l'espace
        else if (codeChar === 32) {
            listeResultat.push(63); 
        }
        // Gestion du point (.)
        else if (codeChar === 46) {
            listeResultat.push(64); 
        }
    }
    return listeResultat;
}

// Fonction pour calculer la fraction à partir d'une liste de nombres
function calculerFraction(nombreListe) {
    if (!Array.isArray(nombreListe) || nombreListe.length === 0) {
        return 'Entrée invalide';
    }

    var numerateur = bigInt(nombreListe[nombreListe.length - 1]);
    var denominateur = bigInt(1);

    for (var i = nombreListe.length - 2; i >= 0; i--) {
        var temp = numerateur;
        numerateur = bigInt(nombreListe[i]).times(numerateur).plus(denominateur);
        denominateur = temp;
    }

    return [numerateur.toString(), denominateur.toString()];
}

// Fonction pour créer la fraction continue à partir d'une liste de nombres
function creerFractionContinue(nombres) {
    if (!nombres || nombres.length === 0) {
        return 'Entrée invalide';
    }

    var nombresInverses = nombres.slice().reverse(); // Créer une copie et inverser l'ordre
    var fractionContinue = nombresInverses[0];

    for (var i = 1; i < nombresInverses.length; i++) {
        fractionContinue = `${nombresInverses[i]} + \\dfrac{1}{${fractionContinue}}`;
    }

    return fractionContinue;
}

// Fonction pour convertir et afficher la fraction continue et la fraction normale
function convertirEtAfficher() {
    var userInput = document.getElementById('userInput').value;
    var listeNombres = convertirChaineEnListe(userInput);
    
    // Calculer la fraction à partir de la liste de nombres
    var fraction = calculerFraction(listeNombres);
    // Créer la fraction continue à partir de la liste de nombres
    var fractionContinue = 'Fraction Continue: \\[' + creerFractionContinue(listeNombres) + '\\]';
    
    // Afficher à la fois la fraction continue et la fraction normale
    var resultHtml = fractionContinue + '<br>' + 'Fraction Normale: ' + fraction[0] + '/' + fraction[1] + '<br>';
    
    // Ajouter un bouton Copy à côté de la fraction normale
    resultHtml += '<button class="btn btn-ramanujan" onclick="copyFraction()">Copier</button>';

    document.getElementById('result').innerHTML = resultHtml;
    
    // Utiliser MathJax pour rendre le LaTeX
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, "result"]);
}

// Fonction pour copier la fraction normale a/b dans le presse-papiers
function copyFraction() {
    var fractionText = document.getElementById('result').textContent;
    var fractionNormale = fractionText.match(/\d+\/\d+/); // Extraction de la fraction normale a/b
    if (fractionNormale) {
        fractionNormale = fractionNormale[0];
        navigator.clipboard.writeText(fractionNormale).then(function() {
            alert('Fraction copiée dans le presse-papiers : ' + fractionNormale);
        }, function(err) {
            console.error('Erreur lors de la copie de la fraction normale a/b : ', err);
        });
    } else {
        console.error('La fraction normale a/b n\'a pas été trouvée dans le contenu.');
    }
}

// Fonction pour décrypter la fraction normale en chaîne de caractères
function calculer() {
    var fraction = document.getElementById("fractionInput").value;
    var nombres = [];

    var parties = fraction.split('/');
    var dividende = BigInt(parties[0]);
    var diviseur = BigInt(parties[1]);

    while (diviseur !== 0n) {
        var quotient = dividende / diviseur;
        quotient = quotient > 0n ? quotient : -(-quotient + 1n);
        var reste = dividende % diviseur;
        nombres.push(quotient);
        dividende = diviseur;
        diviseur = reste;
    }

    var resultat = nombres.map(function(nombre) {
        if (nombre >= 1n && nombre <= 26n) {
            return String.fromCharCode(Number(nombre) + 96); // a=1, b=2, ..., z=26
        } else if (nombre >= 27n && nombre <= 52n) {
            return String.fromCharCode(Number(nombre) + 38); // A=27, B=28, ..., Z=52
        } else if (nombre === 0n) {
            return " "; // Espace
        } else if (nombre === 63n) {
            return " "; // Espace pour 63
        } else {
            return ""; // Ignorer les autres nombres
        }
    }).join("");

    document.getElementById("output").textContent = resultat;
}
