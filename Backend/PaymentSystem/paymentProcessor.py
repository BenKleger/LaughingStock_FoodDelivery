import re
from Backend.FastAPI_DB.schemas import user
class paymentProcessor:
    # ADD SECURITY LATER
    # MAYBE COPY THE PW, EMAIL, AND ADDRESS CHECKERS FROM/TO USER
    userID = int
    def __init__(self, customer: user.User):
        self.userID = customer.id
        # self.userAddress = customer.userAddress
        self.paymentNumber = -1
        self.paymentPin = -1
        self.paymentMethod = "CREDIT"
        self.cardHolderName = "NAME"
        self.postalCode = "A1A 1A1"
        self.email = "TEST@test.com"
        self.emailPassword = -1


    def validatePaymentMethod(self):
        if(self.paymentMethod == "CREDIT" or self.paymentMethod == "DEBIT"):
            if not(len(self.paymentNumber) == 16): return False
            if not(self.paymentNumber.isdigit): return False
            if not(self.luhnTest(self.paymentNumber)): return False
            # instead of having 1 return, within function call that and get the return value
            # e.g. all valid, all functions return 1 
            # validity = self.checkpin(), at end check validity, if validity = 1 then pass
            # have the ifs in the func itself, 
            # or if and
            if not(self.checkPin(self.paymentPin)): return False
            if not(len(self.cardHolderName.strip()) > 0): return False
                #just verifies that holder name is not empty
            if not(self.checkPostal(self.postalCode)): return False
            if not(self.checkAddress(self.userAddress)): return False
        elif(self.paymentMethod == "APPLEPAY" or self.paymentMethod == "PAYPAL"):
            #just checks if email and password are valid
            if not(self.checkEmail(self.email)): return False
            if not(self.checkPassword(self.emailPassword)): return False
        else: return False 
        return True
    
    def luhnTest(self, n):
        """Courtesy of rosettacode.org
            https://rosettacode.org/wiki/Luhn_test_of_credit_card_numbers#Python
            A basic, widely used algorithm used to validate identification numbers. Essentially
            checks for accidental errors when the user inputs it.
            Takes a number(string), takes the last digit (the check digit, CD) which was calculated
            from the rest of the number (payload, P). This function removes the CD and recalculates
            it from P and compares them. If the CDs match, then the number is valid."""
        r = [int(ch) for ch in str(n)][::-1]
        return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0
    
    def checkPin(self, pin: str):
        """Takes the pin and checks that it's 3 characters long and are all numbers"""
        if (len(pin) == 3 and pin.isdigit): return True
        return False

    def checkPostal(postal: str):
        """Courtesy of GRS on StackOverflow
            https://stackoverflow.com/questions/29906947/canadian-postal-code-validation-python-regex/56592315#56592315
            Takes the postal code (format A1A 1A1) and checks that the format is followed."""
        postal = postal.upper()
        if (len(re.findall(r'[A-Z]{1}[0-9]{1}[A-Z]{1}\s*[0-9]{1}[A-Z]{1}[0-9]{1}', postal)))==1: return True
        else: return False

    def checkAddress(self, address: str):
        """Takes the address and checks that its not extremely short, and has a number."""
        address = address.strip()
        if len(address) < 5:
            return False
        if not any(c.isdigit() for c in address):
            return False        
        return True

    def checkEmail(self, email: str):
        """Takes a string, checks that @ isnt the 1st chararacter and that . isnt 
             immediately after @ or the last character"""
        if "@" in email and "." in email:
            atIdx = email.index("@")
            dotIdx = email.rindex(".")
            if (atIdx > 0 and dotIdx > atIdx + 1) and \
                (dotIdx < len(email) - 1): return True
            else:
                return False
        else:
            return False
        
    def checkPassword(self, password):
        """Only checks that the pw is not incredibly short"""
        return len(password) > 5

    def processPayment(self):
        """TBD"""
        pass