import xml.etree.ElementTree as ET

# Chargement du fichier XML
tree = ET.parse('bot/assets/april/2025.xml')  # Remplacer par le chemin de votre fichier XML
root = tree.getroot()

# Récupération des informations spécifiques
def get_challenge_details(root):
    # Trouver le challenge du jour 1 (ou autre jour selon votre besoin)
    challenge = root.find(".//challenge[@jour='1']")

    if challenge is not None:
        # Récupérer les informations spécifiques du challenge
        titre = challenge.find("titre").text
        explication = challenge.find("explication").text
        description = challenge.find("description").text

        # Récupérer les critères de succès
        criteres_succes = []
        for critere in challenge.findall(".//criteres_succes/critere"):
            criteres_succes.append(critere.text)

        # Affichage des résultats
        print("Titre:", titre)
        print("Explication:", explication)
        print("Description:", description)
        print("Critères de succès:")
        for critere in criteres_succes:
            print("-", critere)
    else:
        print("Le challenge pour le jour spécifié n'a pas été trouvé.")

# Appel de la fonction pour afficher les détails du challenge
get_challenge_details(root)
