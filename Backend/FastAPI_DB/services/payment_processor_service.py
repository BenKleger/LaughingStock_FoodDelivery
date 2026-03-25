import re
# from Backend.FastAPI_DB.schemas import user as userClass
from Backend.FastAPI_DB.schemas.payment_processor import PaymentProcessor, PaymentProcessorCreate
from fastapi import HTTPException
from Backend.FastAPI_DB.repositories.order_repo import save_all, load_all
from Backend.FastAPI_DB.services.orders_service import change_order_status
from FastAPI_DB.services.orders_service import get_order_by_order_id

def process_payment(payload: PaymentProcessorCreate):
    """
    Parameters:
        payload (PaymentProcessorCreate): Object containing payment data
    
    Raises:
        HTTPException 400 with a list of specific error messages.

    Description:
        This function processes the payment by validating the payment method, 
        updating the order status, saves it, and raises an error if the 
        payment method is invalid.
    """
    valid = validatePaymentMethod(payload)
    if valid["valid"]: 
        chargePaymentMethod() #dummy method
        change_order_status(payload.order.order_id, "paid")
        return True
    else: raise HTTPException(status_code=400, detail=valid["errors"])

def validatePaymentMethod(payload: PaymentProcessorCreate):
    """
    Validates a given payment method.

    Parameters:
        payload (PaymentProcessorCreate): Object containing payment data

    Returns:
        valid (bool): True if valid
        errors (str[]): array of error messages

    Description:
        This function validates the given payment method using helper functions and stores
        any error messages returned by said functions. These messages are then returned
        along with the validity of the payment method.
    """
    errors = []
    valid = []
    if(payload.payment_method in ("CREDIT", "DEBIT")):
        valid = [checkPaymentNumber(payload.payment_number), luhnTest(payload.payment_number), 
                    checkPin(payload.payment_pin), checkName(payload.card_holder_name), 
                    checkPostal(payload.postal_code), checkAddress(payload.billing_address)]
    elif(payload.payment_method in ("APPLEPAY", "PAYPAL")):
        valid = [checkEmail(payload.email), checkPassword(payload.email_password)]
    else: 
        errors.append("INVALID PAYMENT METHOD!")

    if(payload.order.order_status != "being_created"):
        errors.append("ORDER CANNOT BE MODIFIED IN THIS STATE!")
    # add error messages (if any) to the errors array, if errors is not empty
    # return false and list of errors 
    for item in valid:
        if item: errors.append(item)
    if errors:
        # print(errors)
        return {"valid": False, "errors": errors}
    return {"valid": True}

def chargePaymentMethod():
    """
    Dummy method for charging a card. Unimplemented.
    """
    pass

def checkPaymentNumber(payment_number: str):
    """
    Basic check for a payment number.

    Parameters: 
        payment_number (str): the payment number.

    Returns:
        Nothing if valid, error message (str) if invalid.
    
    Description:
        Checks whether a payment number is of the correct length does not have
        non-digit characters.
    """
    if len(payment_number) != 16: return "CARD NUMBER LENGTH IS INCORRECT!"
    if not payment_number.isdigit(): return "CARD NUMBER IS NOT NUMERIC!"
    return None

def luhnTest(n):
    """
    Advanced check for a payment number.

    Parameters: 
        n (str): the payment number.

    Returns:
        Nothing if valid, error message (str) if invalid.
    
    Description:
        A basic, widely used algorithm used to validate identification numbers. Essentially
        checks for accidental errors when the user inputs it.
        Takes a number(string), takes the last digit (the check digit, CD) which was calculated
        from the rest of the number (payload, P). This function removes the CD and recalculates
        it from P and compares them. If the CDs match, then the number is valid.

    Credits:
        Courtesy of rosettacode.org
        https://rosettacode.org/wiki/Luhn_test_of_credit_card_numbers#Python
        
    """
    r = [int(ch) for ch in str(n)][::-1]
    valid = (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0
    if valid: return None
    else: return "INVALID CARD NUMBER! DID YOU MAKE A MISTAKE?"

def checkPin(pin: str):
    """
    Checks whether a pin (cvv) is valid.

    Parameters: 
        pin (str): the pin.

    Returns:
        Nothing if valid, error message (string) if invalid.
    
    Description:
        Takes the pin and checks that it's 3 characters long and does not have
        non-digit characters.
    """
    if (len(pin) == 3 and pin.isdigit()): return None
    else: return "INVALID PIN!"

def checkName(name: str):
    """
    Checks whether a name is valid.
    
    Parameters: 
        name (str): the cardholder name
    
    Returns: 
        Nothing if valid, error message (str) if invalid.
    
    Description:
        This function checks the name isn't empty.
    """
    name = name.strip()
    name = name.replace(" ", "")
    if (len(name) > 0) and (name.isalpha()): return None
    else: return "INVALID CARDHOLDER NAME!"

def checkPostal(postal: str):
    """
    Checks the postal code.
    
    Parameters: 
        postal (str): postal code
    
    Returns: 
        Nothing if valid, error message (str) if invalid.
    
    Description:
        This function checks that the postal code (format A1A 1A1) follows the correct format.
        
    Credits:
        Courtesy of GRS on StackOverflow
        https://stackoverflow.com/questions/29906947/canadian-postal-code-validation-python-regex/56592315#56592315
    """
    postal = postal.upper()
    if (len(re.findall(r'[A-Z]{1}[0-9]{1}[A-Z]{1}\s*[0-9]{1}[A-Z]{1}[0-9]{1}', postal)))==1: return None
    else: return "INVALID POSTAL CODE!"

def checkAddress(address: str):
    """
    Checks the address.
    
    Parameters: 
        address (str): address
    
    Returns: 
        Nothing if valid, error message (str) if invalid.
    
    Description:
        This function checks that the address is not extremely short, and has a number.
    """
    address = address.strip()
    if len(address) < 5:
        return "ADDRESS TOO SHORT!"
    if not any(c.isdigit() for c in address):
        return "MISSING HOUSE NUMBER!"     
    return None

def checkEmail(email: str):
    """
    Checks the email address.
    
    Parameters: 
        email (str): email address.
    
    Returns: 
        Nothing if valid, error message (str) if invalid.
    
    Description:
        Validates the email by checking that @ isnt the 1st chararacter and that . isnt 
        immediately after @ or the last character
    """
    if "@" in email and "." in email:
        atIdx = email.index("@")
        dotIdx = email.rindex(".")
        if (atIdx > 0 and dotIdx > atIdx + 1) and \
            (dotIdx < len(email) - 1): return None
        else:
            return "INVALID EMAIL FORMAT!"
    else:
        return "INVALID EMAIL DOMAIN!"
    
def checkPassword(password):
    """
    Checks the email password.
    
    Parameters: 
        password (str): email password.
    
    Returns: 
        Nothing if valid, error message (str) if invalid.
    
    Description:
        This function validates the pw by making sure it is not incredibly short.
    """
    if len(password) > 5: return None
    else: return "EMAIL PASSWORD TOO SHORT!"