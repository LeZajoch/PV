class Bottle:
    def __init__(self, max_capacity, current_capacity):
        self.max_capacity = max_capacity
        self.max_capacity_milliliters = self.max_capacity * 1000
        self.current_capacity = current_capacity
        self.current_capacity_milliliters = self.current_capacity * 1000
        self.cap = False

    @property
    def get_capacity_liters(self):
        return str(self.current_capacity)+ "l"

    def fill_liters(self, content):
        if not self.cap:
            if self.current_capacity + content > self.max_capacity:
                print("Maximum capacity reached cannot add more")
            self.current_capacity += content
            self.current_capacity_milliliters = self.current_capacity * 1000
            print(self.current_capacity)
        else:
            print("cannot fill bottle because lid is closed")

    def empty(self):
        if not self.cap:
            self.current_capacity = 0
            self.current_capacity_milliliters = 0
        else:
            print("cannot empty bottle because lid is closed")

    def get_capacity_milliliters(self):
        print(str(self.current_capacity_milliliters) + "ml")

    def fill_milliliters(self, content):
        if not self.cap:
            if self.current_capacity_milliliters + content > self.max_capacity_milliliters:
                print("Maximum capacity reached cannot add more")
            self.current_capacity_milliliters += content
            self.current_capacity = self.current_capacity_milliliters / 1000
            print(self.current_capacity_milliliters)
        else:
            print("cannot fill bottle because lid is closed")
    def close(self):
        self.cap = True

    def open(self):
        self.cap = False





Bottle_1 = Bottle(max_capacity=100, current_capacity=0)
Bottle_1.open()
Bottle_1.fill_liters(10)
Bottle_1.get_capacity_liters
Bottle_1.fill_milliliters(5000)
Bottle_1.get_capacity_milliliters()
Bottle_1.close()