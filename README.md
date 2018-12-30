# SmartCards


Predictive app helping announce on various card games

This project is using
  - python 3.6.7 and several libraries
  - YOLOv3
  - opencv
  - google colab
  - MongoDB 3.4
  - Django 1.11.0


---

# Card detector

## Creating a playing card dataset

```
jupyter notebook object_detection_tutorial.ipynb
```

### A. Explanation
1. Define the alphamask
  The alphamask has 2 purposes:
  - clean the border of the detected cards,
  - make that border transparent. Cards are not perfect rectangles because corners are rounded. We need to make transparent the zone between the real card and its bounding rectangle, otherwise this zone will be visible in the final generated images of the dataset
2. Function extract_card
  Extract from scene image (cv2/bgr) the part corresponding to the card and transforms it
  to fit into the reference card shape.
3. Finding the convex hulls
4. Load all card image, calculate their convex hulls and save the whole in a pickle file (1x)
  The next times, we will directly load the pickle file
  The structure saved in the pickle file is a dictionnary named 'cards' of lists of triplets (img,hullHL,hullLR). The keys of the dictionnary are the card names ("Ad","10h",... so 52 entries in the dictionnary).
5. Load the cards pickle file in 'cards'
  'cards' is an instance of the class Cards
  To get a random background image, call the method : cards.get_random() or cards.get_random(card_name) if you want a random card of a given value. Ex: cards.get_random('Ah')
6. Generating scene with 2,3....x randoms cards on an image with a random background
7. Train YOLOv3 with the generated datasets


## Train cards with YOLOv3 and the generated datasets
### A. use YOLO ipny on google colab

Check YOLO ipny and complete the setup indicated in the file

## B. Run the train and export  frozen model.pb
## C. result
here are the result at step 170k

![alt text](https://github.com/hugofloter/SmartCards/tree/master/Card_detector/data/result1)
![alt text](https://github.com/hugofloter/SmartCards/tree/master/Card_detector/data/result3)
![alt text](https://github.com/hugofloter/SmartCards/tree/master/Card_detector/data/result2)
![alt text](https://github.com/hugofloter/SmartCards/tree/master/Card_detector/data/result4)


# Create the API to detect cards and cards_games datas
## Using django
```
pip install --requirements.txt
```
## Launch server
```
python migrate.py makemigrations
python migrate.py migrate
sudo mongod
python migrate.py runserver
```

## Implementation
Severla apps are available :
- django-cards that gather routes
- coinche that creates the AI and getting rules of the game
- detector where YOLO trained is used ( sending photos and analysis return )


# API Doc :

## GET

- Sends the possible rules of the Coinche
```
def getRules(request)
```

- Sends a list of all the available cards in Coinche
```
def getListCards(request):
```

## POST

- Sends back a card with name and points data : { "name": "As" }
```
def getCard(request):
```

- Sends 4 lists with a coinche distribution (3-2-3) -> 8 cards per list data : { "firstGame": "True" }
```
def getGameHands(request):
```

- Sends the bet of a normal AI
```
data : {
            "player_hand" : [{
                "card_name" : "As",
                "value_atout": "11",
                "value_non_atout": "11",
            },
            {

            }
            ...
            ],
            "partner_bet" : {
                "type_bet" : "D",
                "value_bet" : "80"
            },
            "ennemy_bet" : {
                "type_bet" : "D",
                "value_bet" : "80"
            }
        }
def getAiBet(request):
```

- Sends back the list of the cards that a player can play at the moment t
```
{
      "cards_played" : [
          {
                  "card_name": "As",
                  "value_non_atout": 0,
                  "value_atout": 0,
                  "id" : "A"
          },
          {
                  "card_name": "7s",
                  "value_non_atout": 0,
                  "value_atout": 0,
                  "id" : "7"
          },
          {
                  "card_name": "8s",
                  "value_non_atout": 0,
                  "value_atout": 0,
                  "id" : "8"
          }
      ],
      "atout" : "c",
      "opening_color" : "s",
      "remaining_cards": [
          {
              "card_name": "7d",
              "value_non_atout": 0,
              "value_atout": 0,
              "id":"7"
          },
          {
              "card_name": "Kh",
              "value_non_atout": 4,
              "value_atout": 4,
              "id":"K"
          },
          {
              "card_name": "Ks",
              "value_non_atout": 4,
              "value_atout": 4,
              "id":"K"
          },
          {
              "card_name": "Ac",
              "value_non_atout": 11,
              "value_atout": 11,
              "id":"A"
          },
          {
              "card_name": "9c",
              "value_non_atout": 0,
              "value_atout": 14,
              "id":"9"
          }
      ]
  }


def canPlay(request):
```

- Sends a random possible move from a bot
```
{
      "cards_played" : [
          {
                  "card_name": "Ks",
                  "value_non_atout": 0,
                  "value_atout": 0,
                  "id": "K"
          },
          {
                  "card_name": "As",
                  "value_non_atout": 0,
                  "value_atout": 0,
                  "id": "A"
          },
          {
                  "card_name": "8s",
                  "value_non_atout": 0,
                  "value_atout": 0,
                  "id": "s"
          }
      ],
      "atout" : "h",
      "opening_color" : "s",
      "remaining_cards": [
          {
              "card_name": "Ah",
              "value_non_atout": 0,
              "value_atout": 0,
              "id": "A"
          },
          {
              "card_name": "8h",
              "value_non_atout": 4,
              "value_atout": 4,
              "id": "8"
          },
          {
              "card_name": "Kd",
              "value_non_atout": 4,
              "value_atout": 4,
              "id": "K"
          },
          {
              "card_name": "Ac",
              "value_non_atout": 11,
              "value_atout": 11,
              "id": "A"
          },
          {
              "card_name": "10s",
              "value_non_atout": 0,
              "value_atout": 14,
              "id": "10"
          }
      ]
  }


def getAiRandomMove(request):
```

- Sends back a normal move from a bot ( based on an alpha-beta instance with a certain heuristik)
```
{
      "cards_played" : [
          {
                  "card_name": "Ks",
                  "value_non_atout": 0,
                  "value_atout": 0,
                  "id": "K"
          },
          {
                  "card_name": "As",
                  "value_non_atout": 0,
                  "value_atout": 0,
                  "id": "A"
          },
          {
                  "card_name": "8h",
                  "value_non_atout": 0,
                  "value_atout": 0,
                  "id": "8"
          }
      ],
      "atout" : "h",
      "opening_color" : "s",
      "remaining_cards": [
          {
              "card_name": "Ad",
              "value_non_atout": 11,
              "value_atout": 11,
              "id": "A"
          },
          {
              "card_name": "8d",
              "value_non_atout": 0,
              "value_atout": 0,
              "id": "8"
          },
          {
              "card_name": "Kd",
              "value_non_atout": 4,
              "value_atout": 4,
              "id": "K"
          },
          {
              "card_name": "Ac",
              "value_non_atout": 11,
              "value_atout": 11,
              "id": "A"
          },
          {
              "card_name": "10c",
              "value_non_atout": 10,
              "value_atout": 10,
              "id": "10"
          }
      ]
  }




def getAiNormalMove(request):
```

- Sends the winner of a certain fold ( 4 cards that have been played )
```
{
      "atout" : "C"
      "cards_in_fold" : [
          {
              "played_by" : "South",
              "card_name" : "J",
              "card_color" : "c",
              "value": "20",
              "is_atout" : "True"
          },{
              "played_by" : "East",
              "card_name" : "9",
              "card_color" : "c",
              "value": "14",
              "is_atout" : "True"
          },{
              "played_by" : "North",
              "card_name" : "7",
              "card_color" : "c",
              "value": "0",
              "is_atout" : "True"
          },{
              "played_by" : "West",
              "card_name" : "8",
              "card_color" : "h",
              "value": "0",
              "is_atout" : "False"
          }
      ]
  }



def evaluateFold(request):
```


- Register a game ( who wins, who lose, bets, and so on..) in the mongoDB
```
{	"has_won" : "1",
      "points_done" : "160",
      "final_bettor" : "South",
      "team_personnal" : {
        "player_south" : "Player",
        "south_hand" : "Js-9s-As-8c-Kc-Qd-9d-7d",
        "player_north" : "Bot",
        "north_hand" : "7s-Qs-Ah-9h-7h-Jd-Jc-Qc",
        "south_is_announcing_first" : "1",
        "north_is_announcing_first" : "0"
      },
      "team_opponent" : {
        "player_south" : "Bot",
        "south_hand" : "Js-9s-As-8c-Kc-Qd-9d-7d",
        "player_north" : "Bot",
        "north_hand" : "7s-Qs-Ah-9h-7h-Jd-Jc-Qc",
        "south_is_announcing_first" : "0",
        "north_is_announcing_first" : "0"
      },
      "list_bet" : [
        {
          "bettor" : "South",
          "type_bet" : "D",
          "value_bet" : "80",
          "order_of_bet" : "1"
        },
        {
          "bettor" : "North",
          "type_bet" : "D",
          "value_bet" : "90",
          "order_of_bet" : "3"
        }
      ]
    }




def sendResultGame(request):
```



# Creating data's with the card detector application

The app is using react native, redux and thunk redux.
It uses an API created on the part 2.

Moreover, it uses Tensorflow.js as main source of the recognition part. We transformed a saved modelTF into a TF.js mopdel with a .JSON with weights.
Then we load it and be able to use it.
