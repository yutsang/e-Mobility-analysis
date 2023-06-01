class ReportQuestion:
    def __init__(self,place,number,accident):
        self.place = place
        self.number = number
        self.accident = accident

    def is_accident(self):
        if self.accident == True:
            return True
        else: 
            return False
GetHappen = ReportQuestion("place",2,False)
print(GetHappen.is_accident())

        



