
from classExceptions import NegativeBalanceError
from classAccount import Account
from MiscFunc import updateID
from classFile import File
import pickle
import os


class UserAccount(Account):
    '''Derived class from Account class.
        Handles User's functionalities.'''

    def __init__(self):
        '''Instantiates a User Class Object.
        Assigns ID to the user and creates a user account'''

        self.userID = updateID(0)                                       # Increments user  ID tally
        self.currentRentID= None                                        # Initializes user reservation status to None
        print()

        while True:
            try:
                self.username = input('Enter Username: ')
                if not self.username.isalpha():                         # Checks if the entry contains alphabets only
                    raise ValueError("Username must contain only Alphabets.(No Spaces)")
                break
            except ValueError as e:
                print(f'Error: {e}')
        
        while True:
            PW = input('Create a strong Password: ')
            if len(PW) < 8:                                             # Checks if password is atleast 8 characters long
                print('Error: Password must contain atleast 8 Characters')
            elif PW.isalpha() or PW.isdigit():                          # Checks if password has both alphabets and digits
                print('Error: Password must contain both Alphabets and Digits')
            else: 
                self.password = PW
                break

        while True:
            try:
                self.firstName = input('Enter First Name: ')
                for n in self.firstName:
                    if not n.isalpha() and not n.isspace():             # Checks if the entry contains alphabets only
                        raise ValueError("First Name must contain Alphabets only.")
                break
            except ValueError as e:
                print(f'Error: {e}')

        while True:
            try:
                self.lastName = input('Enter Last Name: ')
                for n in self.lastName:
                    if not n.isalpha() and not n.isspace():             # Checks if the entry contains alphabets only
                        raise ValueError("Last Name must contain Alphabets only.")
                break
            except ValueError as e:
                print(f'Error: {e}')

        while True:
            try:
                self.balance = int(input('Enter Starting Balance: PKR '))
                if self.balance < 0:
                    raise NegativeBalanceError                          # Raises error if the entry is negative
                break

            except ValueError:                                          # Raises error if the entry contains non-digits
                print("Error: Starting balance must contain Digits only.")
            except NegativeBalanceError as e:
                print(f'Error: {e}')

        with open('User'+str(self.userID)+'.pkl','wb') as userdata:
            pickle.dump(self,userdata)                                  # Stores the user object in memory


    def login(self):
        'Logs in as User'

        while True:
            UN = input("Enter Username (Or Enter 'X' to go back): ")
            if UN == 'X' or UN == 'x': return 0                         # An option to abort log in process
            P = input('Enter Password: ')

            if (UN == self.username) and (P == self.password):          # Checks if entered credentials are correct
                print('\nLogged in Successfully!')
                return 1
            else:
                print('Incorrect Username or Password!')


    def addBalance(self):
        'Adds balance to the account'
        while True:
            try:
                deposit = int(input('How much Additional Balance you want to Deposit into this Account?\nPKR '))
                if deposit <= 0:
                    raise NegativeBalanceError                          # Raises error if the entry is negative
                self.balance += deposit                                 # Increases account balance
                break

            except ValueError:                                          # Raises error if the entry contains non-digits
                print('Error: Invalid Input! Only Positive Whole Numbers are Valid')
            except NegativeBalanceError as e:
                print(f'Error: {e}')


    def showRentalHistory(self):
        'Displays the User rental history in a proper format'

        reservationFile = File('reservations')
        print('\nYour Past and Current Reservations:')
        reservationFile.display(2,'U'+str(self.userID))                 # Filters out data of a user and displays it


    def submitFeedback(self):
        'Takes feedback, regarding the application, from the User'

        self.feedback = input('\nSubmit your Feedback here:\n').strip()
        print('\nThanks for Providing Feedback!')
        with open('feedback.txt', 'a+') as feedbackFile:
            feedbackFile.write('- '+self.feedback+'\n')                 # Writes feedback to a text file
        
            
    def logout(self):
        'Logs out to Account Selection Menu'

        super().logout()
        os.remove('User'+str(self.userID)+'.pkl')

        with open('User'+str(self.userID)+'.pkl','wb') as userdata:
            pickle.dump(self,userdata)                                  # Refreshes user object data upon log out
        print('Thanks for Visiting. Have a Blessed Day!')


    def showDetails(self):
        'Displays User credentials in a proper format'

        print('\n-----------Your Credentials-----------')
        print(f'{'User ID':11}| U{self.userID}')
        print(f'{'Username':11}| {self.username}')
        print(f'{'First Name':11}| {self.firstName}')
        print(f'{'Last Name':11}| {self.lastName}')
        print(f'{'Balance':11}| PKR {self.balance}')
        print()

    
    def delete(self):
        'Cancels any active reservation and deletes the User account '

        if not self.currentRentID == None:                              # Checks if there is any active reservation
            with open('Rent'+str(self.currentRentID)+'.pkl','rb') as rentdata:
                reservation = pickle.load(rentdata)                     # Retrieves the active reservation 
            print('Active',end=' ')
            reservation.cancel()                                        # Cancels the reservation
        
        os.remove('User'+str(self.userID)+'.pkl')                       # Removes user object from memory
        del self                                                        # Deletes the user object
        print('Account Deleted')
