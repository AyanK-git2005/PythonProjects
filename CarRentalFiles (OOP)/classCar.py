
from classExceptions import NegativeBalanceError
from classFile import File
from MiscFunc import updateID
import pickle


class Car:

    def __init__(self):
        self.carID=updateID(1)                                      # Increments the car ID tally
        
        while True:
            try:
                self.name=input('Enter the Car Name: ')
                if not self.name.isalpha():                         # Checks if the entry contains alphabets only
                    raise ValueError("Car Name must contain Alphabets only!")
                break
            except ValueError as e1:
                print('Error:',e1)

        while True:
            try:
                self.model=input('Enter the Car Model: ')
                if not self.model.isdigit():                        # Checks if the entry contains digits only
                    raise ValueError("Car Model must contain Digits only!")
                break
            except ValueError as e2:
                print('Error:',e2)

        while True:
            try:
                self.manufacturer=input('Enter the Car Manufacturer: ')
                if not self.manufacturer.isalpha():                 # Checks if the entry contains alphabets only
                    raise ValueError("Car Manufacturer must contain Alphabets only!")
                break
            except ValueError as e3:
                print('Error:',e3)

        while True:
            try:
                self.seats=input('Enter the Number of Seats: ')
                if not self.seats.isdigit():                        # Checks if the entry contains digits only
                    raise ValueError("No. of Seats of a Car must be a Positive Whole Number!")
                break
            except ValueError as e4:
                print('Error:',e4)

        while True:
            try:
                rate = int(input('Enter the Car\'s Rental Rate: PKR '))
                if rate <= 0:
                    raise NegativeBalanceError                      # Raises error if the entry is negative
                self.rate = rate
                break
            except ValueError:                                      # Raises error if the entry contains non-digits
                print("Car Rental Rate must contain Digits only!")
            except NegativeBalanceError as e5:
                print('Error:',e5)

        data=['C'+str(self.carID),self.name,str(self.model),self.manufacturer,
              str(self.seats)+' Seats','PKR '+str(self.rate)]       # Creates a list of car data points
        
        carFile=File('cars')
        carFile.update(data)                                        # Stores the car data list in a text file
        
        with open('Car'+str(self.carID)+'.pkl','wb') as cardata:
            pickle.dump(self,cardata)                               # Stores the car object in memory
