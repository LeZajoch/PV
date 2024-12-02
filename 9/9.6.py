class GeneratorKrasovychJezer():
    i = 0
    j = 0

    jezera = [
        # "Křivé jezero (Dyje)",
        # "Květné jezero (Dyje)",
        # "Kutnar (Dyje)",
        # "Mahenovo jezero (Dyje)",
        # "Babinecká tůň (Labe)",
        # "Hrbáčkovy tůně (Labe)",
        # "Komořanské jezero (Bílina - zaniklo 1831)",
        # "Antošovické jezero",
        # "Holásecká jezera",
        # "Krňák",
        # "Kurfürstovo rameno",
        # "Malá říčka",
        # "Podhradská tůň",
        ["Dyje", ["Křivé jezero", "Květné jezero", "Kutnar", "Mahenovo jezero"]],
        ["Labe", ["Babinecká tůň", "Hrbáčkovy tůně"]],
        ["Bílina", ["Komořanské jezero"]],
        ["(bez řeky)",
         ["Antošovické jezero", "Holásecká jezera", "Krňák", "Kurfürstovo rameno", "Malá říčka", "Podhradská tůň"]]
    ]

    def __iter__(self):
        self.i = 0;
        self.j = 0;
        return self

    def __next__(self):
        if self.i > (len(self.jezera) - 1):
            raise StopIteration()

        reka = self.jezera[self.i][0]
        jezeraNaRece = self.jezera[self.i][1]

        if self.j > (len(jezeraNaRece) - 1):
            self.j = 0;
            self.i = self.i + 1;

        pomocnaPromenna = jezeraNaRece[self.j]
        if (reka != "(bez řeky)"):
            pomocnaPromenna += " (" + reka + ")"
        self.j = self.j + 1;
        return pomocnaPromenna


for jezero in GeneratorKrasovychJezer():
    print(jezero)


