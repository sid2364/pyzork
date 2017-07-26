# pyzork
Yet another version of the classic text game, Zork.
You can design the entire map with the [map.json](map.json) file. This includes putting down the actual floor plan, what objects and characters you come across, which of these you can interact or fight with, and some others.

You can make your own map using these tags in this format:-

```
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
		} 
	  } 
	], 
	"objects": [
	  { 
		"objectThatIsFoundHere": { 
		  "take": true, 
		  "description": "Description of object; will be added to what player sees at this place.", 
		  "message": "Message when object is taken.", 
		  "openObject": { 
				"canOpen": true, 
				"forOpen": ["objectRequiredToOpen"], 
				"onOpen": { 
					"objectAdd": { 
						"key": { 
							"take": true, 
							"description": "Description of new object that is added to scene.", 
							"message": "Message displayed when new object is taken." 
						} 
					}, 
					"directionAdd": { 
						"south": "newDirectionAddedOnObjectOpen" 
					}, 
					"message": "Message displayed when object is opened." 
				}, 
	   		        "alreadyOpen": { 
					"opened": false, 
					"message": "Message to be displayed if object is already opened." 
				} 
		  } 
		} 
	  }, 
	  {
		"anotherObjectThatIsFoundHere": {
		  "take": false,
		  "message": "Message displayed when player tries to take the object.",
		  "description": "Description of object that player sees when present at this place."
	  },
	],
	"fighters": [ 
	{ 
	  "characterThatYouCanFight": { 
		"killable": true, 
		"altDescription": "Description of character after it's killed. Will replace in 'object' list.", 
		"mustUse": [ 
			"requiredWeapon", 
			"alternativeWeapon" 
		], 
		"onKill": {
			"directionAdd": { 
				"north": "newPlaceThatIsAccessible" 
			}, 
			"message": "Message displayed when player kills this character."
		}, 
		"alreadyKilled": { 
			"killed": false, 
			"message": "Message displayed when player tries to kill already dead character." 
		} 
	  } 
	} 
	] 
}
```

To specify where the game starts and ends, use "start" and "end" as nameOfPlace. Check [map.json](map.json) for reference.
