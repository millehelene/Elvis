import random

MAKS_INVENTAR = 10
START_HP = 100
GRUNNSKADE = 10


class Katt:

    def __init__(self, navn, startsted):
        self._navn = navn
        self._sted = startsted
        self._inventar = []
        self._maks_hp = START_HP
        self._hp = START_HP
        self._grunnskade = GRUNNSKADE
        self._forrige_sted = None

    # --- Hent-metoder ---

    def hent_navn(self):
        return self._navn

    def hent_sted(self):
        return self._sted

    def hent_hp(self):
        return self._hp

    def hent_maks_hp(self):
        return self._maks_hp

    # --- Bevegelse ---

    def gaa(self, retning):
        nytt_sted = self._sted.hent_utgang(retning)
        if nytt_sted is None:
            return False
        self._forrige_sted = self._sted
        self._sted = nytt_sted
        return True

    def gaa_tilbake(self):
        if self._forrige_sted is None:
            return False
        self._sted, self._forrige_sted = self._forrige_sted, self._sted
        return True

    # --- Inventar ---

    def finn_i_inventar(self, navn):
        for gjenstand in self._inventar:
            if gjenstand.hent_navn().lower() == navn.lower():
                return gjenstand
        return None

    def har_gjenstand(self, navn):
        return self.finn_i_inventar(navn) is not None

    def ta(self, navn):
        gjenstand = self._sted.finn_gjenstand(navn)
        if gjenstand is None:
            return f"Det finnes ingen {navn} her."
        if len(self._inventar) >= MAKS_INVENTAR:
            return f"{self._navn} kan ikke bære mer! Slipp noe først."
        self._sted.fjern_gjenstand(gjenstand)
        self._inventar.append(gjenstand)
        return f"{self._navn} plukker opp {gjenstand.hent_navn()}."

    def slipp(self, navn):
        gjenstand = self.finn_i_inventar(navn)
        if gjenstand is None:
            return f"{self._navn} har ingen {navn}."
        self._inventar.remove(gjenstand)
        self._sted.legg_til_gjenstand(gjenstand)
        return f"{self._navn} slipper {gjenstand.hent_navn()}."

    def vis_inventar(self):
        if len(self._inventar) == 0:
            return f"{self._navn} bærer ingenting."
        tekst = f"Inventar ({len(self._inventar)}/{MAKS_INVENTAR}):\n"
        for gjenstand in self._inventar:
            tekst += f"  - {gjenstand}\n"
        return tekst

    # --- Mat ---

    def spis(self, navn):
        gjenstand = self.finn_i_inventar(navn)
        if gjenstand is None:
            return f"{self._navn} har ingen {navn}."

        if gjenstand.er_mat():
            gammel_hp = self._hp
            self._hp = min(self._hp + gjenstand.hent_verdi(), self._maks_hp)
            self._inventar.remove(gjenstand)
            okning = self._hp - gammel_hp
            return (f"{self._navn} spiser {gjenstand.hent_navn()} og får {okning} HP. "
                    f"({self._hp}/{self._maks_hp})")

        elif gjenstand.er_boost():
            self._maks_hp += gjenstand.hent_verdi()
            self._hp = self._maks_hp
            self._inventar.remove(gjenstand)
            return (f"Mmm! {self._navn} spiser {gjenstand.hent_navn()} og føler seg sterkere! "
                    f"Maks-HP er nå {self._maks_hp}, og helsa er fylt opp.")

        else:
            return f"{self._navn} snuser på {gjenstand.hent_navn()}, men det kan man ikke spise."

    # --- Kamp ---

    def beregn_skade(self):
        beste_vaapen = 0
        for gjenstand in self._inventar:
            if gjenstand.er_vaapen() and gjenstand.hent_verdi() > beste_vaapen:
                beste_vaapen = gjenstand.hent_verdi()
        return self._grunnskade + beste_vaapen + random.randint(-3, 3)

    def ta_skade(self, mengde):
        self._hp = max(self._hp - mengde, 0)

    def lever(self):
        return self._hp > 0


    # --- Henelser ---
    
    def helbred(self, mengde):
        gammel_hp = self._hp
        self._hp = min(self._hp + mengde, self._maks_hp)
        return self._hp - gammel_hp

    def legg_i_ryggsekk(self, gjenstand):
        if len(self._inventar) >= MAKS_INVENTAR:
            return False
        self._inventar.append(gjenstand)
        return True

    def mist_tilfeldig_gjenstand(self):
        kandidater = []
        for gjenstand in self._inventar:
            if gjenstand.hent_type() != "nøkkel":
                kandidater.append(gjenstand)
        if len(kandidater) == 0:
            return None
        gjenstand = random.choice(kandidater)
        self._inventar.remove(gjenstand)
        return gjenstand

    def fjern_fra_ryggsekk(self, navn):
        gjenstand = self.finn_i_inventar(navn)
        if gjenstand is not None:
            self._inventar.remove(gjenstand)
        return gjenstand