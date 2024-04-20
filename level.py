import datetime
import itertools
from enum import StrEnum, auto
from typing import Optional, Any
from datetime import timedelta


def game_version(version: int):
    match version:
        case 1:
            return "1.0"
        case 2:
            return "1.1"
        case 3:
            return "1.2"
        case 4:
            return "1.3"
        case 5:
            return "1.4"
        case 6:
            return "1.5"
        case 7:
            return "1.6"
        case 10:
            return "1.7"
        case v:
            return str(v / 10)


def game_version_reverse(version: str):
    match version:
        case "1.0":
            return 1
        case "1.1":
            return 2
        case "1.2":
            return 3
        case "1.3":
            return 4
        case "1.4":
            return 5
        case "1.5":
            return 6
        case "1.6":
            return 7
        case "1.7":
            return 10
        case v:
            return int(float(v) * 10)


class DifficultyDenominator(StrEnum):
    NA = auto()
    assigned = auto()

    @classmethod
    def parse(cls, data: int):
        match data:
            case 10:
                return cls.assigned
            case _:
                return cls.NA

    @staticmethod
    def parse_revert(data):
        match data:
            case DifficultyDenominator.NA:
                return 0
            case DifficultyDenominator.assigned:
                return 10


class DifficultyNumerator(StrEnum):
    unrated = auto()
    easy = auto()
    normal = auto()
    hard = auto()
    harder = auto()
    insane = auto()

    @classmethod
    def parse(cls, data: int):
        match data:
            case 10:
                return cls.easy
            case 20:
                return cls.normal
            case 30:
                return cls.hard
            case 40:
                return cls.harder
            case 50:
                return cls.insane
            case _:
                return cls.unrated

    @staticmethod
    def parse_revert(data):
        match data:
            case DifficultyNumerator.unrated:
                return 0
            case DifficultyNumerator.easy:
                return 10
            case DifficultyNumerator.normal:
                return 20
            case DifficultyNumerator.hard:
                return 30
            case DifficultyNumerator.harder:
                return 40
            case DifficultyNumerator.insane:
                return 50


class Length(StrEnum):
    tiny = auto()
    short = auto()
    medium = auto()
    long = auto()
    XL = auto()

    @classmethod
    def parse(cls, data: int):
        match data:
            case 1:
                return cls.short
            case 2:
                return cls.medium
            case 3:
                return cls.long
            case 4:
                return cls.XL
            case _:
                return cls.tiny

    @staticmethod
    def parse_revert(data):
        match data:
            case Length.tiny:
                return 0
            case Length.short:
                return 1
            case Length.medium:
                return 2
            case Length.long:
                return 3
            case Length.XL:
                return 4


class DemonDifficulty(StrEnum):
    easy = auto()
    medium = auto()
    hard = auto()
    insane = auto()
    extreme = auto()

    @classmethod
    def parse(cls, data: int):
        match data:
            case 3:
                return cls.easy
            case 4:
                return cls.medium
            case 5:
                return cls.insane
            case 6:
                return cls.extreme
            case _:
                return cls.hard

    @staticmethod
    def parse_revert(data):
        match data:
            case DemonDifficulty.hard:
                return 0
            case DemonDifficulty.easy:
                return 3
            case DemonDifficulty.medium:
                return 4
            case DemonDifficulty.insane:
                return 5
            case DemonDifficulty.extreme:
                return 6


class Level:
    levelID: int
    levelName: str
    description: str
    levelString: str  # Unzip????
    version: int
    playerID: int  # TODO change to User
    difficultyDenominator: DifficultyDenominator
    difficultyNumerator: DifficultyNumerator
    downloads: int
    setCompletes: int
    officialSong: Optional[int]
    gameVersion: str
    likes: int
    length: Length
    demon: bool
    stars: int
    featureScore: Optional[int]
    difficultyAuto: bool
    recordString: str  # unused
    password: Optional[str]  # XOR
    uploadDate: str
    updateDate: str
    copiedID: Optional[int]
    twoPlayer: bool
    customSongID: Optional[int]
    extraString: str  # unknown
    coins: int
    verifiedCoins: bool
    starsRequested: int
    lowDetailMode: bool
    dailyNumber: Optional[int]
    epic: int
    demonDifficulty: Optional[DemonDifficulty]
    isGauntlet: bool
    objects: int
    editorTime: timedelta  # in seconds
    editorTimeCopies: timedelta  # in seconds
    settingsString: str  # unused

    data: dict[int, str]

    def __init__(self, data: dict[int, Any]):
        self.levelID = int(data.get(1))
        self.levelName = data.get(2, "Unknown")
        self.description = data.get(3, "Unknown")
        self.levelString = data.get(4, "Unknown")
        self.version = int(data.get(5))
        self.playerID = int(data.get(6))
        self.difficultyDenominator = DifficultyDenominator.parse(int(data.get(8)))
        self.difficultyNumerator = DifficultyNumerator.parse(int(data.get(9)))
        self.downloads = int(data.get(10))
        self.setCompletes = int(data.get(11, 0))
        self.officialSong = int(data.get(12, 0)) or None
        self.gameVersion = game_version(int(data.get(13)))
        self.likes = int(data.get(14)) or -int(data.get(16, 0))
        self.length = Length.parse(int(data.get(15)))
        self.demon = bool(int(data.get(17)))
        self.stars = int(data.get(18))
        self.featureScore = int(data.get(19)) or None
        self.difficultyAuto = bool(int(data.get(25)))
        self.recordString = data.get(26)
        self.password = passw if (passw := data.get(27)) != "0" else None
        self.uploadDate = data.get(28)  # TODO change to dt?
        self.updateDate = data.get(29)  # TODO change to dt?
        self.copiedID = int(data.get(30, 0)) or None
        self.twoPlayer = bool(int(data.get(31)))
        self.customSongID = int(data.get(35, 0)) or None
        self.extraString = data.get(36)
        self.coins = int(data.get(37))
        self.verifiedCoins = bool(int(data.get(38)))
        self.starsRequested = int(data.get(39))
        self.lowDetailMode = bool(int(data.get(40)))
        self.dailyNumber = int(data.get(41, 0)) or None
        self.epic = int(data.get(42, 0))
        self.demonDifficulty = DemonDifficulty.parse(int(data.get(43))) if self.demon else None
        self.isGauntlet = bool(int(data.get(44, 0)))
        self.objects = int(data.get(45, 0))
        self.editorTime = datetime.timedelta(seconds=int(data.get(46, 0)))
        self.editorTimeCopies = datetime.timedelta(seconds=int(data.get(47, 0)))
        self.settingsString = data.get(48)
        self.data = data

    def to_json(self):
        return {
            "levelID": self.levelID,
            "levelName": self.levelName,
            "description": self.description,
            "levelString": self.levelString,
            "version": self.version,
            "playerID": self.playerID,
            "difficultyDenominator": DifficultyDenominator.parse_revert(self.difficultyDenominator),
            "difficultyNumerator": DifficultyNumerator.parse_revert(self.difficultyNumerator),
            "downloads": self.downloads,
            "setCompletes": self.setCompletes,
            "officialSong": self.officialSong,
            "gameVersion": game_version_reverse(self.gameVersion),
            "likes": self.likes,
            "length": Length.parse_revert(self.length),
            "demon": self.demon,
            "stars": self.stars,
            "featureScore": self.featureScore,
            "difficultyAuto": self.difficultyAuto,
            "recordString": self.recordString,
            "password": self.password,
            "uploadDate": self.uploadDate,
            "updateDate": self.updateDate,
            "copiedID": self.copiedID,
            "twoPlayer": self.twoPlayer,
            "customSongID": self.customSongID,
            "extraString": self.extraString,
            "coins": self.coins,
            "verifiedCoins": self.verifiedCoins,
            "starsRequested": self.starsRequested,
            "lowDetailMode": self.lowDetailMode,
            "dailyNumber": self.dailyNumber,
            "epic": self.epic,
            "demonDifficulty": DemonDifficulty.parse_revert(self.demonDifficulty) if self.demonDifficulty is not None else None,
            "isGauntlet": self.isGauntlet,
            "objects": self.objects,
            "editorTime": int(self.editorTime.total_seconds()),
            "editorTimeCopies": int(self.editorTimeCopies.total_seconds()),
            "settingsString": self.settingsString
        }

    @classmethod
    def from_json(cls, data: dict[str, Any]):
        self = cls.__new__(cls)

        self.levelID = data.get("levelID")
        self.levelName = data.get("levelName")
        self.description = data.get("description")
        self.levelString = data.get("levelString")
        self.version = data.get("version")
        self.playerID = data.get("playerID")
        self.difficultyDenominator = DifficultyDenominator.parse(data.get("difficultyDenominator"))
        self.difficultyNumerator = DifficultyNumerator.parse(data.get("difficultyNumerator"))
        self.downloads = data.get("downloads")
        self.setCompletes = data.get("setCompletes")
        self.officialSong = data.get("officialSong")
        self.gameVersion = game_version(data.get("gameVersion"))
        self.likes = data.get("likes")
        self.length = Length.parse(data.get("length"))
        self.demon = data.get("demon")
        self.stars = data.get("stars")
        self.featureScore = data.get("featureScore")
        self.difficultyAuto = data.get("difficultyAuto")
        self.recordString = data.get("recordString")
        self.password = data.get("password")
        self.uploadDate = data.get("uploadDate")
        self.updateDate = data.get("updateDate")
        self.copiedID = data.get("copiedID")
        self.twoPlayer = data.get("twoPlayer")
        self.customSongID = data.get("customSongID")
        self.extraString = data.get("extraString")
        self.coins = data.get("coins")
        self.verifiedCoins = data.get("verifiedCoins")
        self.starsRequested = data.get("starsRequested")
        self.lowDetailMode = data.get("lowDetailMode")
        self.dailyNumber = data.get("dailyNumber")
        self.epic = data.get("epic")
        self.demonDifficulty = DemonDifficulty.parse(data.get("demonDifficulty")) if self.demon else None
        self.isGauntlet = data.get("isGauntlet")
        self.objects = data.get("objects")
        self.editorTime = datetime.timedelta(seconds=data.get("editorTime"))
        self.editorTimeCopies = datetime.timedelta(seconds=data.get("editorTimeCopies"))
        self.settingsString = data.get("settingsString")
        self.data = data

        return self

    @classmethod
    def from_string(cls, string: str):
        data = sorted(itertools.batched(string.split(":"), n=2), key=lambda x: int(x[0]))
        dict_data = {int(x[0]): x[1] for x in data}

        obj = cls.__new__(cls)
        obj.__init__(dict_data)

        return obj
