import random
from if3_game.engine import init, Layer
#de notre moteur de jeu, on importe : init qui est une fonction, et Game qui est une classe car a une majuscule
#si on veut voir ce qu'il y a dans if3_game, ctrl + clic  
from asteroid import RESOLUTION, Asteroid, Spaceship, BrilliantIdeasGame
  
init (RESOLUTION,  "THIS is an important mission. ") # on initialise la fenêtre en appelant sa taille et une chaîne de caractères qui correspond au titre de la fenêtre (on peut le modifier à loisir)

game = BrilliantIdeasGame() #on crée une instance de type Game/crée un objet 
main_layer = Layer()   

game.add(main_layer)

game.debug = False
game.run() # on lance le jeu / on va utiliser la méthode run() de la classe Game
 