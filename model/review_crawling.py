import json


class Review_crawling:
    id = None
    restaurant = None
    content = ""
    report = ""
    writer = ""
    writedttm = ""

    def __init__(self, content, restaurant):
        self.content = content
        self.restaurant = restaurant
        return
