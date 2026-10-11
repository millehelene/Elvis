import random

class Minispill:
    """Superklasse for alle minispill."""

    def __init__(self, navn, beskrivelse):
        self._navn = navn
        self._beskrivelse = beskrivelse
        self._fullfort = False

    def hent_navn(self):
        return self._navn

    def er_fullfort(self):
        return self._fullfort

    def spill(self, elvis):
        # Hver subklasse lager sin egen versjon av denne
        print("Dette minispillet er ikke laget ennå.")

    def __init__(self, navn, beskrivelse):
        self._navn = navn
        self._beskrivelse = beskrivelse
        self._fullfort = False
        self._tegning = ""

    def sett_tegning(self, tegning):
        self._tegning = tegning

    def hent_tegning(self):
        return self._tegning


class Gaate(Minispill):

    def __init__(self, navn, beskrivelse, sporsmal, godkjente_svar, belonning):
        super().__init__(navn, beskrivelse)
        self._sporsmal = sporsmal
        self._godkjente_svar = godkjente_svar   # liste med svar som regnes som riktige
        self._belonning = belonning

    def spill(self, elvis):
        print(self._beskrivelse)
        print(f'\n"{self._sporsmal}"\n')

        forsok = 3
        while forsok > 0:
            svar = input("Svar: ").lower().strip()
            if svar in self._godkjente_svar:
                print("\nStatuen smiler sakte. «Riktig, lille katt.»")
                elvis.hent_sted().legg_til_gjenstand(self._belonning)
                print(f"Den legger {self._belonning.hent_navn()} ved potene til Elvis.")
                self._fullfort = True
                return

            forsok -= 1
            if forsok > 0:
                print(f"«Feil.» ({forsok} forsøk igjen)")

        print("\nStatuen stivner igjen. Kanskje Elvis kan prøve senere.")


class KloHaleMjau(Minispill):

    SLAR = {"klo": "hale", "hale": "mjau", "mjau": "klo"}

    FORKLARING = {
        ("klo", "hale"): "Klo griper hale!",
        ("hale", "mjau"): "Halen dasker til trynet og stopper mjauet!",
        ("mjau", "klo"): "Det høye mjauet skremmer kloa tilbake!",
    }

    def __init__(self, navn, beskrivelse, motstander, belonning):
        super().__init__(navn, beskrivelse)
        self._motstander = motstander
        self._belonning = belonning

    def spill(self, elvis):
        print(self._beskrivelse)
        print("\nRegler: klo slår hale, hale slår mjau, mjau slår klo.")
        print("Førstemann til 2 poeng vinner!")

        elvis_poeng = 0
        motstander_poeng = 0

        while elvis_poeng < 2 and motstander_poeng < 2:
            valg = input("\nKlo, hale eller mjau? > ").lower().strip()
            if valg not in self.SLAR:
                print("Skriv 'klo', 'hale' eller 'mjau'.")
                continue

            motstander_valg = random.choice(list(self.SLAR))
            print(f"Elvis: {valg}  |  {self._motstander}: {motstander_valg}")

            if valg == motstander_valg:
                print("Uavgjort! Begge kattene stirrer på hverandre.")
            elif self.SLAR[valg] == motstander_valg:
                print(f"{self.FORKLARING[(valg, motstander_valg)]} Elvis vinner runden!")
                elvis_poeng += 1
            else:
                print(f"{self.FORKLARING[(motstander_valg, valg)]} {self._motstander} vinner runden!")
                motstander_poeng += 1

            print(f"Stilling: Elvis {elvis_poeng} - {motstander_poeng} {self._motstander}")

        if elvis_poeng == 2:
            print(f"\n{self._motstander} bukker anerkjennende. «Du er god, du.»")
            elvis.hent_sted().legg_til_gjenstand(self._belonning)
            print(f"{self._motstander} skyver {self._belonning.hent_navn()} bort til Elvis.")
            self._fullfort = True
        else:
            print(f"\n{self._motstander} maler fornøyd. «Kom tilbake når du har øvd litt!»")