import pygame
from SnakeEyes.Code.settings import Settings
import modifier
import textwrap

class GameMods:
    def __init__(self, scene_manager, game):
        self.scene_manager = scene_manager
        self.game = game
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.available_mods = modifier.available_modifiers
    
    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/shopLoop.wav")
    
    def run(self):
        self.update()
        self.render()

    def update(self):
        self.input_manager()
        

    def render(self):
        self.screen.fill(Settings.COLOR_BACKGROUND)
        self.GAME_FONT.render_to(self.screen, (10, 20), "Game Mods", Settings.COLOR_TEXT)

        for p in self.game.Players:
            self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 50), "Player "+str(p.playerNum)+": $"+str(p.score), Settings.COLOR_TEXT)
            self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 110), "Available Mods ", Settings.COLOR_TEXT)
            self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 150), modifier.available_modifiers[p.modSelection].name, Settings.COLOR_TEXT)
            #self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 340), modifier.available_modifiers[p.modSelection].description, Settings.COLOR_TEXT)
            self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 190), "$"+str(modifier.available_modifiers[p.modSelection].cost), Settings.COLOR_TEXT)
            #self.drawText(self.screen, modifier.available_modifiers[p.modSelection].description, pygame.Rect(80+(300*(p.playerNum-1)), 340, 300, 300), self.GAME_FONT)
            offset = 0
            send = ''
            for line in modifier.available_modifiers[p.modSelection].description:
                send = send + line
                if(line == '\n'):
                    self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 230+offset), send , Settings.COLOR_TEXT)
                    offset = offset + 20
                    send = ''
            self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 230+offset), send , Settings.COLOR_TEXT)
            offset = offset + 40
            if modifier.available_modifiers[p.modSelection] in p.currentMods:
                self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 230+offset), "PURCHASED" , Settings.COLOR_TEXT)

            offset = offset + 80
            self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 230+offset), "Current Mods" , Settings.COLOR_TEXT)
            offset = offset + 20
            for m in p.currentMods:
                offset = offset + 30
                self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 230+offset), m.name , Settings.COLOR_TEXT)

            

        self.GAME_FONT.render_to(self.screen, (350, 680), "Press SPACE to continue...", Settings.COLOR_TEXT)
        pygame.display.flip()

    def input_manager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.scene_manager.quit()

            if event.type == pygame.KEYDOWN:
                for p in self.game.Players:
                    print(str(event.key))
                    print(str(p.left))
                    if event.key == pygame.K_SPACE:
                        self.game.statusFlag = False
                        self.scene_manager.switch_scene('game')
                    # Scene Selection
                    if event.key == pygame.K_ESCAPE:
                        self.scene_manager.switch_scene('pause')

                    if event.key == p.left:
                        #print(str(len(self.game.Players)))
                        if(p.modSelection - 1 < 0):
                            p.modSelection = len(modifier.available_modifiers) -1 
                        else:
                            p.modSelection = p.modSelection -1
                    if event.key == p.right:
                        if(p.modSelection == len(modifier.available_modifiers) - 1):
                            p.modSelection = 0
                        else:
                            p.modSelection = p.modSelection + 1

                    if event.key == p.ready and p.score >= modifier.available_modifiers[p.modSelection].cost and modifier.available_modifiers[p.modSelection] not in p.currentMods:
                        p.score = p.score - modifier.available_modifiers[p.modSelection].cost
                        p.currentMods[modifier.available_modifiers[p.modSelection]] = modifier.available_modifiers[p.modSelection]
