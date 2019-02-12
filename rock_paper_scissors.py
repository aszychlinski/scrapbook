import tkinter as tk
import threading as th
from random import choice
from time import sleep
from sys import platform


def main():
    root = tk.Tk()
    root.geometry('300x325')
    root.title('Rock-Paper-Scissors')
    root.resizable(False, False)
    default_bg = root.cget('bg')
    windows = False

    if platform == 'win32':
        windows = True
        rock = '\u2BC2'
        paper = '2'
        scissors = '\u2700'
    else:
        rock = 'Rock'
        paper = 'Paper'
        scissors = 'Scissors'

    class RPSButton:
        def __init__(self, master, **kwargs):
            self.button = tk.Button(master, **kwargs)
            self.content = self.button['text']
            self.button['command'] = self.push_update

        def push_update(self):
            p1_content.set(self.content)

    class RPSSpinner(th.Thread):
        def __init__(self):
            th.Thread.__init__(self)
            self.kill = False

        def run(self):
            while not self.kill:
                cpu_content.set(choice([rock, paper, scissors]))
                sleep(0.05)
            return None

    class NotGlobalHehe:
        cpu_logic = RPSSpinner()
        player_wins = 0
        cpu_wins = 0

    def terminate_running_spinner():
        NotGlobalHehe.cpu_logic.kill = True
        sleep(0.1)
        root.destroy()

    def resolve_round():
        if not p1_content.get():
            pass
        else:
            go_button.config(state='disabled')
            [x.button.config(state='disabled') for x in (p1_r, p1_p, p1_s)]
            NotGlobalHehe.cpu_logic.kill = True
            sleep(0.1)
            p1, cpu = p1_content.get(), cpu_content.get()
            if p1 == cpu:
                round_result.config(text='DRAW', bg='yellow')
            elif (p1 == rock and cpu == scissors) or (p1 == paper and cpu == rock) or (p1 == scissors and cpu == paper):
                round_result.config(text='PLAYER WINS', bg='green')
                NotGlobalHehe.player_wins += 1
            elif (p1 == rock and cpu == paper) or (p1 == paper and cpu == scissors) or (p1 == scissors and cpu == rock):
                round_result.config(text='CPU WINS', bg='red')
                NotGlobalHehe.cpu_wins += 1
            score.config(text=f'{NotGlobalHehe.player_wins}:{NotGlobalHehe.cpu_wins}')
            restart_question.config(text='Play again?')
            restart_btn.config(state='normal', relief='raised', bg='green', text='YES')
            quit_btn.config(state='normal', relief='raised', bg='red', text='NO')

    def restart_round():
        NotGlobalHehe.cpu_logic = RPSSpinner()
        NotGlobalHehe.cpu_logic.start()
        sleep(0.1)
        go_button.config(state='normal')
        [x.button.config(state='normal') for x in (p1_r, p1_p, p1_s)]
        p1_choice.config(text='')
        restart_question.config(text=' ')
        restart_btn.config(state='disabled', relief='flat', bg=default_bg, text='')
        quit_btn.config(state='disabled', relief='flat', bg=default_bg, text='')

    top_frame, mid_frame, score_frame, bot_frame = tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
    [x.pack(side='top', fill='x') for x in (top_frame, mid_frame, score_frame, bot_frame)]

    # --- top_frame ---
    info_label = tk.Label(top_frame, text='Pick a symbol and click "Go!" to resolve a round.')
    info_label.pack(side='top', pady=5)

    # --- mid_frame ---
    p1_frame, versus_frame, cpu_frame = tk.Frame(mid_frame), tk.Label(mid_frame), tk.Label(mid_frame)
    [x.pack(side='top', fill='x') for x in (p1_frame, versus_frame, cpu_frame)]

    p1_content = tk.StringVar()
    cpu_content = tk.StringVar()

    p1_r = RPSButton(p1_frame, text=rock, width=8)
    p1_p = RPSButton(p1_frame, text=paper, width=8)
    p1_s = RPSButton(p1_frame, text=scissors, width=8)

    p1_r.button.pack(side='left', padx=5)
    p1_p.button.pack(side='left')
    p1_s.button.pack(side='left', padx=5)

    p1_choice = tk.Button(versus_frame, relief='groove', textvariable=p1_content, width=4)
    go_button = tk.Button(versus_frame, text='Go!', command=resolve_round)
    cpu_choice = tk.Button(versus_frame, relief='groove', textvariable=cpu_content, width=4)

    p1_choice.pack(side='left', padx=45, pady=5)
    go_button.pack(side='left', pady=5)
    cpu_choice.pack(side='left', padx=45, pady=5)

    NotGlobalHehe.cpu_logic.start()

    cpu_r = RPSButton(cpu_frame, text=rock, width=8, state='disabled', relief='sunken')
    cpu_p = RPSButton(cpu_frame, text=paper, width=8, state='disabled', relief='sunken')
    cpu_s = RPSButton(cpu_frame, text=scissors, width=8, state='disabled', relief='sunken')

    cpu_r.button.pack(side='right', padx=5)
    cpu_p.button.pack(side='right')
    cpu_s.button.pack(side='right', padx=5)

    # --- score_frame ---
    round_result = tk.Button(score_frame, relief='groove')
    round_result.pack(side='top', fill='x', pady=5)

    score_intro = tk.Label(score_frame, text='Current score:')
    score_intro.pack(side='top')

    player_label = tk.Label(score_frame, text='Player →', anchor='e')
    player_label.pack(side='left', fill='x', expand=1)

    score = tk.Button(score_frame,
                      text=f'{NotGlobalHehe.player_wins}:{NotGlobalHehe.cpu_wins}',
                      relief='groove',
                      width=7,
                      state='disabled')
    score.pack(side='left')

    cpu_label = tk.Label(score_frame, text='← CPU', anchor='w')
    cpu_label.pack(side='left', fill='x', expand=1)

    # --- bot_frame ---
    restart_question = tk.Label(bot_frame, text=' ')

    if windows:
        [x.button.config(font='Wingdings', width=3) for x in (p1_r, p1_p, p1_s, cpu_r, cpu_p, cpu_s)]
        [x.config(font='Wingdings', width=2) for x in (p1_choice, cpu_choice)]
    else:
        warning_bar = tk.Label(bot_frame, text='Non-Windows OS detected! Reverted to text mode.', bg='orange')
        warning_bar.pack(side='top')

    restart_question.pack(side='top')
    restart_btn = tk.Button(bot_frame, height=5, width=15, state='disabled', relief='flat', command=restart_round)
    quit_btn = tk.Button(bot_frame, height=5, width=15, state='disabled', relief='flat', command=exit)
    restart_btn.pack(side='left', expand=1, pady=5), quit_btn.pack(side='left', expand=1, pady=5)

    root.protocol('WM_DELETE_WINDOW', terminate_running_spinner)
    root.mainloop()


if __name__ == '__main__':
    main()
