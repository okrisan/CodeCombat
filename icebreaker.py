import random


class Icebreaker:
    
    def __init__ (self, name :str, min_damage :int, max_damage :int, type :str):
        
         

       


        if type not in ["fracter", "decoder"]:
            print("Invalid type. Type must be 'fracter', 'decoder'. Will be set to 'fracter' by default.")
            type = "fracter"
    
        self.__type= type    
        self.__name = name
        if not isinstance(min_damage, int) or not isinstance(max_damage, int):
            print("Warning: Damage values must be integers. Setting defaults to 1.")
            min_damage = 1
            max_damage = 1
        elif min_damage > max_damage:
            print("Warning: Minimum damage cannot be greater than maximum damage. Swapping values.")
            min_damage, max_damage = max_damage, min_damage

        if min_damage < 1:
            print("Warning: Damage values cannot be negative. Setting to 1.")
            min_damage = 1
        if max_damage < 1:
            max_damage = 1

        self.__min_damage = min_damage
        self.__max_damage = max_damage

    def set_min_damage(self, value: int):
        if not isinstance(value, int):

            print("Warning: Damage values must be integers. No change applied.")
            return value
        if value > self.__max_damage and self.__max_damage != None:
            print("Warning: Minimum damage cannot be greater than maximum damage. Swapping values.")
            (value, self.__max_damage) = (self.__max_damage, value)
            return value
        if value < 1:
            print("Warning: Damage values cannot be negative. Setting to 1.")
            value = 1
            return value
        self.__min_damage = value
        return value

    def set_max_damage(self, value: int):
        if not isinstance(value, int):
            print("Warning: Damage values must be integers. Setting to 1.")
            if self.__max_damage == None:
                value = 1
            else:
                print("Warning: Damage values must be integers. No change applied.")
            return value
        if value < self.__min_damage and self.__min_damage != None:
            print("Warning: Maximum damage cannot be less than minimum damage. Swapping values.")
            (value, self.__min_damage) = (self.__min_damage, value)
            return value
        if value < 1:
            print("Warning: Damage values cannot be negative. Setting to 1.")
            value = 1
            return value

        self.__max_damage = value
        return value

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