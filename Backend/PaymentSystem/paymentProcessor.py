import re
from Backend.FastAPI_DB.schemas import user
class paymentProcessor:
    # ADD SECURITY LATER
    # MAYBE COPY THE PW, EMAIL, AND ADDRESS CHECKERS FROM/TO USER
    def __init__(self, customer: user.User, paymentMethod = "CREDIT", 
                 paymentNumber: str = "", paymentPin: str = "", cardHolderName = "", 
                 postalCode = "", email = "", emailPassword = ""):
        self.userID = customer.id
        # self.userAddress = customer.userAddress
        self.userAddress = "1234 TEST STREET"
        self.paymentNumber = paymentNumber
        self.paymentPin = paymentPin
        self.paymentMethod = paymentMethod
        self.cardHolderName = cardHolderName
        self.postalCode = postalCode
        self.email = email
        self.emailPassword = emailPassword

    def validatePaymentMethod(self):
        validity = []
        errors = []
        # functions return None if valid, error message if not
        if(self.paymentMethod in ("CREDIT", "DEBIT")):
            validity = [self.checkPaymentNumber(self.paymentNumber), self.luhnTest(self.paymentNumber), 
                        self.checkPin(self.paymentPin), self.checkName(self.cardHolderName), 
                        self.checkPostal(self.postalCode), self.checkAddress(self.userAddress)
                        ]
        elif(self.paymentMethod in ("APPLEPAY", "PAYPAL")):
            validity = [self.checkEmail(self.email), self.checkPassword(self.emailPassword)]
        else: return False
        # print out each error message. If there are none, return true
        for error in validity:
            if error: errors.append(error)
        if errors:
            for error in errors: print(error)
            return False
        return True
    
    def checkPaymentNumber(self, n: str):
        if len(n) != 16: return "CARD NUMBER LENGTH IS INCORRECT!"
        if not n.isdigit(): return "CARD NUMBER IS NOT NUMERIC!"
        return None

    def luhnTest(self, n):
        """Courtesy of rosettacode.org
            https://rosettacode.org/wiki/Luhn_test_of_credit_card_numbers#Python
            A basic, widely used algorithm used to validate identification numbers. Essentially
            checks for accidental errors when the user inputs it.
            Takes a number(string), takes the last digit (the check digit, CD) which was calculated
            from the rest of the number (payload, P). This function removes the CD and recalculates
            it from P and compares them. If the CDs match, then the number is valid."""
        r = [int(ch) for ch in str(n)][::-1]
        valid = (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0
        if valid: return None
        else: return "INVALID CARD NUMBER! DID YOU MAKE A MISTAKE?"
    
    def checkPin(self, pin: str):
        """Takes the pin and checks that it's 3 characters long and are all numbers"""
        if (len(pin) == 3 and pin.isdigit): return None
        else: return "INVALID PIN!"
    
    def checkName(self, name: str):
        if (len(self.cardHolderName.strip()) > 0): return None
        else: return "INVALID CARDHOLDER NAME!"

    def checkPostal(self, postal: str):
        """Courtesy of GRS on StackOverflow
            https://stackoverflow.com/questions/29906947/canadian-postal-code-validation-python-regex/56592315#56592315
            Takes the postal code (format A1A 1A1) and checks that the format is followed."""
        postal = postal.upper()
        if (len(re.findall(r'[A-Z]{1}[0-9]{1}[A-Z]{1}\s*[0-9]{1}[A-Z]{1}[0-9]{1}', postal)))==1: return None
        else: return "INVALID POSTAL CODE!"

    def checkAddress(self, address: str):
        """Takes the address and checks that its not extremely short, and has a number."""
        address = address.strip()
        if len(address) < 5:
            return "ADDRESS TOO SHORT!"
        if not any(c.isdigit() for c in address):
            return "MISSING HOUSE NUMBER!"     
        return None

    def checkEmail(self, email: str):
        """Takes a string, checks that @ isnt the 1st chararacter and that . isnt 
             immediately after @ or the last character"""
        if "@" in email and "." in email:
            atIdx = email.index("@")
            dotIdx = email.rindex(".")
            if (atIdx > 0 and dotIdx > atIdx + 1) and \
                (dotIdx < len(email) - 1): return None
            else:
                return "INVALID EMAIL FORMAT!"
        else:
            return "INVALID EMAIL DOMAIN!"
        
    def checkPassword(self, password):
        """Only checks that the pw is not incredibly short"""
        if len(password) > 5: return None
        else: return "EMAIL PASSWORD TOO SHORT!"


    def processPayment(self):
        """TBD"""
        pass