import random


class Icebreaker:
    def __init__ (self, name :str, min_damage :int, max_damage :int, type :str):
        
        if min_damage < 1:
            print("Warning: Damage values cannot be negative. Setting to 1.")
            min_damage= 1
        if max_damage < 1:
            print("Warning: Damage values cannot be negative. Setting to 1.")
            max_damage= 1

        if min_damage > max_damage:
            print("Warning: Minimum damage cannot be greater than or equal to maximum damage, switching values.")
            (max_damage,min_damage)= (min_damage, max_damage)
           
        

        if type not in ["fracter", "decoder"]:
            print("Invalid type. Type must be 'fracter', 'decoder'. Will be set to 'fracter' by default.")
            type = "fracter"
    
        self.__type= type    
        self.__name = name
        self.__min_damage = min_damage
        self.__max_damage = max_damage

    def get_type(self):
        return self.__type
    def get_name(self):
        return self.__name
    def get_min_damage(self):
        return self.__min_damage
    def get_max_damage(self):        
        return self.__max_damage


    def get_damage(self)->int:
        return random.randint(self.__min_damage, self.__max_damage)
    def __str__(self):
        return f"{self.__name} ({self.__type}): {self.__min_damage}-{self.__max_damage} damage"