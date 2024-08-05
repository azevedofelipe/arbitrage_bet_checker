import pytest
import sys
import os
from datetime import date,timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from utils import format_date,list_all_days

@pytest.mark.parametrize("input_date,expected", [
    ('2024-07-30 00:00:00+00', '30/07 12 AM'),
    ('2024-07-30 12:00:00+00', '30/07 12 PM'),
    ('2024-07-30 15:30:00+00', '30/07 03 PM'),
    ('2024-07-30 23:59:59+00', '30/07 11 PM'),
])
def test_format_date(input_date, expected):
    assert format_date(input_date) == expected


@pytest.mark.parametrize("start_date, end_date, expected", [
    (date(2024,8,4),date(2024,8,5),{'2024-08-04':'2024-08-05','2024-08-05': '2024-08-06'}),
    (date(2024,8,4),date(2024,8,7),{'2024-08-04':'2024-08-05','2024-08-05':'2024-08-06','2024-08-06':'2024-08-07','2024-08-07':'2024-08-08'})
])
def test_list_dates(start_date,end_date,expected):
    assert list_all_days(start_date,end_date) == expected
