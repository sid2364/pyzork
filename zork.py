import player
import parser

map_o = parser.Map()
player_o = player.Player()
map_o.goToNextState(player_o, "north")
map_o.goToNextState(player_o, "east")

print("\n\n")

player_o = player.Player(position="dragonCell")
map_o.goToNextState(player_o, "south")

player_o = player.Player(position="dragonCell", have=['key'])
map_o.goToNextState(player_o, "south")

print("\n\n")

print(player_o.have)
map_o.takeObject(player_o, "sword")
map_o.takeObject(player_o, "key")
map_o.takeObject(player_o, "banana")
print(player_o.have)

map_o.goToNextState(player_o, "north")
print("\n\n")
map_o.killFighter(player_o, "dragon", "dagger")
map_o.killFighter(player_o, "dragon", "sword")

map_o.whereAmI(player_o)

print("\n\n")	
map_o.goToNextState(player_o, "west")
map_o.takeObject(player_o, "bone")
map_o.takeObject(player_o, "candle")
map_o.takeObject(player_o, "blue")
print(player_o.have)
map_o.takeObject(player_o, "bone")
print(player_o.have)
map_o.whereAmI(player_o)
