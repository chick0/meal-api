# -*- encoding: utf-8 -*-

# 원산지 검사 필터
def origin(info: str):
    if info.split(":")[-1].replace("국내산", "").find("산") == -1:
        return True
    else:
        return False


# 메뉴 파싱 필터
def parse_menu(menu: str):
    real_menu = ""

    for i in range(0, len(menu)):
        if menu[i] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
            real_menu += menu[i]

    return real_menu


# 알레르기 정보 표시 필터
def allergy(menu: str):
    allergy_str = ""
    allergy_code = ""
    allergy_json = {
        "1": "달걀",     "10": "돼지고기",
        "2": "복숭아",   "11": "우유",
        "3": "메밀",     "12": "토마토",
        "4": "아황산염", "13": "땅콩",
        "5": "대두",     "14": "호두",
        "6": "닭고기",   "15": "밀",
        "7": "고등어",   "16": "쇠고기",
        "8": "오징어",   "17": "게",
        "9": "새우",     "18": "조개"
    }

    for i in range(0, len(menu)):
        if menu[i] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
            allergy_code += menu[i]

    for code in allergy_code.split("."):
        if code in allergy_json.keys():
            allergy_str += f"{allergy_json[code]}, "

    if len(allergy_str) == 0:
        return ""

    return f"[{allergy_str[:-2]}]"
