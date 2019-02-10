import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()
perma_frame, redraw_frame = tk.Frame(root), tk.Frame(root)
perma_frame.pack(side='top')
redraw_frame.pack(side='top')

diff_months = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

months_txt = tk.Label(perma_frame, text="Months:")
months_txt.pack()
months_drop = ttk.Combobox(perma_frame, values=list(diff_months.keys()))
months_drop.pack()

# this is obviously unfinished, but should illustrate the structure
infos = [  # year
    [  # january
        'durrrrrrrrr'  # january 1
    ],
    [  # february
        'beep!', 'boop!', 'something or other'  # february 1, 2, 3
    ]
]


class WrappedButton:
    def __init__(self, master, month, day, **kwargs):
        self.button = tk.Button(master, **kwargs)
        self.month_index = month - 1
        self.day_index = day - 1
        self.toplevel = False
        self.thing = None

    def close_popup(self):
        self.thing.destroy()
        self.toplevel = False
        self.thing = None

    def popup(self):
        while not self.toplevel:
            self.thing = tk.Toplevel()
            self.toplevel = True
            tk.Label(self.thing, text=infos[self.month_index][self.day_index]).pack()
            self.thing.protocol("WM_DELETE_WINDOW", self.close_popup)


buttons = []


def draw_calendar(unused_event_info):
    target_month = int(months_drop.get())

    for x in buttons:
        if x.thing:
            x.thing.destroy()
    for x in redraw_frame.slaves():
        x.destroy()

    rows = [tk.Frame(redraw_frame) for x in range(5)]
    [x.pack() for x in rows]

    current_day = 1

    for x in range(35):
        if len(rows[0].slaves()) == 7:
            rows.pop(0)
        temp = WrappedButton(rows[0], target_month, current_day, text='', height=1, width=2)
        temp.button.pack(side='left')
        buttons.append(temp)
        if current_day <= diff_months[target_month]:
            temp.button.config(text=current_day, command=temp.popup)
            current_day += 1


months_drop.bind('<<ComboboxSelected>>', draw_calendar)


root.mainloop()
