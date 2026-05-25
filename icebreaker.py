import random


class Icebreaker:
    def __init__ (self, name :str, min_damage :int, max_damage :int, type :str):
        if min_damage < 0 or max_damage < 0:
            print("Damage values cannot be negative.")
            min_damage= int(input("Enter minimum damage: "))
            max_damage= int(input("Enter maximum damage: "))

        if min_damage >= max_damage:
            print("Minimum damage cannot be greater than or equal to maximum damage.")
            min_damage= int(input("Enter minimum damage: "))
            max_damage= int(input("Enter maximum damage: "))

        if type not in ["fracter", "decoder"]:
            print("Invalid type. Type must be 'fracter', 'decoder'.")
            type = input("Enter type (fracter, decoder): ")
    
        self.type = type    
        self.name = name
        self.min_damage = min_damage
        self.max_damage = max_damage
    def get_damage(self)->int:
        return random.randint(self.min_damage, self.max_damage)
    def __str__(self):
        return f"{self.name} ({self.type}): {self.min_damage}-{self.max_damage} damage"