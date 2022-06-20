from numpy import True_
import math

class TicTac:
    """
    Klasa TicTac posiadająca metody: 
    Konstruktor główny inicjalizujący zmienne
    abc- sprawdzający ze sobą 3 pojedyńcze elementy 
    Sprawdz_wygrany - sprawdza możliwości wygrania poprzez metodę abc, która
    sprawdza 3 elementy w wierzach, kolumnach, bądź skosach
    Remis- metoda sprawdzająca czy zaszedł remis, czyli czy nie zapełniła się cała tablica 3x3
    """
    def __init__(self):
        self.k = 0
        self.tab33 = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
        self.ids =  ['a00', 'a01', 'a02',
        'a10', 'a11', 'a12',
        'a20', 'a21', 'a22']

    def abc(self, a, b, c):
        return a == b & b == c & a != 0

    def Sprawdz_wygrany(self):
        wygrany = None

        # Pionowo
        for i in range(0,3):
            if (self.abc(self.tab33[i][0], self.tab33[i][1], self.tab33[i][2])):
                wygrany = self.tab33[i][0]
            

        # Poziomo
        for i in range(0,3):
            if (self.abc(self.tab33[0][i], self.tab33[1][i], self.tab33[2][i])):
                wygrany = self.tab33[0][i]


        # Skosem
        if (self.abc(self.tab33[0][0], self.tab33[1][1], self.tab33[2][2])):
            wygrany = self.tab33[0][0]

        if (self.abc(self.tab33[2][0], self.tab33[1][1], self.tab33[0][2])):
            wygrany = self.tab33[2][0]

        if (wygrany == None):
            return 0
        else:
            return wygrany


    def Remis(self):
        for i in range(0,3):
            for j in range(0,3):
                if (self.tab33[i][j] == 0):
                    return False
        return True


