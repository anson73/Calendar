import pandas as pd

from numerology import numerology

class year_calendar:
    def __init__(self): 
        self.month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def generate_calendar(self, year): 
        df = pd.DataFrame(columns=['month', 'daynumber', 'date', 'day'])
        isleapyear = numerology().is_leap_year(year)

        daycount = {1:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 11:0, 22:0, 33:0, 28:0}

        # Reduce the Year
        print(f"YEAR: {year} = {numerology().reduce(year)}")

        month = 1
        daynumber = 1
        for days in self.month_lengths:
            # Print months
            month_reduced, month_V1, month_V2 = numerology().reduce_month(year, month)
            if month_V1 == month_V2:
                print(f"{month} : {month_reduced}, {month_V1}")
            elif month_V1 > month_V2:
                print(f"{month} : {month_reduced}, {month_V1}/{month_V2}")
            elif month_V1 < month_V2:
                print(f"{month} : {month_reduced}, {month_V2}/{month_V1}")
            
            # Check for leap year
            updateddays = days
            if month == 2 and isleapyear:
                updateddays += 1

            # Print Days
            day = 1
            while day <= updateddays:
                day_reduced, day_V1, day_V2 = numerology().reduce_day(year, month, day)
                if day_V1 == day_V2:
                    print(f"\t{daynumber}) {day}/{month}/{year} : {day_reduced}, {day_V1}")
                    daycount[day_V1] += 1
                elif day_V1 > day_V2:
                    print(f"\t{daynumber}) {day}/{month}/{year} : {day_reduced}, {day_V1}/{day_V2}")
                    daycount[day_V2] += 1
                elif day_V1 < day_V2:
                    print(f"\t{daynumber}) {day}/{month}/{year} : {day_reduced}, {day_V2}/{day_V1}")
                    daycount[day_V1] += 1

                day += 1
                daynumber += 1

            month += 1


if __name__ == "__main__":
    year_calendar().generate_calendar(2026)

    # [Month, Daynumber, Date, ReducedDay, TotalDay]
