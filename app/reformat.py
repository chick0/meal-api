from re import compile

LINE_BREAK = "<br/>"
ALLERGY_TABLE = {
    1: "난류",
    2: "우유",
    3: "메밀",
    4: "땅콩",
    5: "대두",
    6: "밀",
    7: "고등어",
    8: "게",
    9: "새우",
    10: "돼지고기",
    11: "복숭아",
    12: "토마토",
    13: "아황산류",
    14: "호두",
    15: "닭고기",
    16: "쇠고기",
    17: "오징어",
    18: "조개류",
    19: "잣",
}


def reformat(json: list):
    new_json = []

    re = compile(r"([0-9]{1,}[.])")

    for item in json:
        menu_list = []
        for menu in item['DDISH_NM'].split(LINE_BREAK):
            search = re.search(menu)

            if search is None:
                allergy = []
                codes = []
            else:
                codes = "".join(re.findall(menu))
                menu = menu.replace(codes, "").replace("()", "")

                codes = [int(x) for x in codes.split(".") if len(x) != 0]

                allergy = []
                for code in codes:
                    # 알러지 식품명 표에서 가져오기
                    # 표에 등록된 식품이 아니라면 그냥 숫자 코드 등록하기
                    allergy.append(ALLERGY_TABLE.get(code, str(code)))

            menu_list.append({
                "name": menu.strip(),
                "allergy": allergy,
                "allergy_code": codes
            })

        new_json.append({
            "school": item['SCHUL_NM'],
            "code": [item['MMEAL_SC_CODE'], item['MMEAL_SC_NM']],

            "calorie": item['CAL_INFO'],
            "nutrient": item['NTR_INFO'].split(LINE_BREAK),
            "origin": item['ORPLC_INFO'].split(LINE_BREAK),

            "menu": menu_list
        })

    return new_json
