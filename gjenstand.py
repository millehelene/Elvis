class Gjenstand:

    def __init__(self, navn, beskrivelse, type="vanlig", verdi=0):
        self._navn = navn
        self._beskrivelse = beskrivelse
        self._type = type      # "mat", "våpen", "nøkkel" eller "vanlig"
        self._verdi = verdi    # hvor mye mat helbreder, eller hvor mye våpen gir i skade

    def hent_navn(self):
        return self._navn

    def hent_beskrivelse(self):
        return self._beskrivelse

    def hent_type(self):
        return self._type

    def hent_verdi(self):
        return self._verdi

    def er_mat(self):
        return self._type == "mat"

    def er_vaapen(self):
        return self._type == "våpen"

    def __str__(self):
        return f"{self._navn}: {self._beskrivelse}"

    def er_boost(self):
        return self._type == "boost"