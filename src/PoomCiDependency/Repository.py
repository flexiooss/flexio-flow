class Repository:
    id: str
    name: str
    checkout_spec: str

    def __init__(self, id: str, name: str, checkout_spec: str):
        self.id = id
        self.name = name
        self.checkout_spec = checkout_spec
