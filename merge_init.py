Elf = type('Elf', (), {'__init__': lambda self: setattr(self, 'hp', 80)})
Archer = type('Archer', (), {'__init__': lambda self: setattr(self, 'arrows', 15)})
Nameable = type('Nameable', (), {'__init__': lambda self, *, name='': setattr(self, 'name', name)})
Hair = type('Hair', (), {'__init__': lambda self, *, hair='': setattr(self, 'hair', hair)})


class MergeInit(type):
    def __call__(cls, **kwargs):
        new = object.__new__(cls)
        for parent in cls.__bases__:
            my_args = {}
            if parent.__init__.__kwdefaults__:
                for arg in parent.__init__.__kwdefaults__:
                    if arg in kwargs:
                        my_args[arg] = kwargs[arg]
            parent.__init__(new, **my_args)
        return new


class Ranger(Elf, Archer, Nameable, Hair, metaclass=MergeInit):
    pass


r = Ranger(hair='blonde', name='Deedlit')
for attr in r.__dict__.items():
    print(f'{attr[0]}: {attr[1]}')
