
from classAccount import Account
from classCar import Car
from classFile import File
import os


class AdministratorAccount(Account):
    '''Derived class from Account class.
    Handles Admin's functionalities.'''

    def login(self):
        'Logs in as administrator and returns the privilege'

        PW = 'admin@123'                                             # A pre-defined fixed admin password
        while True:
            passwordInput = input("Enter your Password (Or 'X' to go back): ")

            if passwordInput == PW:                                 # Checks if the entered password is correct
                print('You Logged in as Administrator Successfully!')
                break

            elif passwordInput == 'X' or passwordInput == 'x':      # An option to abort log in process
                return 'Back'
            
            else:
                print('Incorrect Password. Try Again!')
        return 'Admin'


    def addCar(self):
        'Adds cars to the car rental system database'
        
        while True:
            try:
                noOfCars = int(input('How many Cars you want to Add? '))
                break
            except ValueError as e:
                print('Error: Invalid input! Enter an integer')

        for n in range(noOfCars):
            print(f'Enter Details of Car {n+1}:\n')
            Car()                                                   # Instantiates car object
            print('\nCar Added Successfully!\n')


    def removeCar(self, ID):
        'Removes car of the specified ID from the car rental system database'

        if ID == 'X' or ID == 'x': return 'Removed'                 # An option to abort remove car process
        carFile=File('cars')

        try:
            if not ID[0] == 'C':
                raise NameError  
            carFile.shortlist(ID)                                   # Removes the car from a list of cars

            os.remove('Car'+ ID[1: ] + '.pkl')                      # Removes the car object from memory
            print(f'Car with ID {ID} Removed Successfully')
            return 'Removed'
        
        except:
            print(f'Car with ID {ID} not found in the list!')
            return 'Unfound'


    def reviewFeedback(self):
        'Displays user feedback in a proper format'

        print('\nThe Following is User Feedback:')
        with open('feedback.txt', 'r+') as feedbackFile:
            feedback = feedbackFile.read()                          # Reads the contents of feedback file
            print(feedback)


    def logout(self):
        'Logs out to Account Selection Menu'
        super().logout()
