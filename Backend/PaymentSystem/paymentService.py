from Backend.Order import order
from Backend.FastAPI_DB.schemas import user
from decimal import Decimal
class paymentService:
    """Use decimal instead of floats to ensure floating point errors dont happen"""
    commissionRate = Decimal("0.05")    

    """Setters & getters"""
    def setCommission(self, rate: str): self.commissionRate = Decimal(rate)
    def setTipType(self, type: str): self.tipType = type
    def setTipAmount(self, amount: str): self.tipAmount = Decimal(amount)
    def setDiscountType(self, type: str): self.discountType = type
    def setDiscountAmount(self,amount: str): self.discountAmount = Decimal(amount)

    def getCommission(self): return self.commissionRate
    def getTipType(self): return self.tipType
    def getTipAmount(self): return self.tipAmount
    def getDiscountType(self): return self.discountType
    def getDiscountAmount(self): return self.discountAmount

    def __init__(self, Order: order, User: user):
        self.orderID = Order.order_ID
        # self.address = User.userAddress
        self.paymentBase = Decimal(str(round(Order.get_total(), 2)))
        self.commission = self.calcCommission()
        self.taxRate = self.calcTaxRate()
        self.tipAmount = 0
        self.tipType = "FLAT"
        self.discountAmount = 0
        self.discountType = "FLAT"
    
    def calcTaxRate(self):
        """Calculates the tax rate based on province and returns it"""
        province = self.getProvince()
        GST = Decimal("0.05")
        PST: float
        match province:
            case "AB": PST = Decimal("0")
            case "BC": PST = Decimal("0.07")
            case "MB": PST = Decimal("0.07")
            case "SK": PST = Decimal("0.06")
            case "ON": PST = Decimal("0.08")
            case "QC": PST = Decimal("0.0975")
            case _: raise ValueError("Province is not supported!")
        return (GST + PST)

    def getProvince(self):
        """Returns the province the user resides in"""
        #TBD
        return "BC"

    def calcCommission(self):
        """Returns the commission taken by the app"""
        return self.commissionRate*self.paymentBase
    
    def calcDriverTip(self):
        """Calculates the driver's tip based on the type selected (flat number or
        percentage of subtotal)"""
        if(self.tipType == "FLAT"):
            return self.tipAmount
        elif(self.tipType == "RATE"):
            return self.paymentBase*self.tipAmount

    def calcDiscount(self):
        """Calculates the discount based on the type selected (flat number or
        percentage of subtotal)"""
        if(self.discountType == "FLAT"):
            return self.discountAmount
        elif(self.discountType == "RATE"):
            return self.paymentBase*self.discountAmount

    def calcTotal(self):
        """Calculates the total charge"""
        return self.paymentBase + (self.paymentBase*self.taxRate) + self.calcCommission() \
        + self.calcDriverTip() + self.calcDiscount()