from datetime import datetime
from datetime import timedelta


def get_day_name(code: int) -> str:
    # 요일 이름 불러오는 필터
    return {
        6: "일",  # 주말
        0: "월",
        1: "화",
        2: "수",
        3: "목",
        4: "금",
        5: "토",  # 주말
    }.get(code)


class Day:
    def __init__(self, dt: datetime):
        self.datetime = dt
        self.day_code = self.datetime.weekday()
        self.day_str = get_day_name(code=self.day_code)

    def get_weeks(self) -> dict:
        weeks = {}

        for code in [6, 0, 1, 2, 3, 4, 5]:
            d = self.day_code - code if self.day_code > code else code - self.day_code

            if self.day_code <= code:
                weeks[code] = self.datetime + timedelta(days=d)
            else:
                weeks[code] = self.datetime - timedelta(days=d)

        if self.day_code == 6:
            for c, d in weeks.items():
                weeks[c] = d + timedelta(days=7)

        weeks[6] = weeks[6] - timedelta(days=7)

        return weeks

    def get_center(self, length: int) -> list:
        if length / 2 == int(length / 2):
            raise Exception("I need an odd number!")

        center = int(length / 2)
        weeks = []

        for i in range(-center, center + 1, 1):
            weeks.append(Day(dt=self.datetime + timedelta(days=i)))

        return weeks

    @property
    def dd(self) -> str:
        return self.datetime.strftime("%d")

    @property
    def ymd(self) -> str:
        return self.datetime.strftime("%Y%m%d")

    def __repr__(self):
        return f"<Day dt={self.datetime.strftime('%Y-%m-%d')!r}, day_str={self.day_str!r}>"
