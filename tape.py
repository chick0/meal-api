from glob import glob
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED


def get_files() -> list:
    return [
        x for x in glob("./dist/**", recursive=True)
    ]


def tape():
    files = get_files()
    print("total files:", len(files))

    with ZipFile(
        file="dist.zip",
        mode="w",
        compression=ZIP_DEFLATED,
        compresslevel=9
    ) as zip:
        for file in files:
            print(" +", file), zip.write(file)


if __name__ == "__main__":
    tape()
