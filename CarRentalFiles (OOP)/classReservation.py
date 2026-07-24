
from datetime import datetime, timedelta
from MiscFunc import updateID
from classFile import File
import pickle
import os


reservationfile=File('reservations')
carfile=File('cars')


class Reservation:

    def __init__(self,user,car,days):
        """Takes a User Class Object, Car Class Object and number of
        days to instantiate a Reservation Class Object"""

        self.rent_id=updateID(2)                                    # Increments the reservation ID tally
        self.user=user
        self.car=car
        carfile.shortlist('C'+str(self.car.carID))                  # Removes the car from available cars list
        self.rent_period=days

        self.start_date=datetime.now()                              # Calculates reservation start date
        self.end_date=datetime.now()+timedelta(days=days)           # Calculates reservation end date
        self.rent_cost=self.car.rate*days                           # Calculates reservation cost
        self.user.balance-=self.rent_cost                           # Deducts balance from the user's account
        self.status='Active'                                        # Sets reservation status to Active
        self.log_data()                                             # Logs reservation data to memory


    def log_data(self):
        """Logs reservation data to its text file and stores the 
        reservation object as a file in secondary memory"""

        data= ['R'+str(self.rent_id),self.status,'U'+str(self.user.userID),
            self.user.username,'C'+str(self.car.carID),self.car.name,
            str(self.car.model),str(self.rent_period)+' Days',str(self.start_date.date()),
            str(self.end_date.date()),'PKR '+str(self.rent_cost)]   # Creates a list of reservation data points

        with open('Rent'+str(self.rent_id)+'.pkl','wb') as rentdata:
            pickle.dump(self,rentdata)                              # Stores reservation object in memory
        
        reservationfile.update(data)                                # Updates reservations list text file


    def log_cancellation(self):
        'Removes old reservation data from the list and replaces it with updated data'

        reservationfile.shortlist('R'+str(self.rent_id))            # Removes old reservation data from the list
        self.status='Cancelled'                                     # Sets reservation status to Cancelled

        old_data= ['R'+str(self.rent_id),self.status,'U'+str(self.user.userID),
                self.user.username,'C'+str(self.car.carID),self.car.name,
                str(self.car.model),str(self.rent_period)+' Days',str(self.start_date.date()),
                str(self.end_date.date()),'PKR '+str(self.rent_cost)]
        reservationfile.update(old_data)                            # Updates reservations list text file


    def extend(self,days):
        'Extends reservation period by the specified number of days'

        os.remove('Rent'+str(self.rent_id)+'.pkl')                  # Removes old reservation object from memory
        self.log_cancellation()
        self.rent_id=updateID(2)                                    # Increments the reservation ID tally
        
        self.rent_period+=days
        self.rent_cost+=self.car.rate*days                          # Calculates reservation extension cost
        self.end_date+=timedelta(days=days)                         # Calculates extended reservation end date

        self.status='Active'                                        # Sets reservation status to Active
        self.log_data()                                             # Logs reservation data to memory


    def cancel(self):
        'Cancels the reservation, and deletes it from memory'

        self.log_cancellation()
        data=['C'+str(self.car.carID),self.car.name,str(self.car.model),self.car.manufacturer,
              str(self.car.seats)+' Seats','PKR '+str(self.car.rate)]
        carfile.update(data)                                        # Updates cars list text file

        os.remove('Rent'+str(self.rent_id)+'.pkl')                  # Removes reservation object from memory
        del self                                                    # Deletes the reservation object
        print('Reservation Cancelled')


    def show_info(self):
        'Displays reservation data of a single reservation'

        print('\n------------Your Reservation Information-----------')
        print(f'{'Reservation ID':23}| R{self.rent_id}')
        print(f'{'Customer Name':23}| {self.user.firstName} {self.user.lastName}')
        print(f'{'Reserved Car ID':23}| C{self.car.carID}')
        print(f'{'Reserved Car Name':23}| {self.car.name}')
        print(f'{'Reserved Car Model':23}| {self.car.model}')
        print(f'{'Reservation Period':23}| {self.rent_period} Days')
        print(f'{'Reservation Start Date':23}| {self.start_date.date()}')
        print(f'{'Reservation End Date':23}| {self.end_date.date()}')
        print(f'{'Reservation Charges':23}| PKR {self.rent_cost}')
        print()
