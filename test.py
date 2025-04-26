import dateutil.parser
from 

START_DATE = '10.08.2005'

DT = dateutil.parser.parse(START_DATE)

# (datetime.now() - datetime(2005, 8, 10, 3, 0)).total_seconds() / 60 / 60 / 24 / 365