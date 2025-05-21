import math

class Circle:
    def __init__(self, radius=None, diameter=None):
        if radius is not None:
            self.radius = radius
        elif diameter is not None:
            self.radius = diameter / 2
        else:
            raise ValueError("You must provide either radius or diameter.")

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def area(self):
        return round(math.pi * self.radius ** 2, 2)

    def __str__(self):
        return f"Circle with radius: {self.radius}, diameter: {self.diameter}, area: {self.area}"

    def __repr__(self):
        return f"Circle(radius={self.radius})"

    def __add__(self, other):
        if isinstance(other, Circle):
            return Circle(radius=self.radius + other.radius)
        raise TypeError("Can only add Circle to Circle.")

    def __eq__(self, other):
        return isinstance(other, Circle) and self.radius == other.radius

    def __lt__(self, other):
        return isinstance(other, Circle) and self.radius < other.radius

    def __le__(self, other):
        return isinstance(other, Circle) and self.radius <= other.radius

c1 = Circle(radius=3)
c2 = Circle(diameter=10)

print(c1)                # 👉 Circle with radius: 3, diameter: 6, area: 28.27
print(c2)                # 👉 Circle with radius: 5.0, diameter: 10.0, area: 78.54

c3 = c1 + c2
print(c3)                # 👉 Circle with radius: 8.0...

print(c1 == c2)          # 👉 False
print(c1 < c2)           # 👉 True

# Сортировка списка
circles = [c2, c3, c1]
sorted_circles = sorted(circles)
for c in sorted_circles:
    print(c)