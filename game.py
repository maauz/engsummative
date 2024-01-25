import pygame
import os
import sys
import pygame_gui
from button import Button
import random
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT
# Game states
state_titlescreen = 0
state_intro = 1
state_exhibit1 = 2
state_chart = 3
state_exhibit2 = 4
state_chart2 = 5
state_exhibit3 = 6
state_chart3= 7
state_testbegins = 8
state_test = 9
state_fail = 10
state_passed = 11


Black = (0, 0, 0)
Red = ()
White = (255, 255, 255)
Orange = (255, 165, 0)

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 640
screen_height = 500
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Museum Of Canada's Dark Past")

# Initialize the Pygame mixer module once
pygame.mixer.init()

questions = [
    {
        "question": "What year did apartheid officially end in South Africa?",
        "choices": ["1990", "1992", "1994"],
        "correct_choice": 3,
    },
    {
        "question": "Which Canadian company paid all its workers a wage above the poverty line in South Africa?",
        "choices": ["Rio Tinto", "Ford Motor Company", "Massey Ferguson"],
        "correct_choice": 2,
    },
    {
        "question": "When did Canada impose sanctions against South Africa?",
        "choices": ["1985", "1988", "1990"],
        "correct_choice": 1,
    },
    {
        "question": "During the period of apartheid, what were the wage gaps between White and Black workers in Canadian companies in South Africa?",
        "choices": ["Equal pay", "White workers were paid less", "Black workers were paid less"],
        "correct_choice": 3,
    },
    {
        "question": "Which Canadian company was mentioned for unfairly paying its minority population, specifically Indigenous Peoples?",
        "choices": ["Rio Tinto Canadian Exploration Ltd", "Ford Motor Company of Canada", "Massey Ferguson"],
        "correct_choice": 3,
    },
    {
        "question": "In 1985, Canada took a historic stance against apartheid by imposing sanctions. What was the total two-way trade with South Africa from 1986 to 1993?",
        "choices": ["$500 million", "$1.6 billion", "$2.5 billion"],
        "correct_choice": 2,
    },
    {
        "question": "Despite public sanctions, Canada maintained close economic ties with South Africa. What was the average annual Canadian imports from South Africa during the sanctions period?",
        "choices": ["$50 million", "$100 million", "$122 million"],
        "correct_choice": 3,
    },
    {
        "question": "In the third exhibit, what did scholars say officials with Canada's Indian Affairs Department discussed with their counterparts in South Africa in the 1940s?",
        "choices": ["Economic policies", "Elements of the Indian Act", "Cultural exchanges"],
        "correct_choice": 2,
    },
]



class Game:
    def __init__(self, window, screen_width, screen_height):
        self.window = window
        self.screen_width = screen_width
        pygame.mixer.init()  
        self.screen_height = screen_height
        self.current_state = state_titlescreen
        self.base_font = pygame.font.Font(None, 36)
        self.user_text = ""
        self.enter_pressed = False
        self.transition_time = 0  # Timer in milliseconds
        self.transition_duration = 10000  # Duration in milliseconds
        self.manager = pygame_gui.UIManager((screen_width, screen_height))
        self.input_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(250, 100, 300, 40),
                                                                manager=self.manager)
        self.fact_index = 0
        self.display_timer = 0
        self.display_duration = 450  # in frames (assuming 60 FPS)
        self.max_text_length = 425  # Maximum characters before wrapping
        self.font_size = 20
        self.font = pygame.font.Font(None, self.font_size)  # Adjust the font size
        self.titlepagebg = pygame.image.load('images/Titlepage.png')
        self.titlepagebg = pygame.transform.scale(self.titlepagebg, (self.screen_width, self.screen_height))
        self.introbg = pygame.image.load('images/intro.png') 
        self.introbg = pygame.transform.scale(self.introbg, (self.screen_width, self.screen_height))
        self.exhibit1bg = pygame.image.load('images/firstexhibit.png')
        self.exhibit1bg = pygame.transform.scale(self.exhibit1bg, (self.screen_width, self.screen_height))
        self.chart1bg = pygame.image.load('images/chart1.png')
        self.chart1bg = pygame.transform.scale(self.chart1bg, (self.screen_width, self.screen_height))
        self.exhibit2bg= pygame.image.load('images/secondexhibit.png')
        self.exhibit2bg = pygame.transform.scale(self.exhibit2bg, (self.screen_width, self.screen_height))
        self.chart2bg = pygame.image.load('images/chart2.png')
        self.chart2bg = pygame.transform.scale(self.chart2bg, (self.screen_width, self.screen_height))
        self.chart3bg = pygame.image.load('images/chart3.png')
        self.exhibit3bg = pygame.image.load('images/thirdexhibit.png')
        self.exhibit3bg = pygame.transform.scale(self.exhibit3bg, (self.screen_width, self.screen_height))
        self.testbeginsbg = pygame.image.load('images/testbegins.png')
        self.testbeginsbg = pygame.transform.scale(self.testbeginsbg, (self.screen_width, self.screen_height))
        self.testbackgroundbg = pygame.image.load('images/testbackground.png')
        self.testbackgroundsbg = pygame.transform.scale(self.testbackgroundbg, (self.screen_width, self.screen_height))
        self.failbg = pygame.image.load('images/failed.png')
        self.failbg = pygame.transform.scale(self.failbg, (self.screen_width, self.screen_height))
        self.passedbg = pygame.image.load('images/passed.png')
        self.passedbg = pygame.transform.scale(self.passedbg, (self.screen_width, self.screen_height))
        self.back_button = pygame.image.load(os.path.join("sprites", "back.png"))
        self.back_button = pygame.transform.scale(self.back_button, (80, 80))
        self.back_button = Button(20, screen_height - 110, self.back_button, 0.8)


        self.clock = pygame.time.Clock()
        self.time_delta = self.clock.tick(60) / 1000.0
        self.start_button = pygame.image.load(os.path.join("sprites", "start.png"))
        self.start_button = pygame.transform.scale(self.start_button, (80, 80))
        self.start_button = Button(screen_width - 60, screen_height - 110, self.start_button, 0.8)
        self.next_button = pygame.image.load(os.path.join("sprites", "next.png"))
        self.next_button = pygame.transform.scale(self.next_button, (80, 80))
        self.next_button = Button(screen_width - 60, screen_height - 110, self.next_button, 0.8)
        self.next2_button = pygame.image.load(os.path.join("sprites", "next2.png"))
        self.next2_button = pygame.transform.scale(self.next2_button, (80, 80))
        self.next2_button = Button(screen_width - 60, screen_height - 140, self.next2_button, 0.8)
        self.fact_index = 0  # Add this line to initialize fact_index
        self.songs = [
            os.path.join("music", "sleepytime.mp3"),
            os.path.join("music", "groovy.mp3"),
            os.path.join("music", "music_TheAdventureBegins.mp3"),
        ]
        self.current_song_index = 0
        self.load_random_song()
        self.current_question_index = 0
        self.selected_choice = 0
        self.score = 0

    def load_random_song(self):
        # Load a random song
        random.shuffle(self.songs)
        music_file = self.songs[self.current_song_index]
        print(f"Loading and playing music file: {music_file}")
        pygame.mixer.music.stop()

        # Load and play the new song
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)  # Start playing the loaded song, -1 to loop indefinitely

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.manager.process_events(event)

            # Calculate UI_REFRESH_RATE inside the loop
            self.UI_REFRESH_RATE = self.clock.tick(60) / 1000.0

            if self.current_state == state_titlescreen:
                self.handle_title_page()
            elif self.current_state == state_intro:
                self.handle_intro_page()
            elif self.current_state == state_exhibit1:
                self.handle_exhibit1()
            elif self.current_state == state_chart:
                self.handle_chart_screen()
            elif self.current_state == state_exhibit2:
                self.handle_exhibit2()
            elif self.current_state == state_chart2:
                self.handle_chart2_screen()
            elif self.current_state == state_exhibit3:
                self.handle_exhibit3()
            elif self.current_state == state_chart3:
                self.handle_chart3_screen()
            elif self.current_state == state_testbegins:
                self.handle_testbegins_screen()
            elif self.current_state == state_test:
                self.handle_test()
            elif self.current_state == state_fail:
                self.handle_fail()
            elif self.current_state == state_passed:
                self.handle_pass()
        

            pygame.display.update()
        
    def handle_title_page(self):
        self.window.blit(self.titlepagebg, (0, 0))
        self.load_random_song()
        
        # Adjust the position of the start button
        if self.start_button.draw(self.window):
            self.current_state = state_intro  

    def handle_intro_page(self):
        self.window.blit(self.introbg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.manager.process_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key pressed
                    self.user_text = self.input_entry.get_text()
                    self.enter_pressed = True
                    self.transition_time = pygame.time.get_ticks()  # Record the time when input is received

        if not self.enter_pressed:
            pygame.draw.rect(self.window, (255, 0, 0), self.input_entry.rect, 2)
            self.manager.draw_ui(self.window)
            self.manager.update(self.UI_REFRESH_RATE)  # Add this line to update the UI
        else:
            # Display welcome message
            welcome_text = f"Welcome, {self.user_text}!"
            welcome_surface = self.font.render(welcome_text, True, (255, 255, 255))
            welcome_rect = welcome_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.window.blit(welcome_surface, welcome_rect)

            current_time = pygame.time.get_ticks()
            if current_time - self.transition_time >= 5000:
                print("User input:", self.user_text)
                self.current_state = state_exhibit1
                self.enter_pressed = False  # Reset enter_pressed

        pygame.display.flip()
    def handle_exhibit1(self):
        self.window.blit(self.exhibit1bg, (0, 0))

        # List of facts for exhibit1
        exhibit1_facts = [
            f"Welcome to the first exhibit {self.user_text}!",
            "Make sure you take note of the specific facts I provide, there will be a test in the end.",
            "Before we begin you must know what apartheid Is.",
            "Apartheid, a system of racial segregation and discrimination, was enforced in South Africa from 1948 to 1994.",
            "Initially it aimed to just be system of segreation between Whites and Minority races.",
            "But it quickly escalated.",
            "An example of this is secret death squads created in South Africa resulting in thousands dead",
            "Okay now that you got a background check, the exhibit can truly begin.",
            "Canadian companies historically utilized discriminatory apartheid policies for economic gain.",
            "Businesses profited from discriminatory practices against Black workers in South Africa.",
            "Canadian investors included Rio Tinto Canadian Exploration Ltd, Aluminum Company of Canada Ltd., Ford Motor Company of Canada, and more.",
            "The Ford Motor Company of Canada was the only large Canadian corporation operating South Africa that paid all its workers a wage above the poverty line and the minimum level for it's city.",
            "Wage gaps between White and Black workers were prevalent, mirroring similar injustices faced by Indigenous populations in Canada.",
            "Massey Ferguson a primary Canadian business operating in South Africa, utilized the gap in pay between Whites and Blacks. ",
            "Of the 733 Black employees at the company's Vereeniging plant, 633 were paid less than the PDL for the area, which was $119 at the time",
            "Only White workers received above the MEL, which was $178.",
            f"Please examine the chart I'm about to show you {self.user_text}.",
        ]

        # Display the current fact near the top of the screen in a bigger font
        current_fact = exhibit1_facts[self.fact_index]
        fact_lines = self.wrap_text(current_fact, self.max_text_length)
        
        # Calculate the total height needed for the text
        total_height = len(fact_lines) * 20  # Adjust the spacing between lines

        # Draw each line of the fact
        for i, line in enumerate(fact_lines):
            fact_surface = pygame.font.Font(None, 20).render(line, True, (Black))
            fact_rect = fact_surface.get_rect(center=(self.screen_width // 2, 40 + total_height // 2 + i * 40))
            self.window.blit(fact_surface, fact_rect)
        for i, line in enumerate(fact_lines):
            fact_surface = pygame.font.Font(None, 20).render(line, True, (Black))
            fact_rect = fact_surface.get_rect(center=(self.screen_width // 2, 40 + total_height // 2 + i * 40))

            # Add a highlight rectangle behind the current line
            highlight_rect = pygame.Rect(fact_rect.left - 10, fact_rect.top - 5, fact_rect.width + 20, fact_rect.height + 10)
            pygame.draw.rect(self.window, (255, 255, 0), highlight_rect)  # Yellow highlight
            self.window.blit(fact_surface, fact_rect)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Show the next fact when right arrow key is pressed
                    self.fact_index += 1
                    if self.fact_index >= len(exhibit1_facts):
                        self.fact_index = len(exhibit1_facts) - 1  # Ensure it stays within bounds
                elif event.key == pygame.K_LEFT:
                    # Show the previous fact when left arrow key is pressed
                    self.fact_index -= 1
                    if self.fact_index < 0:
                        self.fact_index = 0  # Ensure it stays within bounds

        if self.next_button.draw(self.window):
            # Change state to state_chart when next button is pressed
            self.fact_index = 0  # Reset the fact index
            self.current_state = state_chart
        elif self.back_button.draw(self.window):
            # Go back to the previous state when back button is pressed
            self.current_state = state_intro
    def wrap_text(self, text, max_length):
        words = text.split()
        lines = []
        current_line = words[0]

        for word in words[1:]:
            if self.font.size(current_line + ' ' + word)[0] <= max_length:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        return lines

    def handle_chart_screen(self):
        # Display the chart background
        self.window.blit(self.chart1bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.manager.process_events(event)

        if self.next2_button.draw(self.window):
            self.current_state = state_exhibit2
        elif self.back_button.draw(self.window):
            self.current_state = state_exhibit1

        
    def handle_exhibit2(self):
        self.window.blit(self.exhibit2bg, (0, 0))
        # List of facts for exhibit2
        exhibit2_facts = [
            f"Welcome to the second exhibit {self.user_text}!",
            "Remember about the test; it's very important.",
            "You really don't want to fail.",
            "Anyways, the second exhibit is about Canada's public stance vs. their economic actions.",
            "In 1985, Canada took a historic stance against apartheid, imposing sanctions against South Africa.",
            "Despite public sanctions, Canada maintained close economic ties and trade relations with South Africa.",
            "From 1986 to 1993, Canada's two-way trade with South Africa totaled $1.6 billion.",
            "Canadian imports from South Africa averaged $122 million a year during the sanctions period.",
            "Canada's double approach raised questions about the consistency of its commitment to fighting racial oppression.",
            "Some argue that economic interests took precedence over human rights considerations.",
            "Activists within Canada called for a more principled stand against apartheid, urging a complete economic disengagement.",
            "The anti-apartheid act was introduced in Canada in 1986, pushing for stronger measures against South Africa.",
            "Despite criticism, the Canadian government continued to engage economically with South Africa until the end of apartheid.",
            "During this time when Canada publicly denounced South Africa for their human rights violation,",
            "Yet they continued with their own inhumane organizations and practices.",
            "This includes Residential Schools which closed after apartheid.",
            "More than 6000 kids died while at residential schools, and more were missing or committed suicide years after they attended.",
            "Lastly, similar to South Africa during apartheid, Canada also unfairly paid its minority population.",
            "In this case being Indigenous Peoples.",
            f"Please examine the chart I'm about to show you {self.user_text}.",
        ]
        # Display the current fact near the top of the screen in a bigger font
        current_fact = exhibit2_facts[self.fact_index]
        fact_lines = self.wrap_text(current_fact, self.max_text_length)
        
        # Calculate the total height needed for the text
        total_height = len(fact_lines) * 20  # Adjust the spacing between lines

        # Draw each line of the fact
        for i, line in enumerate(fact_lines):
            fact_surface = pygame.font.Font(None, 20).render(line, True, (Black))
            fact_rect = fact_surface.get_rect(center=(self.screen_width // 2, 40 + total_height // 2 + i * 40))
            self.window.blit(fact_surface, fact_rect)
        for i, line in enumerate(fact_lines):
            fact_surface = pygame.font.Font(None, 20).render(line, True, (Black))
            fact_rect = fact_surface.get_rect(center=(self.screen_width // 2, 40 + total_height // 2 + i * 40))

            # Add a highlight rectangle behind the current line
            highlight_rect = pygame.Rect(fact_rect.left - 10, fact_rect.top - 5, fact_rect.width + 20, fact_rect.height + 10)
            pygame.draw.rect(self.window, (255, 255, 0), highlight_rect)  # Yellow highlight
            self.window.blit(fact_surface, fact_rect)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Show the next fact when right arrow key is pressed
                    self.fact_index += 1
                    if self.fact_index >= len(exhibit2_facts):
                        self.fact_index = len(exhibit2_facts) - 1  # Ensure it stays within bounds
                elif event.key == pygame.K_LEFT:
                    # Show the previous fact when left arrow key is pressed
                    self.fact_index -= 1
                    if self.fact_index < 0:
                        self.fact_index = 0  # Ensure it stays within bounds

        if self.next_button.draw(self.window):
            # Change state to state_chart2 when next button is pressed
            self.fact_index = 0  # Reset the fact index
            self.current_state = state_chart2
        elif self.back_button.draw(self.window):
            # Go back to the previous state when back button is pressed
            self.current_state = state_chart
    def handle_chart2_screen(self):
        # Display the chart background
        self.window.blit(self.chart2bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.manager.process_events(event)

        if self.next2_button.draw(self.window):
            # Change state to state_chart when next button is pressed
            self.current_state = state_exhibit3
        elif self.back_button.draw(self.window):
            # Go back to the previous state when back button is pressed
            self.current_state = state_exhibit2
    def handle_exhibit3(self):
        self.window.blit(self.exhibit3bg, (0, 0))

        # List of facts for exhibit3
        exhibit3_facts = [
            f"Welcome to the third exhibit {self.user_text}!",
            "It is too late to go back; make sure you are prepared for the test.",
            "I'll make this exhibit shorter so you have less to study.",
            "This exhibit is about the similarities between the Indian Act and the apartheid system.",
            "Canada's treatment of Indigenous peoples is infamous for being unfair and unjust.",
            "This is proven by the creation of Residential schools, which ran from 1831 to 1996, the passing of many discriminatory laws such as the Indian Act, and the disregard for many of the promises they made to the many Indigenous communities.",
            "These injustices done against Indigenous people parallel the many discriminatory laws implemented in apartheid.",
            "Grand Chief Grand Doug Kelly once stated:",
            "Is it not rich with irony that South Africa imposed its legislation on those peoples, those tribes, in 1948, and they learned from the Indian Act of the government of Canada, that they built their apartheid system on the Indian Act in Canada?",
            "In the 1940s, scholars (not named in the sources found) say officials with Canada's Indian Affairs Department met with their counterparts in South Africa in the 1940s to discuss elements of the Indian Act that were eventually incorporated into apartheid.",
            "This included pass laws implemented in South Africa that required Black South Africans to obtain a pass to leave their town or village.",
            "This is very similar to a pass system implemented in most provinces in Canada a century ago, which required First Nations to obtain a pass from their local Indian agent to leave their reserve.",
            f"Please examine the infographic I made for you {self.user_text}.",
        ]

        # Display the current fact near the top of the screen in a bigger font
        current_fact = exhibit3_facts[self.fact_index]
        fact_lines = self.wrap_text(current_fact, self.max_text_length)
        
        # Calculate the total height needed for the text
        total_height = len(fact_lines) * 20  # Adjust the spacing between lines

        # Draw each line of the fact
        for i, line in enumerate(fact_lines):
            fact_surface = pygame.font.Font(None, 20).render(line, True, (Black))
            fact_rect = fact_surface.get_rect(center=(self.screen_width // 2, 40 + total_height // 2 + i * 40))
            self.window.blit(fact_surface, fact_rect)
        for i, line in enumerate(fact_lines):
            fact_surface = pygame.font.Font(None, 20).render(line, True, (Black))
            fact_rect = fact_surface.get_rect(center=(self.screen_width // 2, 40 + total_height // 2 + i * 40))

            # Add a highlight rectangle behind the current line
            highlight_rect = pygame.Rect(fact_rect.left - 10, fact_rect.top - 5, fact_rect.width + 20, fact_rect.height + 10)
            pygame.draw.rect(self.window, (255, 255, 0), highlight_rect)  # Yellow highlight
            self.window.blit(fact_surface, fact_rect)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Show the next fact when right arrow key is pressed
                    self.fact_index += 1
                    if self.fact_index >= len(exhibit3_facts):
                        self.fact_index = len(exhibit3_facts) - 1  # Ensure it stays within bounds
                elif event.key == pygame.K_LEFT:
                    # Show the previous fact when left arrow key is pressed
                    self.fact_index -= 1
                    if self.fact_index < 0:
                        self.fact_index = 0  # Ensure it stays within bounds

        if self.next_button.draw(self.window):
            self.fact_index = 0  # Reset the fact index
            self.current_state = state_chart3
        elif self.back_button.draw(self.window):
            # Go back to the previous state when back button is pressed
            self.current_state = state_chart2
    def handle_chart3_screen(self):
        # Fill the background with black color
        self.window.fill(Black)

        # Calculate the position to center the infographic
        infographic_rect = self.chart3bg.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        # Display the chart3 background without scaling in the center of the screen
        self.window.blit(self.chart3bg, infographic_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.manager.process_events(event)

        if self.next2_button.draw(self.window):
            # Change state to state_chart when next button is pressed
            self.current_state = state_testbegins
        elif self.back_button.draw(self.window):
            # Go back to the previous state when back button is pressed
            self.current_state = state_exhibit3
    def handle_testbegins_screen(self):
        self.window.blit(self.testbeginsbg, (0, 0))
        if self.next2_button.draw(self.window):
            # Change state to state_chart when next button is pressed
            self.current_state = state_test    

    def handle_test(self):
        self.window.blit(self.testbackgroundbg, (0, 0))

        current_question = questions[self.current_question_index]
        question_text = current_question["question"]
        choices = current_question["choices"]

        # Display the wrapped question at the top
        question_lines = self.wrap_text(question_text, self.max_text_length)
        question_y = 50  # Adjusted position from the top

        for i, line in enumerate(question_lines):
            question_surface = pygame.font.Font(None, 28).render(line, True, (Black))
            question_rect = question_surface.get_rect(center=(self.screen_width // 2, question_y + i * 30))
            self.window.blit(question_surface, question_rect)

        # Display the wrapped choices spread out
        choice_start_y = 150  # Adjusted starting position from the top

        for i, choice in enumerate(choices):
            choice_lines = self.wrap_text(choice, self.max_text_length)
            choice_height = len(choice_lines) * 30  # Adjusted for line height
            choice_y = choice_start_y + i * (choice_height + 20)  # Adjusted for vertical spacing

            for j, line in enumerate(choice_lines):
                choice_surface = pygame.font.Font(None, 24).render(line, True, (Black))
                choice_rect = choice_surface.get_rect(center=(self.screen_width // 2, choice_y + j * 30))

                # Add a highlight rectangle behind the current choice
                highlight_rect = pygame.Rect(
                    choice_rect.left - 10, choice_rect.top - 5, choice_rect.width + 20, choice_rect.height + 10
                )
                if i == self.selected_choice:
                    pygame.draw.rect(self.window, (255, 255, 0), highlight_rect)  # Yellow highlight

                self.window.blit(choice_surface, choice_rect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Move to the next choice
                    self.selected_choice = (self.selected_choice + 1) % len(choices)
                elif event.key == pygame.K_LEFT:
                    # Move to the previous choice
                    self.selected_choice = (self.selected_choice - 1) % len(choices)
                if event.key == pygame.K_RETURN:
                    # Check if the selected choice is correct
                    if self.selected_choice == current_question["correct_choice"] - 1:
                        self.score += 1  # Increase score for correct choice

                    # Move to the next question or transition to pass/fail screen
                    self.current_question_index += 1
                    self.selected_choice = 0

                    if self.current_question_index >= len(questions):
                        # Check the score and transition to the pass or fail screen
                        if self.score >= len(questions) // 2:
                            self.current_state = state_passed
                        else:
                            self.current_state = state_fail

        pygame.display.flip()
    def handle_fail(self):
        self.window.blit(self.failbg, (0, 0))

        # Display final score
        score_text = f"Your final score: {self.score} out of {len(questions)}, you should've paid attention {self.user_text}"
        score_surface = pygame.font.Font(None, 28).render(score_text, True, (Black))
        score_rect = score_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        self.window.blit(score_surface, score_rect)
        pygame.display.flip()

    def handle_pass(self):
        self.window.blit(self.passedbg, (0, 0))

        # Display final score
        score_text = f"Your final score: {self.score} out of {len(questions)}, hope you had fun {self.user_text}"
        score_surface = pygame.font.Font(None, 28).render(score_text, True, (Black))
        score_rect = score_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        self.window.blit(score_surface, score_rect)
        pygame.display.flip()
# Create a Game instance
game = Game(window, screen_width, screen_height)

# Run the game loop
game.run()