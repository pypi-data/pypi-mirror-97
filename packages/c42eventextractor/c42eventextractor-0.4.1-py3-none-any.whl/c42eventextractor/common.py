from datetime import datetime


def convert_datetime_to_timestamp(date):
    return (date - datetime.utcfromtimestamp(0)).total_seconds()


class IncompatibleFilterError(ValueError):
    pass
