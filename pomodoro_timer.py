import tkinter as tk
import pygame

pygame.mixer.init()

window = tk.Tk()  # window is the name of the main window object
window.title('Focus Timer')
t_txt = 'Time remaining: {m} Minutes {s} Seconds'
foc_txt = 'Focus Session {x}'
rest_txt = 'Rest Session {x}'
start_focus_sound = pygame.mixer.Sound("startFocus.wav")
rest_sound = pygame.mixer.Sound("finishFocus.wav")
long_rest_sound = pygame.mixer.Sound("finishFourthFocus.wav")


def callback():
    print("Exiting now")
    # TODO I need to log the session data here before the application closes
    
    # File format:
    # [Date]
    # [NumFocus],[FocLength]
    # [NumRest],[RestLength]

    window.destroy()


def pause_pressed(pbt, _timer):

    if pbt.get() == "Pause":
        pbt.set("Resume")
        _timer.pause()
    else:
        pbt.set("Pause")
        _timer.resume()


class Timer:
    # setup class variables
    num_focus = 1
    num_rest = 1
    seconds = 1
    minutes = 0
    total_seconds = 0
    focus_length = 1
    rest_length = 1
    is_paused = False

    def get_num_focus(self):
        return self.num_focus

    def get_num_rest(self):
        return self.num_rest

    def get_focus_length(self):
        return self.focus_length

    def get_rest_length(self):
        return self.rest_length

    def __init__(self, parent):
        # label displaying time
        self.time_label = tk.Label(parent, text=t_txt.format(m=self.minutes, s=self.seconds), width=30)
        self.time_label.config(background='black', foreground="white")
        self.session_label = tk.Label(parent, text=foc_txt.format(x=self.num_focus))
        self.session_label.config(background='black', foreground="white")
        # put widgets onto display
        self.session_label.pack()
        self.time_label.pack()

        # start the timer
        self.time_label.after(0, self.start_focus_session)

    def start_focus_session(self):
        # setup in order to run a focus session.
        self.seconds = 0
        self.minutes = self.focus_length
        pygame.mixer.Sound.play(start_focus_sound)

        # update labels
        self.time_label.configure(text=t_txt.format(m=self.minutes, s=self.seconds))
        self.session_label.configure(text=foc_txt.format(x=self.num_rest))

        self.time_label.after(1000, self.focus_session_loop)  # start the focus loop after 1s

    def focus_session_loop(self):
        if not self.is_paused:
            self.seconds -= 1
            if self.seconds < 0:
                self.minutes -= 1
                self.seconds = 59
                if self.minutes < 0:
                    # focus session has ended
                    self.num_focus += 1

                    self.time_label.after(0, self.start_rest_session)  # start a rest session

            # display the new time
            self.time_label.configure(text=t_txt.format(m=self.minutes, s=self.seconds))
            self.time_label.after(1000, self.focus_session_loop)  # refresh after 1s

    def start_rest_session(self):
        # setup in order to run a focus session.
        self.seconds = 0
        if self.num_rest % 4 == 0:
            self.minutes = self.rest_length*4
            pygame.mixer.Sound.play(long_rest_sound)  # play long rest sound
        else:
            self.minutes = self.rest_length
            pygame.mixer.Sound.play(rest_sound)  # play rest sound

        # update labels
        self.time_label.configure(text=t_txt.format(m=self.minutes, s=self.seconds))
        self.session_label.configure(text=rest_txt.format(x=self.num_rest))

        self.time_label.after(1000, self.rest_session_loop)  # start the rest loop

    def rest_session_loop(self):
        if not self.is_paused:
            self.seconds -= 1
            if self.seconds < 0:
                self.seconds = 59
                self.minutes -= 1
                if self.minutes < 0:
                    # once rest session ends, start another focus session
                    self.num_rest += 1
                    self.time_label.after(0, self.start_focus_session)

            # display the new time
            self.time_label.configure(text=t_txt.format(m=self.minutes, s=self.seconds))
            self.time_label.after(1000, self.rest_session_loop)  # refresh after 1s

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

        # now we need to push back into the loop.
        if self.num_focus > self.num_rest:  # this means that we are currently in a rest session
            self.time_label.after(1000, self.rest_session_loop)
        else:
            self.time_label.after(1000, self.focus_session_loop)


# Below here is the "main"

# initialize objects
welcome_label = tk.Label(window, text='Welcome to Focus Timer', background='black', foreground="white")
welcome_label.pack()
timer = Timer(window)
pause_button_text = tk.StringVar()
pause_button_text.set("Pause")
pause_button = tk.Button(window, textvariable=pause_button_text, width=30, highlightbackground='black',
                         highlightthickness=20, command=lambda: pause_pressed(pause_button_text, timer))


pause_button.pack()

window.configure(background='black')
window.protocol("WM_DELETE_WINDOW", callback)  # this line let's me override the application quit method.
window.mainloop()  # run the Tk program loop
