from django.utils import timezone

import calendar


class Day:
    def __init__(self, year, month, number):
        super().__init__()
        self.number = number
        self.month = month
        self.year = year

    def is_past(self):
        now = timezone.now()
        today = now.day
        now_month = now.month
        now_year = now.year
        if self.year == now_year:
            if self.month == now_month:
                return self.number <= today
            else:
                return self.month < now_month
        else:
            return self.year < now_year

    def getUrlRepr(self):
        if self.number==0:
            return
        return f"{self.year}-{self.month}-{self.number}"

    @classmethod
    def fromUrlRepr(cls, urlRepr: str):
        day_fields = urlRepr.split("-")
        return cls(*day_fields)

    def __str__(self):
        if self.number == 0:
            return ""
        return str(self.number)

    def __repr__(self):
        return f"<Day: year=='{self.year}', month=='{self.month}', number=='{self.number}'>"
    

class MyCalendar(calendar.Calendar):
    def __init__(self, year, month) -> None:
        super().__init__(firstweekday=0)
        self.year = year
        self.month = month
        self.day_names = ("Mon", "Tye", "Wed", "Thu", "Fry", "Sat", "Sun")
        self.months = (
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        for week in weeks:
            for day, _ in week:
                new_day = Day(self.year, self.month, day)
                days.append(new_day)
        return days

    def get_month(self):
        return self.months[self.month-1]
    
    def get_next_month(self):
        return self.months[self.month]


if __name__ == '__main__':
    new_cal = MyCalendar(2021, 3)
    new_cal.get_days()
