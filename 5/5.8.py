class Truck:
    def __init__(self, tank, consumption):
        self.tank = tank
        self.consumption = consumption

    def __set_fuel__(self,value):
        self.tank = value

    def __drive__(self,value):
        self.tank = value / self.consumption


truck_1 = Truck(tank = 30, consumption = 12.5)
truck_1.__set_fuel__(22.5)
truck_1.__drive__(20)
