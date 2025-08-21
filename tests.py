from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


def main():
    print(get_file_content("calculator", "."))
    print(get_file_content("calculator", "pkg"))
    print(get_file_content("calculator", "/bin"))
    print(get_file_content("calculator", "../"))


if __name__ == "__main__":
    main()
