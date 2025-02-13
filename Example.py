import pygame
from Library_A import ClickerGame #import the ClickerGame class from Library_A
# Initialize game instance
game = ClickerGame()

#game. is the main class, game. can also be used to call functions from the class 
# for example game.add_upgrade, game.update, game.render, game.cleanup etc.

#this game is fully functional and can be run as is, but you can add more upgrades to the game by using the game.add_upgrade function
#have fun and play around with the code to see what you can do with it
#be sure to check if i have added any new functions to the game class that you can use
#again this is open sourced so dont be scared to tell me if you have any ideas or suggestions

#game.add_upgrade is the function that adds upgrades to the game

# Add sample upgrades
game.add_upgrade("Double Click", 50, 2)
game.add_upgrade("Auto Clicker", 100, "auto")
game.add_upgrade #(name, cost, effect, max_level=10)
# Run game loop
pygame.init() 
font = pygame.font.SysFont('Arial', 20, bold=True) #sets the font
clock = pygame.time.Clock()
running = True 

while running: 


    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        game.handle_event(event) #handles the event
        game.render_button #renders the button
        #game.Click_anywhere(event) #makes it so you can click anywhere on the screen to get cookies


    game.update()
    game.render(font)
    clock.tick(game.FPS) #sets the frames per second


game.cleanup() #cleanup the game
