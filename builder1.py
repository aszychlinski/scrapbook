from dataclasses import dataclass


class User:
    def __init__(self, first_name: str, last_name: str, email: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __str__(self):
        return f'User(first_name={self.first_name}, last_name={self.last_name}, email={self.email})'

    @dataclass
    class BoringBuilder:
        _first_name: str = None
        _last_name: str = None
        _email: str = None
        test: object = None

        def first_name(self, first_name: str):
            self._first_name = first_name
            return self

        def last_name(self, last_name: str):
            self._last_name = last_name
            return self

        def email(self, email: str):
            self._email = email
            return self

        def build(self):
            return User(self._first_name, self._last_name, self._email)

    class CoolBuilder:
        def __init__(self):
            self.first_name = lambda x: self.__setattr__('first_name', x)
            self.last_name = lambda x: self.__setattr__('last_name', x)
            self.email = lambda x: self.__setattr__('email', x)
            self.build = lambda: User(self.first_name, self.last_name, self.email)

        def __setattr__(self, key, value):
            super().__setattr__(key, value)
            return self

    @classmethod
    def boring_builder(cls):
        return cls.BoringBuilder()

    @classmethod
    def cool_builder(cls):
        return cls.CoolBuilder()


a = User('Adam', 'Szychliński', 'as@unatco.org'); print(a)
b = User.boring_builder().first_name('Alex').last_name('Denton').email('ad@unatco.org').build(); print(b)
c = User.cool_builder().first_name('JC').last_name('Denton').email('jcd@unatco.org').build(); print(c)
