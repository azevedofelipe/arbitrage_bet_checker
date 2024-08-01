import pytest
from utils import format_date

@pytest.mark.parametrize("input_date,expected", [
    ('2024-07-30 00:00:00+00', '30/07 12 AM'),
    ('2024-07-30 12:00:00+00', '30/07 12 PM'),
    ('2024-07-30 15:30:00+00', '30/07 03 PM'),
    ('2024-07-30 23:59:59+00', '30/07 11 PM'),
])
def test_format_date(input_date, expected):
    assert format_date(input_date) == expected
