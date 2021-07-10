import re


class StringManger:
    @staticmethod
    def dots_to_new_line(string: str) -> str:
        return re.sub(pattern="[.]+", repl="\n", string=string)

    @staticmethod
    def filter_without_dot_and_korean(string: str) -> str:
        return re.sub(pattern="[^가-힣.]", repl="", string=string)

    @staticmethod
    def get_grade(string: str) -> str:
        grade = re.search(pattern="\d+학년", string=string).group()
        return re.sub(pattern="[^0-9]", repl="", string=grade).split()[0]

    @staticmethod
    def get_class(string: str) -> str:
        clazz = re.search(pattern="\d반", string=string).group()
        return re.sub(pattern="[^0-9]", repl="", string=clazz)
