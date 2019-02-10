import tkinter as tk
import tkinter.ttk as ttk
import json

root = tk.Tk()
root.resizable(False, False)

combobox_and_calendar_frame = tk.Frame(root)
combobox_and_calendar_frame.pack(side='left', fill='both', expand=1)
perma_frame, redraw_frame = tk.Frame(combobox_and_calendar_frame), tk.Frame(combobox_and_calendar_frame)
perma_frame.pack(side='top'), redraw_frame.pack(side='top')
hours_frame = tk.Frame(root)
hours_frame.pack(side='left')

diff_months = {'January': [1, 31], 'February': [2, 28], 'March': [3, 31], 'April': [4, 30], 'May': [5, 31],
               'June': [6, 30], 'July': [7, 31], 'August': [8, 31], 'September': [9, 30], 'October': [10, 31],
               'November': [11, 30], 'December': [12, 31]}
hours = ['8 AM:', '9 AM:', '10AM:', '11AM:', '12AM:', '1 PM:', '2 PM:', '3 PM:', '4 PM:', '5 PM:', '6 PM:']

try:
    with open('data.json', 'r+', encoding='utf-8') as file:
        year = json.load(file)

        assert len(year) == 12
        for month in diff_months:
            assert month in year
        for month in diff_months:
            assert len(year[month]) == diff_months[month][1]
        for month in diff_months:
            for day in year[month]:
                assert len(year[month][day]) == 11
                for hour in year[month][day]:
                    assert hour in hours
except (FileNotFoundError, AssertionError):
    year = {}

    for x in diff_months:
        year[x] = {}
    for x in year:
        temp_day = 1
        while len(year[x]) < diff_months[x][1]:
            year[x][temp_day] = {}
            temp_day += 1
        else:
            temp_day = 1
    for x in year:
        for y in year[x]:
            for z in hours:
                year[x][y][z] = ''

months_txt = tk.Label(perma_frame, text="Months:")
months_txt.pack()
months_drop = ttk.Combobox(perma_frame, values=list(diff_months.keys()))
months_drop.set('January')
months_drop.pack()


class HourButton:
    def __init__(self, master, month, day, hour, **kwargs):
        self.button = tk.Button(master, **kwargs)
        self.month = month
        self.day = day
        self.hour = hour
        self.name = ''

    def toggle_name(self):
        if not self.name:
            self.name = update_field.get()
            year[self.month][self.day][self.hour] = self.name
        else:
            self.name = ''
            year[self.month][self.day][self.hour] = ''
        self.button.config(text=self.name)


class WrappedButton:

    currently_displayed = None

    def __init__(self, master, month, day, **kwargs):
        self.button = tk.Button(master, **kwargs)
        self.month = month
        self.day = str(day)

    def display_hours(self):
        global update_field
        tk.Label(hours_frame, text='Enter text and click a timeslot to store it there.').pack(side='top')
        update_field = tk.Entry(hours_frame, width=50)
        update_field.pack(side='top')
        hour_label_frame, hour_button_frame = tk.Frame(hours_frame), tk.Frame(hours_frame)
        hour_label_frame.pack(side='left'), hour_button_frame.pack(side='left')
        for x in range(11):
            tk.Label(hour_label_frame, text=hours[x], pady=4).pack(side='top')
            temp = HourButton(
                hour_button_frame,
                self.month,
                self.day,
                hours[x],
                height=1,
                width=40,
                anchor='w')
            temp.button.config(command=temp.toggle_name, text=year[temp.month][temp.day][temp.hour])
            temp.button.pack(side='top')
        self.button.config(bg='green')

    def hide_hours(self):
        for x in hours_frame.slaves():
            x.destroy()

    def hours_logic(self):
        if not WrappedButton.currently_displayed:
            WrappedButton.currently_displayed = self
            self.display_hours()
        elif WrappedButton.currently_displayed and WrappedButton.currently_displayed is self:
            WrappedButton.currently_displayed = None
            self.button.config(bg='SystemButtonFace')
            self.hide_hours()
        elif WrappedButton.currently_displayed not in (None, self):
            WrappedButton.currently_displayed.button.config(bg='SystemButtonFace')
            WrappedButton.currently_displayed = self
            try:
                entry_storage = update_field.get()
            except:
                pass
            self.hide_hours()
            self.display_hours()
            try:
                update_field.insert(0, entry_storage)
            except:
                pass



buttons = []


def draw_calendar(unused_event_info):
    WrappedButton.currently_displayed = None
    target_month = diff_months[months_drop.get()][0]

    for x in (redraw_frame.slaves(), hours_frame.slaves()):
        for y in x:
            y.destroy()

    rows = [tk.Frame(redraw_frame) for x in range(5)]
    [x.pack() for x in rows]

    current_day = 1

    for x in range(35):
        if len(rows[0].slaves()) == 7:
            rows.pop(0)
        temp = WrappedButton(rows[0], months_drop.get(), current_day, text='', height=2, width=4)
        temp.button.pack(side='left')
        buttons.append(temp)
        if current_day <= diff_months[months_drop.get()][1]:
            temp.button.config(text=current_day, command=temp.hours_logic)
            current_day += 1


months_drop.bind('<<ComboboxSelected>>', draw_calendar)
draw_calendar('_')


root.mainloop()
