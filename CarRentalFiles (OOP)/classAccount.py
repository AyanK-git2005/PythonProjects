
from abc import ABC, abstractmethod


class Account(ABC):
    '''An Abstract Base class containing two methods'''

    @abstractmethod
    def login(self): pass
    # An Abstract method implemented in AdministratorAccount and UserAccount Classes


    def logout(self):
        print('\nLogged Out Successfully!')
