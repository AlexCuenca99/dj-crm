import os
from datetime import datetime
import logging


def set_age(birth):
    current_date = datetime.now()
    birth = datetime.strptime(str(birth), "%Y-%m-%d")

    age = current_date.year - birth.year

    # Verify if not have yet completed years
    if current_date.month < birth.month or (
        current_date.month == birth.month and current_date.day < birth.day
    ):
        age -= 1

    return age


def photo_file_name(instance, filename):
    extension = filename.split(".")[-1]
    filename = "photo_{}.{}".format(instance.id, extension)
    return os.path.join("accounts/images/photos/", filename)
