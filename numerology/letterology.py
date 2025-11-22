

class letterology(): 
    def __init__(self):
        
        self.full_letters = {"a" : 1, "b" : 2, "c" : 3, "d" : 4, "e" : 5, "f" : 6, "g" : 7, "h" : 8, "i" : 9, 
                            "j" : 10, "k" : 11, "l" : 12, "m" : 13, "n" : 14, "o" : 15, "p" : 16, "q" : 17, "r" : 18, 
                            "s" : 19, "t" : 20, "u" : 21, "v" : 22, "w" : 23, "x" : 24, "y" : 25, "z" : 26, "A" : 27,
                            "B" : 28, "C" : 29, "D" : 30, "E" : 31, "F" : 32, "G" : 33, "H" : 34, "I" : 35, "J" : 36, 
                            "K" : 37, "L" : 38, "M" : 39, "N" : 40, "O" : 41, "P" : 42, "Q" : 43, "R" : 44, "S" : 45, 
                            "T" : 46, "U" : 47, "V" : 48, "W" : 49, "X" : 50, "Y" : 51, "Z" : 52}

        self.reduced_letters = {"a" : 1, "b" : 2, "c" : 3, "d" : 4, "e" : 5, "f" : 6, "g" : 7, "h" : 8, "i" : 9, 
                                "j" : 1, "k" : 11, "l" : 3, "m" : 4, "n" : 5, "o" : 6, "p" : 7, "q" : 8, "r" : 9, 
                                "s" : 1, "t" : 2, "u" : 3, "v" : 22, "w" : 5, "x" : 6, "y" : 7, "z" : 8, "A" : 9, 
                                "B" : 1, "C" : 11, "D" : 3, "E" : 4, "F" : 5, "G" : 33, "H" : 7, "I" : 8, "J" : 9, 
                                "K" : 1, "L" : 11, "M" : 3, "N" : 4, "O" : 5, "P" : 6, "Q" : 7, "R" : 8, "S" : 9, 
                                "T" : 1, "U" : 11, "V" : 3, "W" : 4, "X" : 5, "Y" : 6, "Z" : 7,}

    def get_sum(self, word): 
        '''
        Convert Letters to Number
        word = Alphanumeric string
        '''

        word = [*word]

        full_sum = 0
        reduced_sum = 0
        for character in word:
            if character.isalpha():
                full_sum += self.full_letters[character]
                reduced_sum += self.reduced_letters[character]

            elif character.isnumeric():
                full_sum += int(character)
                reduced_sum += int(character)

            else: 
                # Character is neither letter or number. 
                continue
        
        return {"Full": full_sum, "Reduced": reduced_sum}

if __name__ == "__main__":
    while True:
        word = input("Enter word: ")

        if word == "":
            break

        print(letterology().get_sum(word))

        
