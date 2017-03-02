import json
from datetime import datetime

from pins.models import Board
from pins.models import Pin
from pins.models import User


def run():
    with open('seed_data/pins_formatted.json') as data_file:
        # Note: Exception raised when treating data file from Pinterest google drive
        # as json because it is not json, it's a list of objects. It was changed
        # to an object instead of a list in order to treat it as json.
        pin_json_data = json.load(data_file)
        count = 0
        for item in pin_json_data.values():
            count += 1
            print count
            # User
            full_name = item["pinner"]["full_name"]
            pin_user_id = item["pinner"]["id"]
            img_url = item["pinner"]["image_small_url"]
            username = item["pinner"]["username"]

            try:
                pinner, created = User.objects.get_or_create(
                    full_name=full_name,
                    pin_user_id=pin_user_id,
                    img_url=img_url,
                    username=username
                    )
            except Exception as inst:
                print type(inst), inst

            print "Pinner created:"
            print pinner, created

            # Board
            owner_id = item["board"]["owner"]["id"]
            url = item["board"]["url"]
            name = item["board"]["name"]
            try:
                board, created = Board.objects.get_or_create(
                    owner_id=owner_id,
                    url=url,
                    name=name
                    )
            except Exception as inst:
                print type(inst), inst

            print "Board created:"
            print board, created

            # # Pin
            pin_board = board
            title = item["title"]

            # can be null
            buyable_product = item["buyable_product"]
            if buyable_product:
                buyable_product = bool(buyable_product)
            else:
                buyable_product = False

            description = item["description"]
            pin_id = item["id"]
            created_at = item["created_at"]

            # ex: "Fri, 15 Jan 2016 21:02:55 +0000"
            datetime_object = datetime.strptime(created_at, '%a, %d %b %Y %H:%M:%S +%f')

            img_url = item["images"]["236x"]["url"]
            img_height = item["images"]["236x"]["height"]

            like_count = item["like_count"]
            repin_count = item["repin_count"]
            try:
                pin, created = Pin.objects.get_or_create(
                    pinner=pinner,
                    title=title,
                    buyable_product=buyable_product,
                    description=description,
                    pinterest_id=pin_id,
                    created_at=datetime_object,
                    img_url=img_url,
                    img_height=img_height,
                    like_count=like_count,
                    repin_count=repin_count
                    )
                pin.boards.add(pin_board)
            except Exception as inst:
                print type(inst), inst
            print "Pin created:"
            print pin, created

            print "***" * 10
    print "DB seeded!"
