class ReportQuestion:
    def __init__(self, place, CarNumber, accident):
        self.place = place
        self.CarNumber = CarNumber
        self.accident = accident

    def is_accident(self):
        if self.accident == True:
            return True
        else: 
            return False

    def traffic_jam_probability(self):
        if self.is_accident():
            accident_factor = 1.5
        else:
            accident_factor = 1.0

        # 假設車流量每增加 100 台車，塞車可能性增加 10%
        traffic_factor = 1 + (self.CarNumber / 1000) * 0.1

        probability = accident_factor * traffic_factor

        return probability

GetHappen = ReportQuestion("place", 10000, False)
print(GetHappen.is_accident())
print("塞車情況" +str( GetHappen.traffic_jam_probability()))
        



