import requests
import json
import datetime
import math

params = (
    ('start_date', '2013-03-10T15:42:46+02:00'),
    ('end_date', '2013-03-12T15:42:46+02:00'),
)

response = requests.get('https://api.track.toggl.com/api/v8/time_entries', params=params, auth=('1971800d4d82861d8f2c1651fea4d212', 'api_token'))