from datetime import datetime, date
from typing import Dict

class numerology: 
    def __init__(self): 
        self.base_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33]
        self.master_numbers = [11, 22, 33]
    
    def is_leap_year(self, year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def get_sum(self, n):
        '''
        Add all the digits of a number
        '''
        sum = 0
        while (n != 0):
            sum = sum + (n % 10)
            n = n//10
        return sum

    def get_sum_w(self, n):
        '''
        Wrapper for get_sum to not sum up master numbers
        '''
        if n in self.base_numbers: 
            return n

        return self.get_sum(n)

    def reduce_final(self, n):
        '''
        Recursively add all the digits of a number until it reaches a base number. 
        Only use this function if it is the final step of the reduction. 
        Handles the case where 20 -> 11
        '''
        if n in self.base_numbers: 
            return n

        if n == 20: 
            return 11

        return self.reduce_final(self.get_sum(n))

    def reduce_number(self, n):
        '''
        Recursively add all the digits of a number until it reaches a base number. 
        '''
        if n in self.base_numbers: 
            return n

        return self.reduce_number(self.get_sum(n))

    def get_info(self, date: date) -> Dict[str, str]:
        '''
        Get all info for date
        '''

        # Day of year
        day_of_year = date.timetuple().tm_yday

        # Day
        day = date.day
        reduced_day = self.reduce_final(day)

        # Month
        month = date.month
        reduced_month = self.reduce_final(month)

        # Year
        year = date.year
        year_reduced = self.reduce_final(year)

        # LP Day
        lp_day_full = self.get_sum_w(year) + month + day
        lp_day_reduced = self.get_sum_w(year) + self.get_sum_w(month) + self.get_sum_w(day)
        
        lp_day_full_reduced = self.reduce_final(lp_day_full)
        lp_day_reduced_reduced = self.reduce_final(lp_day_reduced)

        lp_day_full_combined = str(lp_day_full) + "->" + str(lp_day_full_reduced)
        lp_day_reduced_combined = str(lp_day_reduced) + "->" + str(lp_day_reduced_reduced)

        if lp_day_full_reduced != lp_day_reduced_reduced: 
            lp_day = f"{max(lp_day_full_reduced, lp_day_reduced_reduced)}/{min(lp_day_full_reduced, lp_day_reduced_reduced)}"

        else:
            lp_day = str(lp_day_reduced_reduced)

        # LP Month
        lp_month_full = self.get_sum_w(year) + month
        lp_month_reduced = self.get_sum_w(year) + self.get_sum_w(month)
        lp_month_full_reduced = self.reduce_final(lp_month_full)
        lp_month_reduced_reduced = self.reduce_final(lp_month_reduced)

        lp_month_full_combined = str(lp_month_full) + "->" + str(lp_month_full_reduced)
        lp_month_reduced_combined = str(lp_month_reduced) + "->" + str(lp_month_reduced_reduced)

        if lp_month_full_reduced != lp_month_reduced_reduced: 
            lp_month = f"{max(lp_month_full_reduced, lp_month_reduced_reduced)}/{min(lp_month_full_reduced, lp_month_reduced_reduced)}"

        else:
            lp_month = str(lp_month_reduced_reduced)

        stats = {"date": date.strftime("%Y-%m-%d"), "day_of_year": day_of_year, 
                 "day": day, "reduced_day": reduced_day, 
                 "month": month, "reduced_month": reduced_month, 
                 "year": year, "year_reduced": year_reduced, 

                 "lp_day_full": lp_day_full, "lp_day_reduced": lp_day_reduced, 
                 "lp_day_full_reduced": lp_day_full_reduced, "lp_day_reduced_reduced": lp_day_reduced_reduced, 
                 "lp_day_full_combined": lp_day_full_combined, "lp_day_reduced_combined": lp_day_reduced_combined, 
                 "lp_day": lp_day, 

                 "lp_month_full": lp_month_full, "lp_month_reduced": lp_month_reduced, 
                 "lp_month_full_reduced": lp_month_full_reduced, "lp_month_reduced_reduced": lp_month_reduced_reduced, 
                 "lp_month_full_combined": lp_month_full_combined, "lp_month_reduced_combined": lp_month_reduced_combined, 
                 "lp_month": lp_month, 
                 }

        return stats

if __name__ == "__main__":
    print(numerology().get_info(date(2025, 11, 20)))
