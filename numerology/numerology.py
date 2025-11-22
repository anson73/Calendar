from datetime import datetime

class numerology: 
    def __init__(self): 
        self.base_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33]
        self.master_numbers = [11, 22, 33]
    
    def is_leap_year(self, year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def getSum(self, n):
        '''
        Add all the digits of a number
        '''
        sum = 0
        while (n != 0):
            sum = sum + (n % 10)
            n = n//10
        return sum

    def reduce(self, n):
        '''
        Recursively add all the digits of a number until it reaches a base number. 
        '''
        if n in self.base_numbers: 
            return n

        if n == 20: 
            return 11

        if n == 28: 
            return n

        return self.reduce(self.getSum(n))

    def reduce_month(self, year, month):
        reduce_month = month
        year_sum = self.getSum(year)

        # Version 1 (seperate digits month + year)
        month_V1 = month
        if month_V1 != 11:
            month_V1 = self.getSum(month_V1)

        month_V1 = self.reduce(month_V1 + year_sum)

        # Version 2 (whole month + year)
        month_V2 = self.reduce(month + year_sum)

        # Reduce month individually
        reduce_month = self.reduce(month)

        return (reduce_month, month_V1, month_V2)

    def reduce_day(self, year, month, day):
        reduce_day = day
        year_sum = self.getSum(year)

        # Version 1 (seperate digits day + month + year)
        day_V1 = day
        if day_V1 not in self.master_numbers:
            # Reduce day individually
            if day_V1 == 20 or day_V1 == 29:
                reduce_day = 11
            else:
                reduce_day = self.reduce(day_V1)
            day_V1 = self.getSum(day_V1)

        month_V1 = month
        if month_V1 != 11:
            month_V1 = self.getSum(month_V1)

        day_V1 = self.reduce(day_V1 + month_V1 + year_sum)

        # Version 2 (whole day + month + year)
        day_V2 = self.reduce(day + month + year_sum)

        return (reduce_day, day_V1, day_V2)
    
    def reduce_wrapper(self, date):
        date = datetime.strptime(date, "%Y-%m-%d")
        day, reduced_1, reduced_2 = self.reduce_day(date.year, date.month, date.day)

        return reduced_1


if __name__ == "__main__":
    print(numerology().reduce_day(2025, 8, 15))
    print(numerology().reduce_wrapper("1971-06-28"))
    