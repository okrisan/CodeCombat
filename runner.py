

from icebreaker import Icebreaker


class Runner:

    


    def __init__(self, handle :str, max_integrity :int, power: int, finesse :int):
        self.__handle = handle
        self.__max_integrity = max_integrity
        self.__integrity = max_integrity
        self.__power = power
        self.__finesse = finesse
        self.__icebreaker = None


    def equip(self, icebreaker: Icebreaker):
        self.__icebreaker = icebreaker

    def modifier (self, value: int) -> int:
        return (value - 10) // 2
    
    def is_alive(self) -> bool:
        return self.__integrity > 0
    
    def take_damage(self, amount: int)-> int:
        
        if self.__integrity < amount:
            amount = self.__integrity
            self.__integrity = 0
            return amount
        if amount < 0:
            return 0
        
        self.__integrity -= amount
        return amount
    
    def attack(self, enemy: 'Runner') -> int:
        if self.__icebreaker is None:
            damage=1
            damage=enemy.take_damage(damage)
            print(f"{self.__handle} attacks {enemy.__handle} for {damage} damage!")
            print(enemy)
            return damage
        
        damage = self.__icebreaker.get_damage()
        if self.__icebreaker.get_type() == "fracter":
            damage += self.modifier(self.__power)
        elif self.__icebreaker.get_type() == "decoder":
            damage += self.modifier(self.__finesse)

            

        damage=enemy.take_damage(damage)
        print(f"{self.__handle} attacks {enemy.__handle} with {self.__icebreaker.get_name()} for {damage} damage!")
        print(enemy)
        return damage
    
    def get_handle(self):
        return self.__handle
    def get_integrity(self):
        return self.__integrity 
    def get_max_integrity(self):
        return self.__max_integrity
    def get_power(self):    
        return self.__power
    def get_finesse(self):
        return self.__finesse
    
    
    def __str__(self):
        return f"{self.__handle} (integrity {self.__integrity}/{self.__max_integrity})"
