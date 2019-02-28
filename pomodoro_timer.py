import time
import sys
import pygame
pygame.init()


def check_for_events(pause_text_rect):
    # returns 1 if pause_button_res should be changed.
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        m1, m2, m3 = pygame.mouse.get_pressed()
        if m1 == 1:  # if left mouse is being pressed.
            pos1, pos2 = pygame.mouse.get_pos()
            if pause_text_rect.collidepoint(pos1, pos2):
                return 1
    return 0


# TODO make GUI look a bit better.
# TODO make the pause button pause the clock.
# TODO change time elapsed to time remaining.
def main():
    focus_length = 21
    break_length = 4
    start_focus_sound = pygame.mixer.Sound("finishFocus.wav")
    finish_focus_sound = pygame.mixer.Sound("finishFourthFocus.wav")
    long_break_sound = pygame.mixer.Sound("finishFourthFocus.wav")
    num_focus = 1
    num_break = 1
    seconds = 1
    minutes = 0
    total_seconds = 0

    # string resouces
    pause_button_res = "PAUSE"
    # main_text_res = " Welcome to the Pomodoro Timer "
    
    # set up the window
    canvas_width = 500
    canvas_height = 400
    widow_surface = pygame.display.set_mode((canvas_width, canvas_height), 0, 32)
    pygame.display.set_caption('Pomodoro Timer')

    # set up the colors
    text_color = (255, 255, 255)
    text_background_color = (0, 0, 0)
    focus_background_color = (0, 0, 0)
    rest_background_color = (0, 0, 0)

    # set up fonts
    basic_font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 40)

    # set up object coordinates
    welcome_text_coord = [250, 300]
    pause_text_coord = [420, 50]
    session_text_coord = [canvas_width/2, 150]
    time_text_coord = [widow_surface.get_rect().centerx, widow_surface.get_rect().centery]

    # set up the text
    welcome_text = basic_font.render(" Welcome to the Pomodoro Timer ", True, text_color, text_background_color)
    welcome_text_rect = welcome_text.get_rect()
    welcome_text_rect.centerx = welcome_text_coord[0]
    welcome_text_rect.centery = welcome_text_coord[1]
    pause_text = big_font.render(pause_button_res, True, text_color, text_background_color)
    pause_text_rect = pause_text.get_rect()
    pause_text_rect.centerx = pause_text_coord[0]
    pause_text_rect.centery = pause_text_coord[1]

    # draw the white background onto the surface
    widow_surface.fill(focus_background_color)
    widow_surface.blit(welcome_text, welcome_text_rect)
    widow_surface.blit(pause_text, pause_text_rect)
    pygame.display.update()  # draw the window onto the screen
    
    while True:
        if check_for_events(pause_text_rect) == 1:
            if pause_button_res == "RESUME":
                pause_button_res = "PAUSE"
            elif pause_button_res == "PAUSE":
                pause_button_res = "RESUME"
            pause_text = big_font.render(pause_button_res, True, text_color, text_background_color)
            pause_text_rect = pause_text.get_rect()
            pause_text_rect.centerx = pause_text_coord[0]
            pause_text_rect.centery = pause_text_coord[1]
            pygame.display.flip()

        # adds in session text
        session_text = basic_font.render(
            "Focus session {x}".format(x=num_focus), True, text_color, text_background_color)
        session_text_rect = session_text.get_rect()
        session_text_rect.centerx = session_text_coord[0]
        session_text_rect.centery = session_text_coord[1]
        # update screen
        widow_surface.fill(focus_background_color)
        widow_surface.blit(welcome_text, welcome_text_rect)
        widow_surface.blit(pause_text, pause_text_rect)
        widow_surface.blit(session_text, session_text_rect)
        pygame.display.flip()
    
        # play sound
        pygame.mixer.Sound.play(start_focus_sound)
    
        while total_seconds < focus_length*60:
            # update time text
            time_text = basic_font.render(
                " Time elapsed: {minutes} Minutes {seconds} Seconds ".format(minutes=minutes, seconds=seconds), True,
                text_color, text_background_color)
            time_text_rect = time_text.get_rect()
            time_text_rect.centerx = time_text_coord[0]
            time_text_rect.centery = time_text_coord[1]
    
            # update screen
            widow_surface.fill(focus_background_color)
            widow_surface.blit(welcome_text, welcome_text_rect)
            widow_surface.blit(pause_text, pause_text_rect)
            widow_surface.blit(time_text, time_text_rect)
            widow_surface.blit(session_text, session_text_rect)
            pygame.display.flip()
    
            # other operations
            loop_range = 8
            for x in range(loop_range):
                if check_for_events(pause_text_rect) == 1:
                    if pause_button_res == "RESUME":
                        pause_button_res = "PAUSE"
                    elif pause_button_res == "PAUSE":
                        pause_button_res = "RESUME"
                    pause_text = big_font.render(pause_button_res, True, text_color, text_background_color)
                    pause_text_rect = pause_text.get_rect()
                    pause_text_rect.centerx = pause_text_coord[0]
                    pause_text_rect.centery = pause_text_coord[1]
                    pygame.display.flip()

                time.sleep((1/loop_range))
    
            total_seconds += 1
            seconds += 1
            if seconds >= 60:
                minutes += 1
                seconds = 0
    
        # play sound and reset variables
        pygame.mixer.Sound.play(finish_focus_sound)
        minutes = 0
        seconds = 1
        total_seconds = 0
        num_focus += 1
    
        if (num_focus-1) % 4 == 0:
            session_text = basic_font.render(
                " Time for a long break! ".format(x=(break_length * 4)), True, text_color, text_background_color)
            session_text_rect = session_text.get_rect()
            session_text_rect.centerx = session_text_coord[0]
            session_text_rect.centery = session_text_coord[1]
    
            # update screen
            widow_surface.fill(rest_background_color)
            widow_surface.blit(welcome_text, welcome_text_rect)
            widow_surface.blit(pause_text, pause_text_rect)
            widow_surface.blit(session_text, session_text_rect)
            pygame.display.flip()
    
            # other operations
            temp = break_length * 60 * 4
            pygame.mixer.Sound.play(long_break_sound)
        else:
            session_text = basic_font.render(
                " Rest session {x} ".format(x=num_break), True, text_color, text_background_color)
            session_text_rect = session_text.get_rect()
            session_text_rect.centerx = session_text_coord[0]
            session_text_rect.centery = session_text_coord[1]
    
            # update screen
            widow_surface.fill(rest_background_color)
            widow_surface.blit(welcome_text, welcome_text_rect)
            widow_surface.blit(pause_text, pause_text_rect)
            widow_surface.blit(session_text, session_text_rect)
            pygame.display.update()
            pygame.display.flip()
    
            # other operations
            temp = break_length * 60
    
        while total_seconds < temp:
            # update time text
            time_text = basic_font.render(
                " Time elapsed: {minutes} Minutes {seconds} Seconds ".format(minutes=minutes, seconds=seconds), True,
                text_color, text_background_color)
            time_text_rect = time_text.get_rect()
            time_text_rect.centerx = time_text_coord[0]
            time_text_rect.centery = time_text_coord[1]
    
            # update screen
            widow_surface.fill(rest_background_color)
            widow_surface.blit(welcome_text, welcome_text_rect)
            widow_surface.blit(pause_text, pause_text_rect)
            widow_surface.blit(time_text, time_text_rect)
            widow_surface.blit(session_text, session_text_rect)
            pygame.display.flip()
    
            # pomodoro stuff
            time.sleep(1)
            total_seconds += 1
            seconds += 1
            if seconds >= 60:
                minutes += 1
                seconds = 0
            if check_for_events(pause_text_rect) == 1:
                if pause_button_res == "RESUME":
                    pause_button_res = "PAUSE"
                elif pause_button_res == "PAUSE":
                    pause_button_res = "RESUME"
                pause_text = big_font.render(pause_button_res, True, text_color, text_background_color)
                pause_text_rect = pause_text.get_rect()
                pause_text_rect.centerx = time_text_coord[0]
                pause_text_rect.centery = time_text_coord[1]
                pygame.display.flip()
    
        minutes = 0
        seconds = 1
        total_seconds = 0
        num_break += 1


main()
