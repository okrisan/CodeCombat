

from icebreaker import Icebreaker


class Runner:

    


    def __init__(self, handle :str, max_integrity :int, power: int, finesse :int):
        self.handle = handle
        self.max_integrity = max_integrity
        self.integrity = max_integrity
        self.power = power
        self.finesse = finesse
        self.icebreakers = None


    def equip(self, icebreakers: Icebreaker):
        self.icebreakers = icebreakers

    def modifier (self, value: int) -> int:
        return (value - 10) // 2
    
    def is_alive(self) -> bool:
        return self.integrity > 0
    
    def take_damage(self, amount: int)-> int:
        if self.integrity >= amount:
            self.integrity -= amount
        return amount
    
    def attack(self, enemy: 'Runner') -> int:
        if self.icebreakers is None:
            damage=1
        else:
            damage = self.icebreakers.get_damage()
            if self.icebreakers.type == "fracter":
                damage += self.modifier(self.power)
            elif self.icebreakers.type == "decoder":
                damage += self.modifier(self.finesse)

        if damage < 0:
            damage = 0    
        enemy.take_damage(damage)
        print(f"{self.handle} attacks {enemy.handle} with {self.icebreakers.name} for {damage} damage!")
        print(enemy)
        return damage
    
    def __str__(self):
        return f"{self.handle} (integrity {self.integrity}/{self.max_integrity})"

