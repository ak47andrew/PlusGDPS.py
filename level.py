import datetime
from enum import StrEnum, auto
from typing import Optional, Any
from datetime import timedelta


def define_version(version: int):
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
            case 0:
                return cls.hard


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
        self.gameVersion = define_version(int(data.get(13)))
        self.likes = int(data.get(14)) or -int(data.get(16))
        self.length = Length.parse(int(data.get(15)))
        self.demon = bool(data.get(17))
        self.stars = int(data.get(18))
        self.featureScore = int(data.get(19)) or None
        self.difficultyAuto = bool(data.get(25))
        self.recordString = data.get(26)
        self.password = passw if (passw := str(data.get(27) ^ 26364)) != "0" else None
        self.uploadDate = data.get(28)  # TODO change to dt?
        self.updateDate = data.get(29)  # TODO change to dt?
        self.copiedID = int(data.get(30, 0)) or None
        self.twoPlayer = bool(data.get(31))
        self.customSongID = int(data.get(35, 0)) or None
        self.extraString = data.get(36)
        self.coins = int(data.get(37))
        self.verifiedCoins = bool(data.get(38))
        self.starsRequested = int(data.get(39))
        self.lowDetailMode = bool(data.get(40))
        self.dailyNumber = int(data.get(41, 0)) or None
        self.epic = int(data.get(42, 0))
        self.demonDifficulty = DemonDifficulty.parse(int(data.get(43))) if self.demon else None
        self.isGauntlet = bool(data.get(44))
        self.objects = int(data.get(45, 0))
        self.editorTime = datetime.timedelta(seconds=int(data.get(46, 0)))
        self.editorTimeCopies = datetime.timedelta(seconds=int(data.get(47, 0)))
        self.settingsString = data.get(48)
        self.data = data
