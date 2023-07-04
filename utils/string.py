import re


class StringManger:
    @staticmethod
    def br_to_new_line(string: str) -> str:
        return string.replace("<br/>", "\n") + "\n"

    @staticmethod
    def filter_with_unused_data(string: str) -> str:
        round1 = re.sub(
                pattern=r"\((\d\.?)+\)", repl="", string=string
            )
        return re.sub(
            pattern=r"[^가-힣0-9|<br/>|\&|()]", repl="", string=round1
        )

    @staticmethod
    def get_grade(string: str) -> str:
        grade = re.search(pattern="\d+학년", string=string).group()
        return re.sub(pattern="[^0-9]", repl="", string=grade).split()[0]

    @staticmethod
    def get_class(string: str) -> str:
        clazz = re.search(pattern="\d반", string=string).group()
        return re.sub(pattern="[^0-9]", repl="", string=clazz)
