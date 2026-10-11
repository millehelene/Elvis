class Figur:
    """En figur Elvis kan snakke med."""

    def __init__(self, navn, replikk):
        self._navn = navn
        self._replikk = replikk

    def hent_navn(self):
        return self._navn

    def snakk(self, elvis):
        print(f"{self._navn}: «{self._replikk}»")

    def __init__(self, navn, replikk):
        self._navn = navn
        self._replikk = replikk
        self._tegning = ""

    def sett_tegning(self, tegning):
        self._tegning = tegning

    def hent_tegning(self):
        return self._tegning


class Selger(Figur):

    def __init__(self, navn, replikk, varer):
        super().__init__(navn, replikk)
        self._varer = varer   # liste med (gjenstand, navn på det den koster)

    def snakk(self, elvis):
        super().snakk(elvis)

        while len(self._varer) > 0:
            print("\nVarer:")
            for vare, pris in self._varer:
                print(f"  - {vare.hent_navn()}: koster én {pris}")

            valg = input("Hva vil Elvis bytte til seg? (eller 'ha det') > ").lower().strip()
            if valg == "ha det" or valg == "":
                print(f"{self._navn} vinker. «Kom gjerne tilbake!»")
                return

            funnet = None
            for vare_og_pris in self._varer:
                if vare_og_pris[0].hent_navn().lower() == valg:
                    funnet = vare_og_pris

            if funnet is None:
                print(f"{self._navn}: «Den har jeg ikke, dessverre.»")
                continue

            vare, pris = funnet
            if not elvis.har_gjenstand(pris):
                print(f"{self._navn}: «Den koster én {pris}, og det har du visst ikke.»")
                continue

            elvis.fjern_fra_ryggsekk(pris)
            elvis.legg_i_ryggsekk(vare)
            self._varer.remove(funnet)
            print(f"Elvis gir bort {pris} og får {vare.hent_navn()}!")

        print(f"{self._navn}: «Nå er jeg utsolgt! Takk for handelen.»")