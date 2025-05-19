class Farm:
    def __init__(self, farm_name):
        self.name = farm_name
        self.animals = {}

    def add_animal(self, animal_type, count=1):
        if animal_type in self.animals:
            self.animals[animal_type] += count
        else:
            self.animals[animal_type] = count

    def get_info(self):
        output = f"{self.name}'s farm\n\n"
        for animal, count in self.animals.items():
            output += f"{animal} : {count}\n"
        output += "\n    E-I-E-I-0!"
        return output

    def get_animal_types(self):
        return sorted(self.animals.keys())

    def get_short_info(self):
        animal_list = self.get_animal_types()
        animal_phrases = []
        for animal in animal_list:
            if self.animals[animal] > 1:
                animal_phrases.append(animal + "s")
            else:
                animal_phrases.append(animal)
        if len(animal_phrases) == 1:
            animals_str = animal_phrases[0]
        else:
            animals_str = ', '.join(animal_phrases[:-1]) + " and " + animal_phrases[-1]
        return f"{self.name}'s farm has {animals_str}."
