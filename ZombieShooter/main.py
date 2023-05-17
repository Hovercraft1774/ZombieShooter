#Tyler Johnson
#Zombie Shooter


from scripts.game import *

def main():
    game = Game()
    game.start_Screen()
    while True:
        game.new()
        game.gameLoop()
        game.end_Screen()
        quit()




if __name__ == '__main__':
    main()