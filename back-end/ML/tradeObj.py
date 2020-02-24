class trade:
    def __init__(self, previousNotional, currentNotional, previousQuantity, currentQuantity):
        self.previousNotional = previousNotional
        self.currentNotional = currentNotional
        self.previousQuantity = previousQuantity
        self.currentQuantity = currentQuantity
    def getPreviousNotional(self):
        return self.previousNotional
    def getCurrentNotional(self):
        return self.currentNotional
    def getPreviousQuantity(self):
        return self.previousQuantity
    def getCurrentQuantity(self):
        return self.currentQuantity
    def setBothValues(self, notional, quantity):
        self.currentNotional = notional
        self.currentQuantity = quantity
