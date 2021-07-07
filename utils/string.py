import re

class StringManger:
    @staticmethod
    def dots_to_new_line(string : str):
        return "\n".join(string.split("<br/>"))
    @staticmethod
    def filter_without_dot_and_korean(string : str):
        return re.sub(pattern="[^가-힣.]", repl="", string=string)