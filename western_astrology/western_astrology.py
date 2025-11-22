import pandas as pd

class western_astrology:
    def __init__(self): 
        self.data = {'sign': ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'], 
                    'gloss': ['The Ram', 'The Bull', 'The Twins', 'The Crab', 'The Lion', 'The Maiden', 
                                'The Scales', 'The Scorpion', 'The Archer', 'The Goat', 'The Water-bearer', 'The Fish'], 
                    'start_date': ['March 21', 'April 20', 'May 21', 'June 21', 'July 23', 'August 23', 
                                    'September 23', 'October 23', 'November 22', 'December 22', 'January 20', 'February 19'], 
                    'end_date': ['April 19', 'May 20', 'June 20', 'July 22', 'August 22', 'September 22', 
                                'October 22', 'November 21', 'December 21', 'January 19', 'February 18', 'March 20'], 
                    'house': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
                    'element': ['Fire', 'Earth', 'Air', 'Water', 'Fire', 'Earth', 'Air', 'Water', 'Fire', 'Earth', 'Air', 'Water'], 
                    'Ruler': ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']}
        
        self.df = pd.DataFrame(self.data)
    
    def print_data(self):
        print(self.df)

if __name__ == "__main__":
    western_astrology().print_data()