import tkinter as tk


class App(tk.Tk):
    # note that the app IS vertically centered - it doesn't look like it but that's an optical illusion
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = 0  # 0: English, 1: mirrored English
        self.loc = {
            # menubar
            'file': ('File', 'eliF'),
            'main menu': ('Main Menu', 'uneM niaM'),
            'exit': ('Exit', 'tixE'),
            'change language': ('egaugnal egnahC', 'Change language'),
            # main menu
            'hello': ('Hello\n', 'olleH\n'),
            'go to settings': ('Go to Settings', 'sgnitteS ot oG'),
            # settings
            'increase by one': ('Increase by one', 'eno yb esaercnI'),
            'go to main menu': ('Go to Main Menu', 'uneM niaM ot oG')
        }

        self.shared_variable = tk.IntVar()
        self.shared_variable.set(5)

        self.current_view = MainMenu(self, self.lang)
        self.current_view.pack(expand=True)

        self.menu = MenuBar(self)
        self.config(menu=self.menu)
        self.geometry('300x200')
        self.mainloop()

    def update_menu(self):
        self.menu = MenuBar(self)
        self.config(menu=self.menu)

    def switch_language(self, current_view, targeted=False):
        if type(targeted) == int:
            self.lang = targeted
        else:
            self.lang = int(not self.lang)  # >_>

        self.change_view(current_view, current_view.__class__)
        self.update_menu()

    def change_view(self, old, new):
        old.destroy()
        self.current_view = new(self, self.lang)
        self.current_view.pack(expand=True)


class MenuBar(tk.Menu):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(
            label=self.master.loc['main menu'][self.master.lang],
            underline=0,
            command=lambda: self.master.change_view(self.master.current_view, MainMenu)
        )
        self.filemenu.add_separator()
        self.filemenu.add_command(label=self.master.loc['exit'][self.master.lang], underline=1, command=master.quit)
        self.add_cascade(label=self.master.loc['file'][self.master.lang], underline=0, menu=self.filemenu)

        self.langmenu = tk.Menu(self, tearoff=0)
        self.langmenu.add_command(
            label='English',
            underline=0,
            command=lambda: self.master.switch_language(self.master.current_view, 0)
        )
        self.langmenu.add_command(
            label='hsilgnE',
            underline=0,
            command=lambda: self.master.switch_language(self.master.current_view, 1)
        )
        self.add_cascade(label=self.master.loc['change language'][self.master.lang], underline=0, menu=self.langmenu)


class MainMenu(tk.Frame):
    def __init__(self, master, lang, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.hello = tk.Label(self, text=self.master.loc['hello'][lang])
        self.hello.pack()

        self.display1 = tk.Label(self, textvariable=self.master.shared_variable)
        self.display1.pack()

        self.settings_menu = tk.Button(
            self,
            text=self.master.loc['go to settings'][lang],
            command=lambda: self.master.change_view(self, SettingsMenu)
        )
        self.settings_menu.pack()


class SettingsMenu(tk.Frame):
    def __init__(self, master, lang, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.plus_one = tk.Button(
            self,
            text=self.master.loc['increase by one'][lang],
            command=lambda: self.master.shared_variable.set(self.master.shared_variable.get() + 1))  # <_<
        self.plus_one.pack()

        self.change_language = tk.Button(
            self,
            text=self.master.loc['change language'][lang],
            command=lambda: self.master.switch_language(self)
        )
        self.change_language.pack()

        self.main_menu = tk.Button(
            self,
            text=self.master.loc['go to main menu'][lang],
            command=lambda: self.master.change_view(self, MainMenu)
        )
        self.main_menu.pack()


if __name__ == '__main__':
    App()
