from gjenstand import Gjenstand


class Hendelse:
    """En hendelse som bare viser en tekst (stemning)."""

    def __init__(self, tekst):
        self._tekst = tekst

    def utfor(self, elvis):
        return self._tekst


class HelbredHendelse(Hendelse):

    def __init__(self, tekst, mengde):
        super().__init__(tekst)
        self._mengde = mengde

    def utfor(self, elvis):
        okning = elvis.helbred(self._mengde)
        return f"{self._tekst} (+{okning} HP)"


class SkadeHendelse(Hendelse):

    def __init__(self, tekst, mengde):
        super().__init__(tekst)
        self._mengde = mengde

    def utfor(self, elvis):
        # En hendelse skal aldri kunne drepe Elvis, så han beholder minst 1 HP
        skade = min(self._mengde, elvis.hent_hp() - 1)
        if skade <= 0:
            return self._tekst
        elvis.ta_skade(skade)
        return f"{self._tekst} (-{skade} HP)"


class GjenstandHendelse(Hendelse):

    def __init__(self, tekst, navn, beskrivelse, type="vanlig", verdi=0):
        super().__init__(tekst)
        self._navn = navn
        self._beskrivelse = beskrivelse
        self._type = type
        self._verdi = verdi

    def utfor(self, elvis):
        # Lager en ny gjenstand hver gang, så hendelsen kan skje flere ganger
        gjenstand = Gjenstand(self._navn, self._beskrivelse, self._type, self._verdi)
        if elvis.legg_i_ryggsekk(gjenstand):
            return f"{self._tekst} Elvis putter {self._navn} i ryggsekken."
        return f"{self._tekst} Men ryggsekken er full, så Elvis må la den ligge."


class TyveriHendelse(Hendelse):

    def utfor(self, elvis):
        gjenstand = elvis.mist_tilfeldig_gjenstand()
        if gjenstand is None:
            return f"{self._tekst} Men ryggsekken er tom, så den flyr skuffet videre."
        return f"{self._tekst} Den stakk av med {gjenstand.hent_navn()}!"