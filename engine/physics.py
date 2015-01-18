class Stepper(object):

    def __init__(self, fraction_per_update):
        self.fraction_per_update = fraction_per_update
        self.current_value = 0.0

    def __add__(self, other):

        return self.get() + other

    def get(self):
        new_value = self.current_value + self.fraction_per_update

        if int(self.current_value) == int(new_value):
            self.current_value = new_value

            return 0

        else:
            self.current_value = 0.0

            return int(new_value)

