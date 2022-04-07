import json


class Review_crawling:
    id = None
    restaurant = None
    content = ""
    report = ""
    writer = ""
    writedttm = ""

    def __init__(self, content, writer, writedttm, restaurant):
        self.content = content
        self.writer = writer
        self.writedttm = writedttm
        self.restaurant = restaurant
        return
