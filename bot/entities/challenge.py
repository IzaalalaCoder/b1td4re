import datetime as d
import xml.etree.ElementTree as ET

class Challenge():
    def _get_correct_file_on_today(self):
        date = d.date.today()
        month = date.strftime("%B").lower()
        year = date.year
        return ET.parse(f'bot/assets/{month}/{year}.xml')

    def _read_challenge(self, challenge):
        titre = challenge.find("titre").text
        explication = challenge.find("explication").text
        description = challenge.find("description").text
        text = f"Titre: {titre}\nExplication: {explication}\nDescription: {description} \nCritères de succès:"
        for critere in challenge.findall(".//criteres_succes/critere"):
            text += f"\n- {critere.text}"
        return text

    def get_all_challenges_on_day(self):
        root = self._get_correct_file_on_today().getroot()
        day = d.date.today().day
        challenge = root.find(f".//challenge[@jour='{day}']")
        if challenge is not None:
            return self._read_challenge(challenge)
        else:
            return "Le challenge pour le jour spécifié n'a pas été trouvé."

    def get_one_challenge_on_day(self, index : int):
        root = self._get_correct_file_on_today().getroot()
        day = d.date.today().day
        challenge = root.find(f".//challenge[@jour='{day}'][@index='{index}']")
        if challenge is not None:
            return self._read_challenge(challenge)
        else:
            return f"Le challenge pour le jour numéro {index} spécifié n'a pas été trouvé."