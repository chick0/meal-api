from datetime import datetime
from datetime import timedelta


def get_weeks(day: datetime) -> dict:
    weeks = {}
    day_code = day.weekday()

    for code in [6, 0, 1, 2, 3, 4, 5]:
        d = day_code - code if day_code > code else code - day_code

        if day_code <= code:
            weeks[code] = day + timedelta(days=d)
        else:
            weeks[code] = day - timedelta(days=d)

    if day_code == 6:
        for c, d in weeks.items():
            weeks[c] = d + timedelta(days=7)

    weeks[6] = weeks[6] - timedelta(days=7)

    return weeks
