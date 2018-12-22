# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import get_template
from rest_framework import mixins, viewsets, views
from rest_framework.decorators import (api_view, permission_classes,
                                       renderer_classes)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import json
from coinche import models as coinche_models
import tensorflow as tf

"""
Note globale pour ce fichier :

Dans ce fichier, en dehors des viewsets, les vues
simples sont déclarées de deux façons :
- de façon générique Django, avec une fonction qui va se terminer par le retour d'un
render d'une template Django.
- de façon Django REST Framework - cette façon permet de définir clairement les méthodes
HTTP par lesquelles une vue peut être atteinte, et permet de prédéfinir le Content-Type
dans lequel la réponse sera rendue.
Par exemple, pour les vues qui sont sensées retourner du JSON, on utilisera le
renderer REST Framework appelé JSONRenderer.

Ces deux vues peuvent être distinguées par l'utilisation des décorateurs api_view (définition
des méthodes HTTP) et renderer_class (content type du retour), qui sont caractéristiques de
la vue REST Framework.

L'intérêt d'une vue générique Django est de permettre de render une vue, tandis que celle
de la vue Django REST Framework est de pouvoir retourner facilement dans un format voulu.
On utilisera donc principalement les vues traditionnelles pour afficher des pages, et des
vues REST Framework pour des appels d'API (qui serviront, par exemple, en appel AJAX).
user = authenticate(username=username, password=password)
assert isinstance(user, mongoengine.django.auth.User)
"""

"""
Fonctions Utiles reconnaissance cartes
"""
class PlayingCardsClassifier(object):
    def __init__(self):
        PATH_TO_MODEL = 'frozen_inference_graph.pb'
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            # Works up to here.
            with tf.gfile.GFile(PATH_TO_MODEL, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
            self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            self.d_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
            self.d_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            self.d_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            self.num_d = self.detection_graph.get_tensor_by_name('num_detections:0')
        self.sess = tf.Session(graph=self.detection_graph)

    def get_classification(self, img):
        # Bounding Box Detection.
        with self.detection_graph.as_default():
            # Expand dimension since the model expects image to have shape [1, None, None, 3].
            img_expanded = np.expand_dims(img, axis=0)
            (boxes, scores, classes, num) = self.sess.run(
                [self.d_boxes, self.d_scores, self.d_classes, self.num_d],
                feed_dict={self.image_tensor: img_expanded})
        return boxes, scores, classes, num

"""
API Detector
"""

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def getCardsInPhoto(request):
    """
    Endpoint qui permet d'obtenir la liste des cartes sur la photo
    """
    body = json.loads(request.body)
    photo = body['photo']
    result = PlayingCardsClassifier.get_classification(photo)
    final_list_cards = result[2]

    return Response(final_list_cards)

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def getHandInPhoto(request):
    """
    Endpoint qui permet d'obtenir les cartes présentes sur la photo dans la main et retourne une photo avec le nombre de points dans la main
    """
    body = json.loads(request.body)
    photo = body['photo']
    # On envoie la photo dans YOLO et on choppe le retour
    # Une fois la photo retour avec la liste des cartes, on retourne la liste des cartes
    list_cards = []
    result = PlayingCardsClassifier.get_classification(photo)
    # result=[[boxes,box...],[scores,sddds],[classes,classes],[num,num]]
    final_list_cards = result[2]
    total_points = 0
    for e in final_list_cards:
        card = coinche_models.ListCards.objects.filter(
                card_name = e
            ).values('card_name','value_non_atout','value_atout')
        total_point+=card['value_non_atout']

    return Response({
        'list_cartes': final_list_cards,
        'total_point': total_point
    })
