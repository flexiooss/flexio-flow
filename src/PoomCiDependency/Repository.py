class Repository:
    id: str
    name: str
    checkoutSpec: str

    def __init__(self, id: str, name: str, checkoutSpec: str):
        self.id = id
        self.name = name
        self.checkoutSpec = checkoutSpec
