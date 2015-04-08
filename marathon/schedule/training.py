class TrainingDay(object):
    def __init__(self, date, run):
        self.date = date
        self.run = run
        self.formatted_date = self.date.strftime("%B %d, %Y")
        self.weekday_name = self.date.strftime("%A")
        self.weekday_num = self.date.weekday()

    def __str__(self):
        return self.weekday_name.ljust(9) + self.formatted_date.ljust(20, '.') + str(self.run)

    def __repr__(self):
        return self.weekday_name.ljust(9) + self.formatted_date.ljust(20, '.') + str(self.run)