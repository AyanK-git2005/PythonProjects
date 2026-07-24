
from classExceptions import InsufficientBalanceError
from classReservation import Reservation
from classAdmin import AdministratorAccount
from classFile import File
from classUser import UserAccount
import pickle


reservationFile = File('reservations')
carFile = File('cars')

print('\n\nWelcome to the Best Car Rental System!')

while True:
    print('\n--------Account Selection Menu--------')
    print('Select an Option:')
    print('\n1. Login as Administrator')
    print('2. Login as User')
    print('3. Create a New User Account')
    print('4. Exit the Application')

    choice1 = input('\nYour Choice: ')

    while True:

        if choice1 == '4':
            print('\nProgram Ended!\n')
            quit()                                                              # Terminates the program

        elif choice1 == '1':
            admin = AdministratorAccount()                                      # Instantiates an AdminitratorAccount object
            privilege = admin.login()                                           # Logs in and returns the privilege
            if privilege == 'Back': break

            while True:
                print('\n-------Administrator Dashboard-------')
                print('Select an Option:')
                print('\n1. Show Available Cars')
                print('2. Show Active Reservations')
                print('3. Add Car(s)')
                print('4. Remove Car')
                print('5. Generate Customer Report')
                print('6. View User Feedback')
                print('7. Logout')

                choice2 = input('\nYour Choice: ')

                while True:
                    breakFlag = 1                                               # Sets breakFlag to 1
                    if choice2 == '7':
                        admin.logout()

                    elif choice2 == '1':
                        carFile.display()                                       # Displays available cars in a proper format

                    elif choice2 == '2':
                        reservationFile.display(1, 'Active')      # Displays reservation data of reserved cars

                    elif choice2 == '3':
                        admin.addCar()

                    elif choice2 == '4':
                        carFile.display()                                       # Displays available cars in a proper format
                        while True:
                            carID = input("\nEnter the ID of the Car to be Removed (Or Enter 'X' to go back): ")
                            msg = admin.removeCar(carID)                        # Removes a car and returns a message
                            if msg == 'Removed': break                          # Returns to the dashboard if car is removed

                    elif choice2 == '5':
                        reservationFile.display()                               # Displays the reservation data of all users

                    elif choice2 == '6':
                        admin.reviewFeedback()

                    else:
                        choice2 = input('Invalid Choice! Please Enter a Correct Choice: ')
                        breakFlag = 0                                           # Sets breakFlag to 0

                    if breakFlag: break                                         # Breaks the loop if breakFlag is 1
                if choice2 == '7': break                                        # Breaks the loop if choice was to log out

        elif choice1 == '2':
            while True:
                UID = input("\nEnter Your User ID (Or Enter 'X' to go back): ")
                if UID == 'X' or UID == 'x': break                              # An option to go back

                try:
                    if not UID[0] == 'U':
                        raise NameError                                         # Raises Error if entry is invalid
                    with open('User'+UID[1:]+'.pkl','rb') as userdata:
                        user=pickle.load(userdata)                              # Retrieves the user object from memory
                    break
                except:
                    print('User ID not found!')

            if UID == 'X' or UID == 'x': break                                  # An option to go back
            if not user.login(): break                                          # Breaks the loop if login was unsuccessful

            while True:
                print('\n---------User Dashboard---------')
                print('Select an Option:')
                print('\n1. Reserve a Car')
                print('2. View Current Reservation')
                print('3. Show Reservation History')
                print('4. Add Balance to the Account')
                print('5. View Account Credentials')
                print('6. Submit Feedback')
                print('7. Logout')
                print('8. Delete Account')

                choice3 = input('\nYour Choice: ')

                while True:
                    breakFlag = 1                                                # Sets breakFlag to 1
                    if choice3 == '7':
                        user.logout()

                    elif choice3 == '1' and user.currentRentID == None:         # Ensures that there is no active reservation
                        print('\nHere are the Available Cars:')
                        carFile.display()                                       # Displays available cars in a proper format
                        print()

                        while True:
                            CID = input("Enter the ID of the Car you want to Reserve (Or Enter 'X' to go back): ")
                            if CID == 'X' or CID == 'x': break                  # An option to go back

                            try:
                                if not CID[0] == 'C':
                                    raise NameError                             # Raises Error if entry is invalid
                                with open('Car'+CID[1:]+'.pkl','rb') as cardata:
                                    car = pickle.load(cardata)                  # Retrieves the car object from memory
                                break
                            except:
                                print('Car ID not found!')

                        if CID == 'X' or CID == 'x': break                      # An option to go back
                        print()

                        while True:
                            try:
                                days = int(input('For how many Days you want to Reserve this Car?\n'))
                                
                                if days <= 0:                                   # Checks if entry is positive
                                    raise ValueError
                                
                                if car.rate*days > user.balance:
                                    raise InsufficientBalanceError              # Raises error if balance is insufficient
                                
                                print('Reservation Successful!')
                                break

                            except ValueError:
                                print('Invalid Input! Only Positive Whole Numbers are Valid')
                            
                            except InsufficientBalanceError as e:
                                print('Error:',e)
                                print('\nYour Current Balance is: PKR '+str(user.balance))
                                print('Balance Required for this Reservation: PKR '+str(car.rate*days))
                                print('\nSelect an Option:')
                                print('1. Add More Balance to the Account and Reserve Again')
                                print('2. Reserve for a Shorter Period')
                                
                                choice4 = input('\nYour Choice: ')
                                
                                while True:
                                    if choice4 == '1':
                                        print()
                                        user.addBalance()
                                        break

                                    elif choice4 == '2':
                                        print()
                                        break

                                    else:
                                        choice4 = input('Invalid Choice! Please Enter a Correct Choice: ')
                            
                        reservation = Reservation(user,car,days)                # Instantiates a reservation class object  
                        user.currentRentID = reservation.rent_id                # Assigns a reservation ID to the user
                        reservation.show_info()                                 # Displays reservation information
                        print('Thanks for Reserving!')
                    
                    elif choice3 == '2' and not user.currentRentID == None:     # Checks if there is an active reservation
                        
                        with open('Rent'+str(user.currentRentID)+'.pkl','rb') as rentdata:
                            reservation = pickle.load(rentdata)                 # Retrieves reservation object from memory
                        reservation.show_info()                                 # Displays reservation information

                        print('Select an Option:')
                        print('1. Extend this Reservation')
                        print('2. Cancel this Reservation')
                        print('Or Enter Any Key to Go Back')

                        choice5 = input('\nYour Choice: ')

                        while True:
                            if choice5 == '1':
                                while True:
                                    try:
                                        days = int(input('By how many Days you want to Extend this Reservation?\n'))
                                        if days <= 0:                           # Checks if entry is positive
                                            raise ValueError
                                        
                                        if reservation.car.rate*days > user.balance:
                                            raise InsufficientBalanceError      # Raises error if balance is insufficient
                                        
                                        reservation.extend(days)                # Extends the reservation
                                        print('Reservation Extension Successful!')
                                        break

                                    except ValueError:
                                        print('Invalid Input! Only Positive Whole Numbers are Valid')
                                    
                                    except InsufficientBalanceError as e:
                                        print('Error:',e)
                                        print('\nYour Current Balance is: PKR '+str(user.balance))
                                        print('Balance Required for this Reservation Extension: PKR '+str(reservation.car.rate*days))
                                        print('\nSelect an Option:')
                                        print('1. Add More Balance to the Account and Extend Again')
                                        print('2. Extend this Reservation by a Shorter Period')
                                        
                                        choice6 = input('\nYour Choice: ')
                                        
                                        while True:
                                            if choice6 == '1':
                                                user.addBalance()
                                                break

                                            elif choice6 == '2': break
                                            else:
                                                choice6 = input('Invalid Choice! Please Enter a Correct Choice: ')

                                user.balance -= reservation.car.rate*days   # Deducts balance from the user's account
                                user.currentRentID = reservation.rent_id    # Assigns a reservation ID to the user
                                reservation.show_info()                     # Displays reservation information
                                print('Thanks for Extending the Reservation!')

                            elif choice5 == '2':
                                reservation.cancel()                        # Cancels any active reservation
                                user.currentRentID = None                   # Decouples any reservation ID from the user
                            break

                    elif choice3 == '1' and not user.currentRentID == None: # Checks if there is an active reservation
                        print('\nYou already have an Active Reservation. Kindly Select another Option.')
                    
                    elif choice3 == '2' and user.currentRentID == None:     # Checks if there is an active reservation
                        print('\nYou do not have an Active Reservation. Kindly Select another Option.')
                    
                    elif choice3 == '3':
                        user.showRentalHistory()                            # Displays user's rental history
                    
                    elif choice3 == '4':
                        print('\nYour Current Balance is: PKR',user.balance)
                        user.addBalance()
                        print('Now Your Balance is PKR',user.balance)

                    elif choice3 == '5':
                        user.showDetails()                                  # Displays user credentials

                    elif choice3 == '6':
                        user.submitFeedback()                               # Takes feedback from the user
                    
                    elif choice3 == '8':
                        choice8 = input("\nAre you sure you want to Delete this Account?(Enter 'Y' for 'Yes'): ")
                        if choice8 == 'Y' or choice8 == 'y':
                            user.delete()                                   # Deletes the account
                    
                    else:
                        choice3 = input('Invalid Choice! Please Enter a Correct Choice: ')
                        breakFlag = 0                                       # Sets breakFlag to 0

                    if breakFlag: break                                     # Breaks the loop if breakFlag is 1
                if choice3 == '7' or choice3 == '8': break                  # Breaks loop if account deleted or logged out

        elif choice1 == '3':
            print('\nAre you sure that you dont already have an Existing Account?')
            choice7 = input("Do you really want to make a New one?(Enter 'Y' for 'Yes'): ")
            
            if choice7 == 'Y' or choice7 == 'y':
                user = UserAccount()                                        # Instantiates a user class object
                print('\nAccount Created Successfully!')
                print(f'Your User ID is: U{user.userID}')
        break
            