class Disk:
    def __init__(self) -> None:
        self.name = None
        self.rating = None
        self.interface = None
        self.capacity = None
        self.capacityTb = None
        self.capacityRaw = None
        self.rpm = None
        self.size = None
        self.rspeed = None
        self.wspeed = None
        self.price = None
        self.url = None

    def isValid(self):
        return None not in [self.capacity, self.name, self.price]
