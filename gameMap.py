# -*- coding: utf-8 -*-

import json
import os
import pickle
import sys

try:
    import nltk

    nltk.data.path.append(os.path.join(os.getcwd(), "nltk_data"))
    from nltk import PorterStemmer
except ImportError:
    print("You need NLTK installed to run this game.")
    sys.exit(0)

mapFile = "map.json"
saveGameMapFile = "savedGameMap.dat"
saveGamePlayerFile = "savedGamePlayer.dat"

# JSON tags for the map
description = "description"
prerequisites = "prerequisites"
objects = "objects"
directions = "directions"
take = "take"
message = "message"
problem = "problem"
solution = "solution"
fighters = "fighters"
killable = "killable"
altDescription = "altDescription"
mustUse = "mustUse"
openObject = "openObject"
canOpen = "canOpen"
onOpen = "onOpen"
forOpen = "forOpen"
action = "action"
objectAdd = "objectAdd"
directionAdd = "directionAdd"
alreadyOpen = "alreadyOpen"
opened = "opened"
onKill = "onKill"
alreadyKilled = "alreadyKilled"
killed = "killed"
end = "end"


def byteify(data, ignore_dicts=False):
    """Compatibility shim from the old Python 2 implementation."""
    return data


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def welcome():
    clear()
    print(
        "================================================ Z O R K ================================================"
    )
    print("Welcome to Zork!")
    print(
        "This is a text based adventure game, where you control your character by typing commands into the terminal."
    )
    print("Hope you have fun with the game! Happy adventuring!")
    if not os.path.exists(saveGameMapFile) and not os.path.exists(saveGamePlayerFile):
        return 1
    print("\nDo you wish to load a saved game?")
    try:
        said = input("[y/n] ")
    except (KeyboardInterrupt, EOFError):
        print("\nGood-bye.")
        sys.exit()
    return 0 if said.lower() == "y" else 1


def stem(word):
    ps = PorterStemmer()
    return ps.stem(word)


def saveGame(mapDict, playerInfo):
    with open(saveGameMapFile, "wb") as f:
        pickle.dump(mapDict, f)
    with open(saveGamePlayerFile, "wb") as f:
        playerState = (playerInfo.position, playerInfo.direction, playerInfo.have)
        pickle.dump(playerState, f)


def loadGame():
    try:
        fm = open(saveGameMapFile, "rb")
        mapDict = pickle.load(fm)
        fm.close()

        fp = open(saveGamePlayerFile, "rb")
        p, d, h = pickle.load(fp)
        fp.close()
    except (OSError, IOError):
        print("Cannot load game. File not found.")
        return None, None, None, None
    return mapDict, p, d, h


class Map:
    def __init__(self, mapDict=None):
        if mapDict is not None:
            self.fsm = mapDict
        else:
            try:
                with open(mapFile, "r") as map_f:
                    self.fsm = json.load(map_f)
            except (IOError, OSError):
                print("Cannot load game. Map file not found.")
                sys.exit(0)

    def mainMenu(self, p_player):
        clear()

    def help(self, p_player):
        print(
            "\nZork is a fully text based adventure game. You can let your imagination run wild as the game guides you through the story. You interact with the environment and control your character by typing commands into the terminal in natural language. Though the game understands some variations in your commands, there is a structure, as described below."
        )
        print("\nYou may use commands like:-")
        print("Go north\t\t\tTo move your character in a particular direction.")
        print("Look\t\t\t\tTo look around you and describe what you see.")
        print("Look door\t\t\tTo examine a specific object in sight.")
        print("Pick up banana\t\t\tTo take an object from the environment you are in.")
        print("Open door\t\t\tTo open the door, duh.")
        print("Help\t\t\t\tTo display these messages again.")
        print("Drop pencil\t\t\tTo drop the object whereever you currently are.")
        print("Inventory\t\t\tTo check what you currently have on you.")
        print(
            "\n================================================ Z O R K ================================================"
        )

    """
    Goes to the next state in the direction specified, if possible
    """

    def goToNextState(self, p_player, p_direction):
        prerequisites_d = {}
        try:
            newState = self.fsm[p_player.position][directions][p_direction]
        except KeyError:
            print("You can't go " + p_direction + ".")
            return
        try:
            prerequisites_d = self.fsm[newState][prerequisites]
        except KeyError:
            pass
        for item in prerequisites_d:
            for key in item:
                if not key in p_player.have:
                    try:
                        print(item[key][problem])
                    except KeyError:
                        print("You cannot go there.")
                    return
                else:
                    try:
                        print(item[key][solution])
                    except KeyError:
                        continue
        p_player.moveToNewState(newState, p_direction)
        self.whereAmI(p_player)
        if newState == end:
            print("\nBravo! You beat the game!")
            try:
                input("\nPress enter to exit...")
            except (EOFError, KeyboardInterrupt):
                pass
            sys.exit()
        return

    """
    Tries to take the object from current position
    """

    def takeObject(self, p_player, p_object):
        try:
            obj_l = self.fsm[p_player.position][objects]
            if p_object in p_player.have:
                print("You already have that!")
                return
            for obj in obj_l:
                for key in obj:
                    if p_object == stem(key):
                        print(obj[key][message])
                        if obj[key][take]:
                            p_player.takeItem(p_object)
                            obj[key][take] = False
                            # Removing item from the map
                            del obj[key]
                            obj_l[:] = [d for d in obj_l if d]
                        return
            print("You see no such thing here.")
        except KeyError:
            print("You cannot do that.")

    def inventory(self, p_player):
        if p_player.have:
            say = "You have with you: "
            say += ", ".join(p_player.have)
            say += "."
        else:
            say = "You do not hold anything at the moment."
        print(say)

    """
    Drops the object in the current position
    """

    def dropObject(self, p_player, p_object):
        if p_object not in p_player.have:
            print("Cannot drop something you don't have!")
            return
        try:
            obj_l = self.fsm[p_player.position][objects]
        except KeyError:
            # No objects mentioned - create object list and redo
            self.fsm[p_player.position][objects] = []
            self.dropObject(p_player, p_object)
            return
        obj_d = {
            p_object: {
                "take": True,
                "message": "You have picked up the " + p_object + ".",
                "description": "You see the "
                + p_object
                + " you dropped on the ground.",
            }
        }
        obj_l.append(obj_d)
        p_player.have.remove(p_object)
        print("Dropped.")

    """
    Tries to kill the fighter in the current position
    """

    def killFighter(self, p_player, p_fighter, p_weapon=None):
        if p_weapon is None:
            print("You do not stand a chance if you fight with your bare hands.")
            if not p_player.have:
                print("Come back another day when you are deemed a worthy opponent.")
                return
            else:
                try:
                    weapon = input("\nWhat weapon do you want to use for this battle? ")
                except (EOFError, KeyboardInterrupt):
                    print("You can type 'quit' if you wish to get out of here.")
                    return
                if not weapon:
                    print("Alright then...")
                    return
                p_weapon = weapon
        foundFighter = None
        if p_weapon not in p_player.have:
            print("You do not possess this " + p_weapon + " of which you speak.")
            return
        try:
            fighters_l = self.fsm[p_player.position][fighters]
            for fighter in fighters_l:
                for key in fighter:
                    if p_fighter == stem(key):
                        if fighter[key][alreadyKilled][killed]:
                            print(fighter[key][alreadyKilled][message])
                            return
                        foundFighter = str(key)
                        if foundFighter[0].upper() == foundFighter[0]:
                            say = foundFighter
                        else:
                            say = "The " + foundFighter
                        say += " ogles you keenly."
                        print(say)
                        if not fighter[key][killable]:
                            say = "You cannot kill "
                            if foundFighter[0].upper() != foundFighter[0]:
                                say += "the "
                            say = foundFighter + "."
                            return
                        if (
                            p_weapon in fighter[key][mustUse]
                            or not fighter[key][mustUse]
                        ):
                            say = "You draw your " + p_weapon + " and slay "
                            if foundFighter[0].upper() != foundFighter[0]:
                                say += "the "
                            say += foundFighter + "."
                            print(say)
                            fighter[key][alreadyKilled][killed] = True
                            try:
                                newDirection = fighter[key][onKill][directionAdd]
                                self.fsm[p_player.position][directions].update(
                                    newDirection
                                )
                                print(fighter[key][onKill][message])
                            except KeyError:
                                pass
                        else:
                            say = (
                                "You do not possess a weapon worthy "
                                + "of this battle. You decide to live "
                                + "and let live."
                            )
                            print(say)
                            return
                        for obj in self.fsm[p_player.position][objects]:
                            for k in obj:
                                if k == foundFighter:
                                    obj[k][description] = str(
                                        fighter[key][altDescription]
                                    )
                                    obj[k][take] = False

        except KeyError:
            print(
                "There is no "
                + p_fighter
                + " you can tussle with here. With a word you can get what you came for."
            )

    """
    Prints the description of current position
    """

    def whereAmI(self, p_player):
        try:
            print(self.fsm[p_player.position][description])
        except KeyError:  # Map region has no description (but why?)
            print(
                "There is darkness all around you. All you can hear is your heavy breathing..."
            )
        try:
            for obj in self.fsm[p_player.position][objects]:
                for k in obj:
                    try:
                        print(obj[k][description])
                    except:
                        pass
        except KeyError:  # map has no description (but, why?)
            pass

    """
    Tries to open object in the current position
    """

    def openObject(self, p_player, p_object):
        say = "There is no such thing you see here."
        try:

            obj_l = self.fsm[p_player.position][objects]
            for obj in obj_l:
                for key in obj:
                    if p_object == str(key):
                        if obj[key][openObject][canOpen]:
                            if (
                                set(obj[key][openObject][forOpen]).issubset(
                                    set(p_player.have)
                                )
                                or obj[key][openObject][forOpen] == []
                            ):
                                if obj[key][openObject][alreadyOpen][opened]:
                                    say = obj[key][openObject][alreadyOpen][message]
                                    print(say)
                                    return
                                saidAlready = False
                                try:
                                    newDirection = obj[key][openObject][onOpen][
                                        directionAdd
                                    ]
                                    self.fsm[p_player.position][directions].update(
                                        newDirection
                                    )
                                    print(obj[key][openObject][onOpen][message])
                                    saidAlready = True
                                except KeyError:
                                    pass
                                # Seperate try-except because directionAdd/objectAdd may not exist together
                                try:
                                    self.fsm[p_player.position][objects].append(
                                        obj[key][openObject][onOpen][objectAdd]
                                    )
                                    if not saidAlready:
                                        print(obj[key][openObject][onOpen][message])
                                        saidAlready = True
                                except KeyError:
                                    pass
                                try:
                                    obj[key][openObject][alreadyOpen][opened] = True
                                except KeyError:
                                    pass
                                try:
                                    if not saidAlready:
                                        print(obj[key][openObject][onOpen][message])
                                except KeyError:
                                    pass
                                return
                            else:
                                say = (
                                    "You do not have the required object to open this."
                                )
                        else:
                            say = "It's not possible to open the " + p_object + "."

        # print(say)
        except KeyError:
            print("You cannot do that.")
            return

        print(say)

    """
    Describe an object in the current position
    """

    def examineObject(self, p_player, p_object):
        if p_object in p_player.have or stem(p_object) in [
            stem(o) for o in p_player.have
        ]:
            print(f"You are already holding the {p_object}.")
            return
        try:
            obj_l = self.fsm[p_player.position][objects]
            for obj in obj_l:
                for key in obj:
                    if p_object == stem(key) or p_object == key:
                        try:
                            print(obj[key][description])
                        except KeyError:
                            print("You see nothing special about the " + p_object + ".")
                        return
            print("You see no such thing here.")
        except KeyError:
            print("You see nothing special here.")

    """
    Returns list of objects present in the current position
    """

    def getObjectList(self, p_player):
        objects_ret = []
        try:
            obj_l = self.fsm[p_player.position][objects]
            for obj in obj_l:
                for key in obj:
                    objects_ret.append(key)
        except KeyError:
            return []
        return objects_ret

    """
    Returns list of fighters present in the current position
    """

    def getFighterList(self, p_player):
        fighters_ret = []
        try:
            fighters_l = self.fsm[p_player.position][fighters]
            for fighter in fighters_l:
                for key in fighter:
                    fighters_ret.append(key)
        except KeyError:
            return []

        return fighters_ret

    def sayOkay(self, p_player):
        print("Okay then...")


if __name__ == "__main__":
    map_o = Map()
