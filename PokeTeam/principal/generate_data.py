import random
import names

with open("../../data/teams.txt", "a", encoding="utf-8") as file:
    for i in range(10000):
        user_id = i
        lista = []
        for j in range(6):
            pokemon = random.randint(1,802)
            if pokemon < 10:
                pokemon = "#00" + str(pokemon)
            elif pokemon < 100:
                pokemon = "#0" + str(pokemon)
            else:
                pokemon = "#" + str(pokemon)
            lista.append(pokemon)
        file.write(str(user_id) + "|" + lista[0]+ "|" + lista[1]+ "|" + lista[2]+ "|" + lista[3]+ "|" + lista[4]+ "|" + lista[5] + "\n")
        
with open("../../data/users.txt", "a", encoding="utf-8") as file:
    for i in range(10000):
        file.write(str(i) + "|" + names.get_full_name() + "\n")
