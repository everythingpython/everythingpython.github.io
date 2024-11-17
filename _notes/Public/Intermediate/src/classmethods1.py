from datetime import date, timedelta


class MyDate(date):
    @classmethod
    def yesterday(cls):
        today = date.today()
        d = today - timedelta(days=1)
        return cls.isoformat(d)

print(f'The date today is {MyDate.yesterday()}')
