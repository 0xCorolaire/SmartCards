# SmartCards
BackEnd of Coinche Application https://github.com/hugofloter/CoincheApp

Include **AI moves and choices based on alpha-beta elegation algorithm and MonteCarlo's**

Algorithm is currently not optimized (O(n^3))

Routes are served from Django framework

This project is using
  - python 3.6.7 and several libraries
  - MongoDB 3.4
  - Django 1.11.0

---

1. [Creation of the API](https://github.com/hugofloter/SmartCards#create-the-api-to-detect-cards-and-cards_games-datas)
2. [Doc of the API](https://github.com/hugofloter/SmartCards#api-doc-)
3. [Creating the app](https://github.com/hugofloter/SmartCards#creating-datas-with-the-card-detector-application)

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

- Get the prediction of the cards in a given image ( form-data ) "photo"  et le file .jpg forme carré
```
def getCardsInPhoto(request):
```


# Creating data's with the card detector application

The app is using react native, redux and thunk redux.
It uses an API created on the part 2.

Moreover, it uses Tensorflow.js as main source of the recognition part. We transformed a saved modelTF into a TF.js mopdel with a .JSON with weights.
Then we load it and be able to use it.


Bibl:
https://www.javatpoint.com/ai-alpha-beta-pruning
