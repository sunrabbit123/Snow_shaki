import random


class Strings:
    # region bot information
    activity_list = [
        "'샤키야 도움말' 이라고 해보지 않으련?",
        "샤키가 구르기 ",
    ]
    bot_prefix = [
        "샤키야",
        "참수진",
        "수진아",
        "Shaki",
        "shaki",
        "사카린",
        "샤캬",
        "스노우스키",
        "샤키",
        "수진",
        ".",
        "ㅅ",
    ]
    # endregion
    # region bot const
    number_emoji = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    number_emoji_dict = {
        "1️⃣": 0,
        "2️⃣": 1,
        "3️⃣": 2,
        "4️⃣": 3,
        "5️⃣": 4,
        "6️⃣": 5,
        "7️⃣": 6,
        "8️⃣": 7,
        "9️⃣": 8,
        "🔟": 9,
    }
    meal_dict = {"조식": 0, "중식": 1, "석식": 2}
    school_type: dict = {
        "초등학교": "elsTimetable",
        "중학교": "misTimetable",
        "고등학교": "hisTimetable",
        "특수학교": "spsTimetable",
    }
    # endregion

    # region command list
    command_prefixes = {
        # region basic command
        "help": ["도움말", "명령어", "help", "?", "도와줘"],
        "choice": ["골라", "뽑아", "chose"],
        "구글검색": ["구글검색", "사진검색", "사진가져와", "사진"],
        "사전검색": ["사전검색", "지식검색", "네이버검색", "사전"],
        "굴러": [
            "구르기",
            "앞구르기",
            "뒷구르기",
            "데굴데굴",
            "굴러",
            "뒹굴뒹굴",
            "rnffj",
            "eprnfmfm",
            "Rhkd",
        ],
        "링크": ["url", "Url", "URL", "링크", "주소", "초대"],
        "emoji": ["emoji", "이모지", "임티", "이모티콘", "표정"],
        "clean_messages": ["지워", "치워", "삭제", "없애", "delete", "클린", "clean"],
        # endregion
        # region custom command
        "배워": ["배워", "익혀", "study"],
        "잊어": ["잊어", "forget"],
        # endregion
        # region school command
        "급식": ["급식", "밥", "배고파", "조식", "아침", "중식", "점심", "석식", "저녁", "저녘", "ㅂ"],
        "regist": ["학교등록", "등록", "학교검색"],
        "시간표": ["시간표", "스케쥴", "스케줄"]
        # endregion
    }

    # region command type
    # custom command
    custom = ["배워", "잊어"]

    # School Command
    school = ["시간표", "급식", "regist"]
    # endregion

    # region none prefix
    commands = {"help": ["샤키명령어", "샤키도움말"]}
    meal = ["급식", "밥", "배고파", "조식", "아침", "중식", "점심", "석식", "저녁", "저녘"]
    # endregion

    # region datetime
    week = ["월", "화", "수", "목", "금", "토", "일"]
    dateCentury = ["하룻", "이튿", "사흗", "나흗", "닷샛", "엿샛", "이렛", "여드렛", "아흐렛"]
    dateCenturyAbbr = [
        "하루",  # 0
        "이틀",  # 1
        "사흘",  # 2
        "나흘",  # 3
        "닷새",  # 4
        "엿새",  # 5
        "이레",  # 6
        "여드레",  # 7
        "아흐레",  # 8
    ]
    dateExp = {
        "그끄저께": -3,
        "그끄제": -3,
        "그저께": -2,
        "그제": -2,
        "어제": -1,
        "오늘": 0,
        "내일": 1,
        "모레": 2,
        "글피": 3,
        "그글피": 4,
    }
    dateYearExp = ["재재작년", "재작년", "작년", "올해", "내년", "후년", "내후년", "후후년"]
    # endregion

    # region const message

    emoji = [
        "야발",
        "어쩌라고요,,,,",
        "☆*:.｡. o(≧▽≦)o .｡.:*☆",
        "༼ ༎ຶ ෴ ༎ຶ༽",
        "༼; ́༎ຶ ۝༎ຶ`༽",
        "༼; ́༎ຶ + ༎ຶ༽]",
        "(╬ ಠ 益ಠ)",
        "ಥಒ್ಲಥ",
        "ꂧ᷆◞८̯◟ꂧ᷆",
        "૮(ꂧꁞꂧ)ა",
        "(๑≖ิټ≖ิ)",
        "(´⊙ω⊙`)",
        "( ́◞ิ౪◟ิ‵)",
        "ᓀ( ́◒`๑)",
        "(ง ̇∇ ̇)ว(ว ̇∇ ̇)ง",
        "(╯°□°）╯︵ ┻━┻",
        "༼ つ ◕_◕ ༽つ",
        "¯\_(ツ)_/¯",
        "(´▽`ʃ♡ƪ)",
    ]

    roll = random.choice(["데구르르 꽝", "꽝 데구르르", "데구르르 뎅강", "ㄷㄱㄹㄹ ㄷㄱ", "야랄,,, 너나 구르세요"])
    # endregion


class CommandType:
    배워 = "custom"
    잊어 = "custom"

    시간표 = "school"
    급식 = "school"
    regist = "school"

    help = "basic"
    choice = "basic"
    구글검색 = "basic"
    사전검색 = "basic"
    굴러 = "basic"
    링크 = "basic"
    emoji = "basic"
    clean_message = "basic"
