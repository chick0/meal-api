# -*- coding: utf-8 -*-
from sys import exit
from argparse import ArgumentParser
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini", encoding="utf-8")


if __name__ == "__main__":
    parser = ArgumentParser(description="설정 파일 수정/확인 유틸리티")
    parser.add_argument("-i", "--init",
                        help="설정 파일을 기본 값으로 초기화 합니다.",
                        action="store_const", const=True)
    parser.add_argument("-v", "--view", help="설정된 설정 파일을 확인 합니다.",
                        action="store_const", const=True)
    parser.add_argument("-e", "--edit", help="설정파일을 수정합니다",
                        action="store_const", const=True)

    args = parser.parse_args()
    if args.init:
        config = ConfigParser()
        config.add_section("app")
        config.set("app", "host", "http://localhost:1365")
        config.set("app", "port", "1365")
        config.add_section("redis")
        config.set("redis", "url", "redis://127.0.0.1:6379/0\n; use '#' to disable redis cache")
        config.add_section("api")
        config.set("api", "n", "#")

        config.write(open("config.ini", mode="w", encoding="utf-8"))
        print("설정 파일을 기본 값으로 초기화 했습니다.")
    if args.view:
        for sec in config.sections():
            print("[" + sec + "]")
            for k, v in config[sec].items():
                print("  "+k, v, sep=" = ")
    if args.edit:
        def fetch_int(prompt):
            try:
                return int(input(prompt))
            except ValueError:
                print("**숫자로 입력해주세요**")
                return fetch_int(prompt=prompt)

        print("수정할 섹션을 선택해주세요")
        print("\n".join([f" {x} : {i}" for x, i in enumerate(config.sections())]))
        try:
            section = config.sections()[fetch_int(prompt="섹션번호=")]
        except (IndexError, Exception):
            print("- 잘못된 섹션을 선택하셨습니다. 수정 취소됨.")
            exit(-1)

        print("선택된 섹션 : ", section)
        while True:
            print("수정할 옵션을 선택해주세요.")
            print("\n".join([f" {x} : {i}" for x, i in enumerate(config[section].keys())]))
            try:
                index = fetch_int(prompt="옵션번호=")
                print("현재 설정되어 있는 값 : ", config[section][list(config[section].keys())[index]])

                config[section][list(config[section].keys())[index]] = input("변경할 값=")
                config.write(open("config.ini", mode="w", encoding="utf-8"))
                print("- 설정파일을 수정했습니다.")
                exit(0)
            except (IndexError, Exception):
                print("- 잘못된 옵션을 선택하셨습니다.")


del exit, ArgumentParser, ConfigParser
