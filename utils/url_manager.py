class url_manager:
    def __init__(
        self,
        type: str,
        auth_key: str = None,
        pIndex: int = 1,
        pSize: int = 100,
        additions: list = None,
    ):
        option_list: list = [f"pIndex={pIndex}", f"pSize={pSize}"]
        option: str = "&".join(option_list)

        try:
            addition_str = "&" + "&".join(additions)
        except TypeError:
            addition_str = ""

        self.url = (
            f"https://open.neis.go.kr/hub/{type}?Type=json&{option}"
            + ("" if auth_key is None else auth_key)
            + f"{addition_str}"
        )

    def get_url(self):
        return self.url
