import datetime as d
import xml.etree.ElementTree as ET

class Challenge():
    def _get_correct_file_on_today(self):
        date = d.date.today()
        month = date.strftime("%B").lower()
        year = date.year
        return ET.parse(f'bot/assets/{month}/{year}.xml')

    def _read_challenge(self, challenge):
        informations_challenge = {}
        informations_challenge["titre"] = challenge.find("titre").text
        informations_challenge["explication"] = challenge.find("explication").text
        informations_challenge["description"] = challenge.find("description").text

        if challenge.find("exemple_de_deroulement") is not None:
            informations_challenge["exemples"] = challenge.find("exemple_de_deroulement").text

        if challenge.find("criteres_succes") is not None:
            informations_challenge["criteres"] = ""
            for critere in challenge.findall(".//criteres_succes/critere"):
                informations_challenge["criteres"] += f"\n- {critere.text}"

        return informations_challenge

    def get_all_challenges_on_day(self):
        root = self._get_correct_file_on_today().getroot()
        day = d.date.today().day
        challenges_str = []
        challenges = root.findall(f".//challenge[@jour='{day}']")
        if challenges:
            for c in challenges:
                challenges_str.append(self._read_challenge(c))
            return challenges_str
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