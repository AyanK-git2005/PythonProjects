
class NegativeBalanceError(Exception):
    'Exception class for Negative Balance Entry'
    def __init__(self):
        super().__init__('Negative Amount is not Valid!')


class InsufficientBalanceError(Exception):
    'Exception Class for Insufficient Balance for a Transaction'
    def __init__(self):
        super().__init__('Insufficient Balance for this Reservation!')
