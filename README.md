# pyzork
Yet another version of the classic text game, Zork.
You can design the entire map with the __map.json__ file. This includes putting down the actual floor plan, what objects and characters you come across, which of these you can interact or fight with, and some others.

You can make your own map using these tags in this format:-

"nameOfPlace": {

	"description": "Description of what the player sees here.",

	"directions": {

	  "north-west": "somePlaceThatIsNorthWestOfHere",

	  "south": "somePlaceThatIsSouthOfHere"

	},

	"prerequisites": [

	  { 

		"objectRequiredToGetToThisPlace": {

		  "problem": "Message displayed if player does not have the object.", 

		  "solution": "Message displayed if player has the object and tries to enter."

		} __
	  } __
	], __
	"objects": [ __
	  { __
		"objectThatIsFoundHere": { __
		  "take": true, __
		  "description": "Description of object; will be added to what player sees at this place.", __
		  "message": "Message when object is taken.", __
		  "openObject": { __
				"canOpen": true, __
				"forOpen": ["objectRequiredToOpen"], __
				"onOpen": { __
					"objectAdd": { __
						"key": { __
							"take": true, __
							"description": "Description of new object that is added to scene.", __
							"message": "Message displayed when new object is taken." __
						} __
					}, __
					"directionAdd": { __
						"south": "newDirectionAddedOnObjectOpen" __
					}, __
					"message": "Message displayed when object is opened." __
				}, __
	   		        "alreadyOpen": { __
					"opened": false, __
					"message": "Message to be displayed if object is already opened." __
				} ___
		  } __
		} __
	  }, __
	  {
		"anotherObjectThatIsFoundHere": { __
		  "take": true, __
		  "message": "Message displayed when player takes the object." __
	  },__
	], __
	"fighters": [ __
	{ __
	  "characterThatYouCanFight": { __
		"killable": true, __
		"altDescription": "Description of character after it's killed. Will replace in 'object' list.", __
		"mustUse": [ __
			"requiredWeapon", __
			"alternativeWeapon" __
		], __
		"onKill": { __
			"directionAdd": { __
				"north": "newPlaceThatIsAccessible" __
			}, __
			"message": "Message displayed when player kills this character." __
		}, __
		"alreadyKilled": { __
			"killed": false, __
			"message": "Message displayed when player tries to kill already dead character." __
		} __
	  } __
	} __
	] __
} __


