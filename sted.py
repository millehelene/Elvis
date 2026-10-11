class Sted: 

    def __init__(self, navn, beskrivelse): 
        self._navn = navn
        self._beskrivelse = beskrivelse
        self._utganger = {}
        self._gjenstander = []
        self._fiende = None
        self._laaste_utganger = {}   # retning -> navn på nøkkelen som trengs
        self._minispill = None
        self._figur = None

    def hent_navn(self):
        return self._navn

    def legg_til_utgang(self, retning, sted):
        if retning not in self._utganger: 
            self._utganger[retning] = sted

    def hent_utgang(self, retning):
        if retning in self._utganger:
            return self._utganger[retning]
        return None

    def legg_til_gjenstand(self, gjenstand):
        self._gjenstander.append(gjenstand)

    def fjern_gjenstand(self, gjenstand):
        if gjenstand in self._gjenstander:
            self._gjenstander.remove(gjenstand)

    def beskriv(self):
        tekst = f"--- {self._navn} ---\n"
        tekst += self._beskrivelse + "\n"

        # Gjenstander på stedet
        if len(self._gjenstander) > 0:
            navneliste = []
            for gjenstand in self._gjenstander:
                navneliste.append(gjenstand.hent_navn())
            tekst += "Du ser: " + ", ".join(navneliste) + "\n"

        # Fiende på stedet
        if self._fiende is not None:
            if self._fiende.hent_tegning() != "":
                tekst += self._fiende.hent_tegning() + "\n"
            tekst += (f"Pass opp! {self._fiende.hent_navn().capitalize()} "
                      f"sperrer veien mot {self._fiende.hent_blokkert_retning()}!\n")

        if self._minispill is not None and not self._minispill.er_fullfort():
            tekst += f"Her kan Elvis spille: {self._minispill.hent_navn()} \n"

        # selgere
        if self._figur is not None:
            tekst += f"Her står {self._figur.hent_navn()}. (skriv 'snakk')\n"

        # Utganger
        if len(self._utganger) > 0:
            retninger = []
            for retning in self._utganger:
                retninger.append(retning)
            tekst += "Utganger: " + ", ".join(retninger)
        else:
            tekst += "Det finnes ingen utganger herfra."

        return tekst

    def sett_fiende(self, fiende):
        self._fiende = fiende

    def hent_fiende(self):
        return self._fiende

    def fjern_fiende(self):
        self._fiende = None

    def finn_gjenstand(self, navn):
        for gjenstand in self._gjenstander:
            if gjenstand.hent_navn().lower() == navn.lower():
                return gjenstand
        return None

    def laas_utgang(self, retning, nokkelnavn):
        self._laaste_utganger[retning] = nokkelnavn

    def hent_nokkel_for(self, retning):
        if retning in self._laaste_utganger:
            return self._laaste_utganger[retning]
        return None

    def sett_minispill(self, minispill):
        self._minispill = minispill

    def hent_minispill(self):
        return self._minispill

    def sett_figur(self, figur):
        self._figur = figur

    def hent_figur(self):
        return self._figur