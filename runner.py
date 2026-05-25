

from icebreaker import Icebreaker


class Runner:

    


    def __init__(self, handle :str, max_integrity :int, power: int, finesse :int):
        self.handle = handle
        self.max_integrity = max_integrity
        self.integrity = max_integrity
        self.power = power
        self.finesse = finesse
        self.icebreaker = None


    def equip(self, icebreaker: Icebreaker):
        self.icebreaker = icebreaker

    def modifier (self, value: int) -> int:
        return (value - 10) // 2
    
    def is_alive(self) -> bool:
        return self.integrity > 0
    
    def take_damage(self, amount: int)-> int:
        
        if self.integrity < amount:
            amount = self.integrity
            self.integrity = 0
            return amount
        if amount < 0:
            return 0
        
        self.integrity -= amount
        return amount
    
    def attack(self, enemy: 'Runner') -> int:
        if self.icebreaker is None:
            damage=1
            enemy.take_damage(damage)
            print(f"{self.handle} attacks {enemy.handle} for {damage} damage!")
            print(enemy)
            return damage
        
        damage = self.icebreaker.get_damage()
        if self.icebreaker .type == "fracter":
            damage += self.modifier(self.power)
        elif self.icebreaker.type == "decoder":
            damage += self.modifier(self.finesse)

        if damage < 0:
            damage = 0    

        enemy.take_damage(damage)
        print(f"{self.handle} attacks {enemy.handle} with {self.icebreaker.name} for {damage} damage!")
        print(enemy)
        return damage
    
    def __str__(self):
        return f"{self.handle} (integrity {self.integrity}/{self.max_integrity})"

