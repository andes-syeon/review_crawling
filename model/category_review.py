import json


class Category_Review:
    category_id = None
    id = None
    restaurant_id = ""
    txt = ""

    def __init__(self, category_id, restaurant_id, txt, restaurant = None):
        self.txt = txt
        self.restaurant_id = restaurant_id
        self.category_id = category_id
        self.restaurant = restaurant
        return
