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

## B. Run the train



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

URL :

# Creating data's with the card detector application

The app is using react native, redux and thunk redux.
It uses an API created on the part 2.
