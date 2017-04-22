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
print(player_o.have)
