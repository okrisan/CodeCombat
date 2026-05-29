from runner import Runner
from icebreaker import Icebreaker
import random

if __name__=="__main__":


    # Create some icebreakers
    fracter = Icebreaker("Fracter", 2, 5, "fracter")
    decoder = Icebreaker("Decoder", 1, 4, "decoder")

    # Create some runners
    runner1 = Runner("Runner1", 20, random.randint(1, 20), random.randint(1, 20))
    runner2 = Runner("Runner2", 18, random.randint(1, 20), random.randint(1, 20))

    # Equip icebreakers
    runner1.equip(fracter)
    runner2.equip(decoder)
    i=0

    print("--- Battle Start ---")
    # Simulate a battle
    while runner1.is_alive() and runner2.is_alive():
        i += 1
        print(f"--- Round {i} ---")

        if i % 2:
            runner1.attack(runner2)
        else:
            runner2.attack(runner1)


        if not runner2.is_alive():
            print(f"{runner2.get_handle()} has been defeated!")
            break
        
        if not runner1.is_alive():
            print(f"{runner1.get_handle()} has been defeated!")
            break

    print("--- Battle End ---")