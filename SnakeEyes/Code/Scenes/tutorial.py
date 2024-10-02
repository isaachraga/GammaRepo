import pygame
from settings import Settings
import pygame_gui

class Tutorial:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.HEADER_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.HEADER_FONT_SIZE)
        self.controlSchemeNum = 0

        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json") #pygame_gui manager
        self.clock = pygame.time.Clock() #Needed for pygame_gui

        self.make_GUI()
        self.hide_GUI()
        self.default_text.show()

    def make_GUI(self):

        self.back_button_width = 150
        self.back_button_height = 60
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (0, (Settings.HEIGHT - self.back_button_height)), #Position
                (self.back_button_width, self.back_button_height)), #Size
            text='BACK',
            manager=self.ui_manager
        )

        self.tutorial_page_num = ["1/7", "2/7", "3/7", "4/7", "5/7", "6/7", "7/7"]
        self.tutorial_page_name = ["EXPLAINATION", "CONTROLS", "GOAL", "GAMEPLAY", "WINNING MONEY", "ALARMS", "POLICE"]
        self.page_index = 0

        self.page_name_width = 200
        self.page_name_height = 50
        self.page_name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.page_name_width / 2)), 30), #Position
                (self.page_name_width, self.page_name_height)),  #Size
            text=self.tutorial_page_name[self.page_index],  # Show current option
            manager=self.ui_manager
        )

        self.page_select_width = 50
        self.page_select_height = 50
        self.page_label_width = 150
        self.page_label_heigth = 50

        self.page_num_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.page_label_width / 2)), (Settings.HEIGHT - self.page_select_height)), #Position
                (self.page_label_width, self.page_label_heigth)),  #Size
            text=self.tutorial_page_num[self.page_index],  # Show current option
            manager=self.ui_manager
        )
        self.page_left = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.page_label_width / 2) - (self.page_select_width)), (Settings.HEIGHT - self.page_select_height)), #Position
                (self.page_select_width, self.page_select_height)),  #Size
            text='<',
            manager=self.ui_manager
        )
        self.page_right = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) + (self.page_label_width / 2)), (Settings.HEIGHT - self.page_select_height)), #Position
                (self.page_select_width, self.page_select_height)),  #Size
            text='>',
            manager=self.ui_manager
        )


        textbox_width = 800
        textbox_height = 200
        self.default_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(
                ((Settings.WIDTH/2 - textbox_width/2), (Settings.HEIGHT/2 - textbox_height/2)), #Position
                (textbox_width, textbox_height)), #Size
            html_text = 
            'You and up to 4 players are placed in various shopping malls '
            'and are tasked with choosing stores to rob in order to '
            'make the most amount of money, all while avoiding '
            'being caught by the police!',
            manager=self.ui_manager
        )

        control_scheme_width = 1000
        control_scheme_height = 580
        self.control_schemes = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(
                ((Settings.WIDTH/2 - control_scheme_width/2), (Settings.HEIGHT/2 - control_scheme_height/2)), #Position
                (control_scheme_width, control_scheme_height)), #Size
            html_text = 
            '---Keyboard 1--- <br>'
            'Movement:  Up - W  |  Down - S  |  Left - A  |  Right - D<br>'
            'Interaction:  Select - 1  |  Cash Out - 2  |  Pause/Menu - SHIFT+S<br><br>'
            '---Keyboard 2---<br>'
            'Movement:  Up - T  |  Down - G  |  Left - F  |  Right - H<br>'
            'Interaction:  Select - 3  |  Cash Out - 4  |  Pause/Menu - SHIFT+S<br><br>'
            '---Keyboard 3---<br>'
            'Movement:  Up - I  |  Down - K  |  Left - J  |  Right - L<br>'
            'Interaction:  Select - 5  |  Cash Out - 6  |  Pause/Menu - SHIFT+S<br><br>'
            '---Keyboard 4---<br>'
            'Movement:  Arrow Keys<br>'
            'Interaction:  Select - 7  |  Cash Out - 8  |  Pause/Menu - SHIFT+S<br><br>'
            '---Controller---<br>'
            'Movement:  Right Joystick or D-pad<br>'
            'Interaction:  Select - South Button  |  Cash Out - East Button  |  Pause/Menu - Start Button',
            manager=self.ui_manager
        )

        goal_text_width = 800
        goal_text_height = 200
        self.goal_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(
                ((Settings.WIDTH/2 - goal_text_width/2), (Settings.HEIGHT/2 - goal_text_height/2)), #Position
                (goal_text_width, goal_text_height)), #Size
            html_text = 
            "The player who passes the goal amount of money the furthest "
            "wins. Once a player cashes out past the goal amount, all the "
            "other players only have the remainder of that mall to try "
            "and make the most amount of money to win.",
            manager=self.ui_manager
        )

        gameplay_text_width = 800
        gameplay_text_height = 200
        self.gameplay_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(
                ((Settings.WIDTH/2 - gameplay_text_width/2), (Settings.HEIGHT/2 - gameplay_text_height/2)), #Position
                (gameplay_text_width, gameplay_text_height)), #Size
            html_text = 
            "All players will start in a mall and walk around to find "
            "stores with desirable risk and rewards. Once all players "
            "have either selected a store to rob or cashed out their "
            "cash-on-hand, the players will initiate their robbery "
            "and find out how much they grabbed, if they set off an "
            "alarm, or if the police arrived.",
            manager=self.ui_manager
        )

        money_text_width = 800
        money_text_height = 200
        self.money_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(
                ((Settings.WIDTH/2 - money_text_width/2), (Settings.HEIGHT/2 - money_text_height/2)), #Position
                (money_text_width, money_text_height)), #Size
            html_text = 
            "If you won money, you now have that amount as cash-on-hand "
            "and can either cash out before the next robbery, leave the mall, "
            "and put it in your vault or you can try your luck with another robbery.",
            manager=self.ui_manager
        )

        alarm_text_width = 800
        alarm_text_height = 200
        self.alarm_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(
                ((Settings.WIDTH/2 - alarm_text_width/2), (Settings.HEIGHT/2 - alarm_text_height/2)), #Position
                (alarm_text_width, alarm_text_height)), #Size
            html_text = 
            "If an alarm is set off at your store, you lose your "
            "cash-on-hand and can no longer rob from that store. "
            "This also alerts the police and raises the chances "
            "of the police showing up and arresting everyone in the mall.",
            manager=self.ui_manager
        )

        police_text_width = 800
        police_text_height = 200
        self.police_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(
                ((Settings.WIDTH/2 - police_text_width/2), (Settings.HEIGHT/2 - police_text_height/2)), #Position
                (police_text_width, police_text_height)), #Size
            html_text = 
            "If the police show up, everyone who is still at the mall "
            "gets removed and loses everything they have stored in their vault.",
            manager=self.ui_manager
        )

    def hide_GUI(self):
        self.default_text.hide()
        self.control_schemes.hide()
        self.goal_text.hide()
        self.gameplay_text.hide()
        self.money_text.hide()
        self.alarm_text.hide()
        self.police_text.hide()

    def run(self):
        self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui
        self.update()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.scene_manager.quit()
            
            self.ui_manager.process_events(event) #Update pygame_gui

            if event.type == pygame.KEYDOWN:
                # Scene Selection
                if event.key == pygame.K_s:
                    self.scene_manager.switch_scene('scene')

            if event.type == pygame.USEREVENT:
                # Check if a button was clicked
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    #Back Button
                    if event.ui_element == self.back_button:
                        self.scene_manager.switch_scene('menu')
                    
                    #Page Change
                    if event.ui_element == self.page_left or event.ui_element == self.page_right:
                        if event.ui_element == self.page_left:
                            self.page_index -= 1
                        if event.ui_element == self.page_right:
                            self.page_index += 1

                        self.page_index %= len(self.tutorial_page_num)  #Wrap list
                        self.page_num_label.set_text(self.tutorial_page_num[self.page_index])
                        self.page_name_label.set_text(self.tutorial_page_name[self.page_index])

                        self.hide_GUI()
                        match self.page_index:
                            case 0:
                                self.default_text.show()
                            case 1:
                                self.control_schemes.show()
                            case 2:
                                self.goal_text.show()
                            case 3:
                                self.gameplay_text.show()
                            case 4:
                                self.money_text.show()
                            case 5:
                                self.alarm_text.show()
                            case 6:
                                self.police_text.show()
                                



    def render(self):
        self.screen.fill((255, 255, 255))
        tutorial_header = self.HEADER_FONT.get_rect("TUTORIAL")
        tutorial_header.center = ((Settings.WIDTH / 2), (Settings.HEADER_FONT_SIZE/2) + 10)
        self.HEADER_FONT.render_to(self.screen, tutorial_header, "TUTORIAL", (0, 0, 0))

        #Render pygame_gui
        self.ui_manager.update(self.time_delta)
        self.ui_manager.draw_ui(self.screen) 

        pygame.display.flip()