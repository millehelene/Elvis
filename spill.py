from sted import Sted
from gjenstand import Gjenstand
from katt import Katt
import random
from fiende import Fiende
from hendelse import Hendelse, HelbredHendelse, SkadeHendelse, GjenstandHendelse, TyveriHendelse
from minispill import Gaate
from minispill import Gaate, KloHaleMjau
from figur import Selger

HENDELSE_SJANSE = 0.2   # 20 % sjanse hver gang Elvis kommer til et nytt sted

TITTEL = r"""
 _____   _      __     __  ___   ____
| ____| | |     \ \   / / |_ _| / ___|
|  _|   | |      \ \ / /   | |  \___ \
| |___  | |___    \ V /    | |   ___) |
|_____| |_____|    \_/    |___| |____/

              /\_/\
             ( o.o )
              > ^ <

    ~ en katt på villspor i Oslo ~
"""
MOTSATT = {"nord": "sør", "sør": "nord", "øst": "vest", "vest": "øst"}

MAAKE_TEGNING = r"""

                   /^v^\
         /^v^\                      /^v^\
                /^v^\

       /^v^\
       
"""

KRAAKE_TEGNING = r"""
              __
             /'{>
         ____) (____
       //'--;   ;--'\\
      ///////\_/\\\\\\\
             m m
"""

BIKKJE_TEGNING = r"""
        __      _
        \.'---.//|
         |\./|  \/
        _|.|.|_  \
       /(  ) ' '  \
      |  \/   . |  \
       \_/\__/| |    
        V  /V / |
          /__/ /
          \___/\.    VOFF!

"""

MJAUCIFER_TEGNING = r"""
                 __        .-.
             .-"` .`'.    /\\|
     _(\-/)_" ,  .   ,\  /\\\/
    {(#b^d#)} .   ./,  |/\\\/
    `-.(Y).-`  ,  |  , |\.-`
         /~/,_/~~~\,__.-`
        ////~    // ~\\
      ==`==`   ==`   ==`
     
     ~ M J A U C I F E R ~
"""

SEIER_TEGNING = r"""
        /\_/\
       ( ^.^ )    HJEMME!
        > ^ <
       /     \
      (  | |  )
     (___|_|___)~~
"""

ROTTE_TEGNING = r"""

       (`-()_.-=-.
       /66  ,  ,  \
     =(o_/=//_(   /======`
         ~"` ~"~~`

"""

KART = """
                                             Birkelunden
                                                  |
                                             Grünerløkka
                                                  |
                Majorstuen    Youngstorget    Akerselva
                     |              |             |
Frognerparken---Slottsparken---Karl Johan---Jernbanetorget---Grønland---Tøyen
                     |              |             |              |
                Aker Brygge   Rådhusplassen    Operaen   Middelalderparken
                                                  |
                                               Sørenga
"""

STATUE_TEGNING = r"""
            .---.
           ( o o )
            \ ~ /
          .-'---'-.
         /|       |\
        / |       | \
          |       |
          |   |   |
          |   |   |
         _|___|___|_
        |           |
        |  ~ ? ~ ?  |
        |___________|
"""

RASKUS_TEGNING = r"""
       /\_/\       Klo, hale
      ( o.O )      eller mjau?
      (> ^ <)
      /  _  \
     (  (_)  )~~~
      ""   ""
"""


BENNI_TEGNING = r"""
      _________________________
     |       BENNIS BOD        |
     |_________________________|
      \/\/\/\/\/\/\/\/\/\/\/\/\/
      |         .---.         |
      |        ( ^ ^ )        |
      |         \ v /         |
      |       __/   \__       |
    __|______/_______\_______|__
   |  (o)(o)    ~~~~    (@)(@)  |
   |____________________________|
"""


class Spill:

    def __init__(self):
        self._hjem = None
        startsted = self._lag_kart()
        self._elvis = Katt("Elvis", startsted)
        self._ferdig = False
        self._hendelser = self._lag_hendelser()

    # --- Bygg kartet ---

    def _lag_kart(self):
        jernbanetorget = Sted("Jernbanetorget",
            "Folk haster forbi, trikker ringer og en tigerstatue glor på deg.")
        karl_johan = Sted("Karl Johan",
            "En lang gate full av folk og butikker. Det lukter vafler og ferdigtygga tyggegummi.")
        operaen = Sted("Operaen",
            "Et gigantisk hvitt bygg som holder på falle i vannet. Noen spiller på en ødelagt kassegitar.")
        akerselva = Sted("Akerselva",
            "Elva bruser forbi. Langs bredden kryr det av ender og søplete søppel.")
        grunerlokka = Sted("Grünerløkka",
            "Det lukter svidd kaffe. Folk med for store briller tar bilder av seg sjæl. Noen griller i parken.")
        slottsparken = Sted("Slottsparken",
            "Svære trær og masse gress. Vaktene står stille som statuer.")
        frognerparken = Sted("Frognerparken",
            "Drøssevis av steinstatuer, det ser ut som noen av dem stirrer på Elvis.")
        majorstuen = Sted("Majorstuen",
            "Et travelt kryss med T-bane, trikk og mange skynde-seg-mennesker.")
        aker_brygge = Sted("Aker Brygge",
            "Restauranter og snublete mennsker. Det lukter reker og saltvann.")
        sorenga = Sted("Sørenga",
            "Bølgene bruser. Alle soler seg. Ingen bader")
        gronland = Sted("Grønland",
            "Ananas, kanel, godteri pakka inn i for mye plast og masse bein som tramper.")
        toyen = Sted("Tøyen",
            "Grønt og skjønt. Pass opp, trikker suser forbi!")
        birkelunden = Sted("Birkelunden",
            "En liten park med mange trær. Elvis kjenner igjen lukten. Han er hjemme!")
        youngstorget = Sted("Youngstorget",
            "Et åpent torg med blomsterboder og folk som sitter på uteserveringer.")
        radhusplassen = Sted("Rådhusplassen",
            "En stor plass foran det brune Rådhuset. Klokkene ringer over hele byen.")
        middelalderparken = Sted("Middelalderparken",
            "Gamle ruiner, små dammer og grønne plener. Det er stille og litt mystisk her.")
        self._hjem = birkelunden

        # Vestover fra sentrum
        self._koble(jernbanetorget, "vest", karl_johan)
        self._koble(karl_johan, "vest", slottsparken)
        self._koble(slottsparken, "vest", frognerparken)
        self._koble(slottsparken, "nord", majorstuen)
        self._koble(slottsparken, "sør", aker_brygge)

        # Sørover ved sjøen
        self._koble(jernbanetorget, "sør", operaen)
        self._koble(operaen, "sør", sorenga)

        # Østover
        self._koble(jernbanetorget, "øst", gronland)
        self._koble(gronland, "øst", toyen)

        # Nordover langs elva og hjem
        self._koble(jernbanetorget, "nord", akerselva)
        self._koble(akerselva, "nord", grunerlokka)
        self._koble(grunerlokka, "nord", birkelunden)
        
        # Nye steder
        self._koble(karl_johan, "nord", youngstorget)
        self._koble(karl_johan, "sør", radhusplassen)
        self._koble(gronland, "sør", middelalderparken)

        # Gjenstander
        nokkel = Gjenstand("nøkkel", "En liten messingnøkkel. Den lukter hjemme!", "nøkkel")
        karl_johan.legg_til_gjenstand(
            Gjenstand("fiskebolle", "En litt kald fiskebolle.", "mat", 20))
        operaen.legg_til_gjenstand(
            Gjenstand("laks", "En fersk laksebit!", "boost", 25))
        akerselva.legg_til_gjenstand(
            Gjenstand("kebabspyd", "Et spisst trespyd.", "våpen", 5))
        akerselva.legg_til_gjenstand(
            Gjenstand("flaskekork", "En blank kork. Helt ubrukelig, men fin."))
        toyen.legg_til_gjenstand(
            Gjenstand("kattemynte", "En dusk kattemynte fra Botanisk hage. Elvis blir helt ør!", "boost", 25))
        aker_brygge.legg_til_gjenstand(
            Gjenstand("rekesmørbrød", "Et rekesmørbrød noen har glemt på en benk.", "mat", 25))
        majorstuen.legg_til_gjenstand(
            Gjenstand("strikkepinne", "En lang, spiss strikkepinne. Perfekt til å fekte med!", "våpen", 8))
        sorenga.legg_til_gjenstand(
            Gjenstand("makrell", "En åpen boks makrell i tomat. Elvis blir sterk bare av lukten!", "boost", 25))
        
        frognerparken.legg_til_gjenstand(nokkel)
        # grunerlokka.legg_til_gjenstand(nokkel)
        
        # Fiender
        rotte = Fiende("rotta", "En stor, grå rotte med gule tenner.",
                       hp=30, skade=8, blokkert_retning="nord",
                       belonning=Gjenstand("pølsebit", "En halvspist grillpølse.", "mat", 15),
                       tegning=ROTTE_TEGNING)
        akerselva.sett_fiende(rotte) 
        
        maake = Fiende("måka", "En stor, grådig måke med et sultent blikk.",
                       hp=25, skade=6, blokkert_retning="sør",
                       belonning=Gjenstand("pommes frites", "En pose kalde pommes frites.", "mat", 10),
                       tegning=MAAKE_TEGNING)
        operaen.sett_fiende(maake)

        kraake = Fiende("kråka", "En svart kråke med skarpt nebb. Den har sett deg lenge.",
                        hp=35, skade=9, blokkert_retning="øst",
                        belonning=Gjenstand("blank mynt", "En skinnende mynt. Kråka har passet godt på den."),
                        tegning=KRAAKE_TEGNING)
        gronland.sett_fiende(kraake)

        bikkje = Fiende("bikkja", "En stor, sint bikkje uten bånd. Den har ikke sett en katt den liker.",
                        hp=50, skade=12, blokkert_retning="vest",
                        belonning=Gjenstand("hundekjeks", "En hundekjeks. Ikke Elvis sin favoritt, men det er mat.", "mat", 15),
                        tegning=BIKKJE_TEGNING)
        slottsparken.sett_fiende(bikkje)

        mjaucifer = Fiende("Mjaucifer",
                           "Nabolagets mest fryktede katt. Svart pels, ett øre med hakk i, "
                           "og han har tatt over hele Grünerløkka mens Elvis var borte.",
                           hp=100, skade=20, blokkert_retning="nord",
                           tegning=MJAUCIFER_TEGNING)
        grunerlokka.sett_fiende(mjaucifer)
        
        # låste utganger
        grunerlokka.laas_utgang("nord", "nøkkel")

        # minispill
        gaate = Gaate("Statuens gåte",
                      "En av steinstatuene snur plutselig hodet og ser ned på Elvis.\n"
                      "«Svar riktig på gåten min, så skal du få en gave.»",
                      "Jo mer du tar av meg, jo mer legger du igjen bak deg. Hva er jeg?",
                      ["fotspor", "fotsporene", "spor", "skritt"],
                      Gjenstand("potesalve", "En liten krukke potesalve. Lukter mynte.", "mat", 30))
        frognerparken.sett_minispill(gaate)
        gaate.sett_tegning(STATUE_TEGNING)

        klo_hale_mjau = KloHaleMjau("Klo, hale, mjau",
            "En lubben, oransje gatekatt hopper ned fra en blomsterkasse.\n"
            "«Du ser ut som en som liker et spill. Klo, hale, mjau?»",
            "Raskus",
            Gjenstand("kyllingvinge", "En sprø kyllingvinge fra en uteservering.", "mat", 20))
        youngstorget.sett_minispill(klo_hale_mjau)
        klo_hale_mjau.sett_tegning(RASKUS_TEGNING)

        
        # selgere
        selger = Selger("selgeren Benni",
                        "Hei, lille pus! Jeg tar ikke penger, men jeg elsker blanke ting.",
                        [
                            (Gjenstand("kattemynte", "En stor dusk fersk kattemynte!", "boost", 25), "blank mynt"),
                            (Gjenstand("tørrfisk", "En bit tørket torsk. Seig, men god.", "mat", 20), "flaskekork"),
                        ])
        gronland.sett_figur(selger)
        selger.sett_tegning(BENNI_TEGNING)

        return jernbanetorget

    # --- Hovedløkka ---

    def start(self):
        print(TITTEL)
        print("Ånei, Elvis har gått seg vill i Oslo! Kan du hjelpe han med å finne veien hjem?")
        print("Skriv 'hjelp' for å se alt Elvis kan gjøre.\n")

        valg = input("Trykk Enter for å starte... ")
        if valg.lower() == "hjelp":
            self._vis_hjelp()
            input("\nTrykk Enter for å starte...")
        print()


        print(self._elvis.hent_sted().beskriv())

        while not self._ferdig:
            kommando = input("\n> ")
            self._utfor_kommando(kommando)

        print("Takk for at du spilte!")

    def _snakk(self):
        figur = self._elvis.hent_sted().hent_figur()
        if figur is None:
            print("Det er ingen å snakke med her.")
        else:
            if figur.hent_tegning() != "":
                print(figur.hent_tegning())
            figur.snakk(self._elvis)
    
    def _vis_kart(self):
        her = self._elvis.hent_sted().hent_navn()
        kart = KART.replace(her, her.upper())
        print(kart)
        print(f"Elvis er her: {her.upper()}")
    
    # --- Tolk kommandoer ---

    def _utfor_kommando(self, kommando):
        ord = kommando.lower().split()
        if len(ord) == 0:
            return

        verb = ord[0]
        objekt = " ".join(ord[1:])   # resten av ordene, f.eks. "fiskebolle"

        if verb == "gå":
            self._gaa(objekt)
        elif verb == "se":
            print(self._elvis.hent_sted().beskriv())
        elif verb == "ta":
            print(self._elvis.ta(objekt))
        elif verb == "slipp":
            print(self._elvis.slipp(objekt))
        elif verb == "spis":
            print(self._elvis.spis(objekt))
        elif verb == "inventar":
            print(self._elvis.vis_inventar())
        elif verb == "status":
            print(f"HP: {self._elvis.hent_hp()}/{self._elvis.hent_maks_hp()}")
        elif verb == "hjelp":
            self._vis_hjelp()
        elif verb == "avslutt":
            self._ferdig = True
        elif verb == "angrip":
            self._kamp()
        elif verb == "kart":
            self._vis_kart()
        elif verb == "spill":
            self._spill_minispill()
        elif verb == "snakk":
            self._snakk()
        else:
            print("Elvis forstår ikke hva du mener. Skriv 'hjelp'.")

    def _gaa(self, retning):
        if retning == "":
            print("Gå hvor? F.eks. 'gå nord'.")
            return

        sted = self._elvis.hent_sted()

        fiende = sted.hent_fiende()
        if fiende is not None and fiende.hent_blokkert_retning() == retning:
            print(f"{fiende.hent_navn().capitalize()} står i veien! "
                  f"Elvis må angripe eller gå en annen vei.")
            return

        nokkel = sted.hent_nokkel_for(retning)
        if nokkel is not None and not self._elvis.har_gjenstand(nokkel):
            print("Porten er låst. Elvis trenger en nøkkel for å komme videre.")
            return

        if self._elvis.gaa(retning):
            nytt_sted = self._elvis.hent_sted()
            if nytt_sted == self._hjem:
                self._seier()
            else:
                print(nytt_sted.beskriv())
                if nytt_sted.hent_fiende() is None:
                    self._kanskje_hendelse()
        else:
            print("Elvis kan ikke gå den veien.")

    def _spill_minispill(self):
        minispill = self._elvis.hent_sted().hent_minispill()
        if minispill is None:
            print("Det er ikke noe å spille her.")
        elif minispill.er_fullfort():
            print("Elvis har allerede klart dette minispillet.")
        else:
            if minispill.hent_tegning() != "":
                print(minispill.hent_tegning())
            minispill.spill(self._elvis)
    
    def _kamp(self):
        sted = self._elvis.hent_sted()
        fiende = sted.hent_fiende()
        if fiende is None:
            print("Det er ingen å angripe her.")
            return

        print(f"\nElvis går til angrep på {fiende.hent_navn()}!")
        print(fiende.hent_beskrivelse())

        while True:
            print(f"\nElvis: {self._elvis.hent_hp()}/{self._elvis.hent_maks_hp()} HP"
                  f"  |  {fiende.hent_navn().capitalize()}: {fiende.hent_hp()} HP")
            valg = input("Angrip, spis <ting> eller flykt? > ").lower().split()
            if len(valg) == 0:
                continue

            if valg[0] == "angrip":
                skade = self._elvis.beregn_skade()
                fiende.ta_skade(skade)
                print(f"Elvis klorer {fiende.hent_navn()} og gjør {skade} skade!")

                if not fiende.lever():
                    print(f"{fiende.hent_navn().capitalize()} flykter vekk!")
                    sted.fjern_fiende()
                    belonning = fiende.hent_belonning()
                    if belonning is not None:
                        sted.legg_til_gjenstand(belonning)
                        print(f"Den mistet noe: {belonning.hent_navn()}!")
                    return

                if not self._fiende_angriper(fiende):
                    return

            elif valg[0] == "spis":
                ting = " ".join(valg[1:])
                if not self._elvis.har_gjenstand(ting):
                    print(f"Elvis har ingen {ting} i ryggsekken.")
                    continue
                print(self._elvis.spis(ting))
                if not self._fiende_angriper(fiende):
                    return

            elif valg[0] == "flykt":
                if random.random() < 0.5:
                    skade = fiende.beregn_skade()
                    self._elvis.ta_skade(skade)
                    print(f"{fiende.hent_navn().capitalize()} biter Elvis i halen "
                          f"mens han flykter! (-{skade} HP)")
                    if not self._elvis.lever():
                        self._game_over()
                        return
                else:
                    print("Elvis kommer seg unna uten en skramme!")

                if self._elvis.gaa_tilbake():
                    print(self._elvis.hent_sted().beskriv())
                return

            else:
                print("Skriv 'angrip', 'spis <ting>' eller 'flykt'.")

    def _fiende_angriper(self, fiende):
        skade = fiende.beregn_skade()
        self._elvis.ta_skade(skade)
        print(f"{fiende.hent_navn().capitalize()} angriper Elvis og gjør {skade} skade!")
        if not self._elvis.lever():
            self._game_over()
            return False
        return True

    def _koble(self, sted1, retning, sted2):
        sted1.legg_til_utgang(retning, sted2)
        sted2.legg_til_utgang(MOTSATT[retning], sted1)

    def _lag_hendelser(self):
        return [
            HelbredHendelse("Et lite barn klør Elvis bak øret. Akkurat det han trengte!", 10),
            HelbredHendelse("Elvis finner en solflekk på asfalten og tar en liten lur.", 15),
            SkadeHendelse("Plutselig styrtregn! Elvis blir søkkvåt og mjauer surt.", 5),
            SkadeHendelse("En sparkesykkel suser forbi og streifer halen til Elvis. Au!", 8),
            GjenstandHendelse("En turist mister en vaffel rett foran Elvis.",
                              "vaffel", "En varm vaffel med syltetøy.", "mat", 15),
            GjenstandHendelse("Under en benk ligger det en glemt boks.",
                              "sardiner", "En boks sardiner. Elvis sin drøm!", "mat", 20),
            TyveriHendelse("En frekk due dykker ned mot ryggsekken!"),
            Hendelse("En trikk ringer rett bak Elvis. Han skvetter en meter opp i lufta, men lander så klart på beina!"),
            Hendelse("En gatemusikant spiller saksofon. Elvis setter seg ned og lytter en stund."),
        ]

    def _kanskje_hendelse(self):
        if random.random() < HENDELSE_SJANSE:
            hendelse = random.choice(self._hendelser)
            print("\n*** " + hendelse.utfor(self._elvis) + " ***")


    def _seier(self):
        print(SEIER_TEGNING)
        print("Elvis låser opp porten og smyger seg inn.")
        print("Han kjenner igjen hver eneste busk og benk. Fra et vindu i nærheten")
        print("roper noen navnet hans, og det lukter middag.")
        print("\nElvis er endelig hjemme!")
        print(f"\nHan kom hjem med {self._elvis.hent_hp()}/{self._elvis.hent_maks_hp()} HP.")
        print("\nGRATULERER, DU FIKK ELVIS HJEM IGJEN!")
        self._ferdig = True

    def _game_over(self):
        print("\nElvis orker ikke mer og legger seg ned på fortauet...")
        print("GAME OVER")
        self._ferdig = True

    def _vis_hjelp(self):
        print("Kommandoer:")
        print("  gå <retning>   - gå nord, sør, øst eller vest")
        print("  se             - se deg rundt")
        print("  kart           - se kart over Oslo")
        print("  ta <ting>      - plukk opp noe")
        print("  slipp <ting>   - legg fra deg noe")
        print("  spis <ting>    - spis noe fra ryggsekken")
        print("  inventar       - se hva Elvis har i ryggsekken")
        print("  angrip         - angrip fiende")
        print("  spill          - prøv et minispill, hvis det finnes her")
        print("  snakk          - snakk med noen (hvis det står noen her)")
        print("  status         - se livet til Elvis")
        print("  avslutt        - avslutt spillet")