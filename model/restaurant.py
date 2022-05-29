import json


class Restaurant:
    id = None
    original_name = ""
    name = ""
    address = ""
    local = ""
    operation = ""
    number = ""
    infodttm = ""
    star = 0.0

    def __init__(self):
        return

    def __init__(self, original_name,
                 name,
                 address,
                 local,
                 operation,
                 number,
                 infodttm,
                 star):
        self.original_name = original_name
        self.name = name
        self.address = address
        self.local = local
        self.operation = operation
        self.number = number
        self.infodttm = infodttm
        self.star = star
        return

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def to_parentheses(self):
        return (
            self.original_name, self.name, self.address, self.local, self.operation, self.number, self.infodttm,
            self.star)
