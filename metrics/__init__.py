import datetime
from metrics.build import BuildsCollector
from metrics.constants import Constants


def get_formatted_timestamp():
    """ Return iso time for UTC now """
    return f'{datetime.datetime.utcnow().isoformat()}Z'
