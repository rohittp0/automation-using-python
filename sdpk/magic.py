class FirstClass:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __add__(self, other):
        if not isinstance(other, FirstClass):
            return other + self

        return FirstClass(self.first + other.first, self.second + other.second)

    def __str__(self):
        return f"{self.first} {self.second}"


print(FirstClass(10, 12) + FirstClass(20, 30))
