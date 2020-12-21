class Job:
    def __init__(self, job_parameters):
        self.total_salary = job_parameters['amount']
        self.holiday_allowance_perc = job_parameters['holiday_allowance']
        self.monthly_salary = self.total_salary / (1 + self.holiday_allowance_perc) / 12

    def get_salary(self, month):
        pay = self.monthly_salary
        if month % 12 == 4:
            pay += self.holiday_allowance
        return pay

    @property
    def holiday_allowance(self):
        return self.total_salary * self.holiday_allowance_perc / (1 + self.holiday_allowance_perc)
