import time
import sys
import pygame
pygame.init()

focus_length = 20
break_length = 5

start_focus_sound = pygame.mixer.Sound("begin_focus.wav")
finish_focus_sound = pygame.mixer.Sound("finishFocus.wav")
long_break_sound = pygame.mixer.Sound("finishFourthFocus.wav")
numFocus = 1
numBreak = 1
time_start = time.time()
seconds = 1
minutes = 0
totalSeconds = 0
long_break = False
#TODO add a pause feature.
#TODO change time elapsed to time remaining.

print("Welcome to the Focus Keeper, Maintain focus with the Pomodoro technique")
while True:
    print("\nBeginning focus session {x}, it will last {y} minutes.".format(x=numFocus, y=focus_length))
    pygame.mixer.Sound.play(start_focus_sound)
    while totalSeconds < focus_length*60:
        sys.stdout.write("\rTime elapsed: {minutes} Minutes {seconds} Seconds".format(minutes=minutes, seconds=seconds))
        sys.stdout.flush()
        time.sleep(1)
        totalSeconds += 1
        seconds += 1
        if seconds >= 60:
            minutes += 1
            seconds = 0

    pygame.mixer.Sound.play(finish_focus_sound)
    minutes = 0
    seconds = 1
    totalSeconds = 0
    numFocus += 1
    if (numFocus-1) % 4 == 0:
        print("\nYou have completed four focus sessions!"
              + "Time for a long break, It will last {x} minutes.".format(x=(break_length*4)))
        long_break = True
        temp = break_length * 60 * 4
        pygame.mixer.Sound.play(long_break_sound)
    else:
        print("\nBeginning rest session {x}, it will last {y} minutes.".format(x=numBreak, y=break_length))
        temp = break_length * 60

    while totalSeconds < temp:
        sys.stdout.write("\rTime elapsed: {minutes} Minutes {seconds} Seconds".format(minutes=minutes, seconds=seconds))
        sys.stdout.flush()
        time.sleep(1)
        totalSeconds += 1
        seconds += 1
        if seconds >= 60:
            minutes += 1
            seconds = 0

    minutes = 0
    seconds = 1
    totalSeconds = 0
    numBreak += 1
