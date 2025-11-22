from datetime import datetime

class date: 
    def __init__(self, datetime):
        self.datetime = datetime
    
    def day_of_year(self): 
        return self.datetime.timetuple().tm_yday



if __name__ == "__main__":
    print(date(datetime(2023, 3, 29)).day_of_year())