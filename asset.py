
class Asset:
    def __init__(self, initial_value, return_rate):
        self.value = initial_value
        self.return_rate = return_rate

    def add(self, amount):
        self.value += amount

    def advance(self):
        self.value *= 1 + self.return_rate / 12
