# This file will contain the enums of all jobs and class
from enum import IntEnum  # Importing enums
from ffxivcalc.Constants import LevelConstants, JobMod, StatInt


import math


class PlayerEnum(IntEnum):
    # Parent enum class for all other enums. Will have
    # the two functions.

    @classmethod
    def name_for_id(cls, id: int) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def id_for_name(cls, name: str) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1  # Evaluated as Unknown


class RoleEnum(PlayerEnum):
    # Enum for all roles
    Caster = 1
    Healer = 2
    Melee = 3
    Tank = 4
    PhysicalRanged = 5
    Pet = 6


class JobEnum(PlayerEnum):
    # Enum for all jobs

    # Caster
    BlackMage = 25
    Summoner = 27
    RedMage = 35

    # Healer
    WhiteMage = 24
    Astrologian = 33
    Sage = 40
    Scholar = 28

    # Melee
    Ninja = 30
    Samurai = 34
    Reaper = 39
    Monk = 20
    Dragoon = 22

    # Tank
    Gunbreaker = 37
    DarkKnight = 32
    Paladin = 19
    Warrior = 21

    # Physical ranged
    Machinist = 31
    Bard = 23
    Dancer = 38

    # Pet
    Pet = 0

    def JobStat(self):
        match self.value:
            case JobEnum.BlackMage:
                return MainStatEnum.INT
            case JobEnum.RedMage:
                return MainStatEnum.INT
            case JobEnum.Summoner:
                return MainStatEnum.INT
            case JobEnum.Scholar:
                return MainStatEnum.MND
            case JobEnum.WhiteMage:
                return MainStatEnum.MND
            case JobEnum.Astrologian:
                return MainStatEnum.MND
            case JobEnum.Sage:
                return MainStatEnum.MND
            case JobEnum.Monk:
                return MainStatEnum.STR
            case JobEnum.Ninja:
                return MainStatEnum.DEX
            case JobEnum.Dragoon:
                return MainStatEnum.STR
            case JobEnum.Samurai:
                return MainStatEnum.STR
            case JobEnum.Reaper:
                return MainStatEnum.STR
            case JobEnum.Machinist:
                return MainStatEnum.DEX
            case JobEnum.Bard:
                return MainStatEnum.DEX
            case JobEnum.Dancer:
                return MainStatEnum.DEX
            case JobEnum.DarkKnight:
                return MainStatEnum.STR
            case JobEnum.Gunbreaker:
                return MainStatEnum.STR
            case JobEnum.Warrior:
                return MainStatEnum.STR
            case JobEnum.Paladin:
                return MainStatEnum.STR
        return

    def RoleEnum(self):
        match self.value:
            case JobEnum.BlackMage:
                return RoleEnum.Caster
            case JobEnum.RedMage:
                return RoleEnum.Caster
            case JobEnum.Summoner:
                return RoleEnum.Caster
            case JobEnum.Scholar:
                return RoleEnum.Healer
            case JobEnum.WhiteMage:
                return RoleEnum.Healer
            case JobEnum.Astrologian:
                return RoleEnum.Healer
            case JobEnum.Sage:
                return RoleEnum.Healer
            case JobEnum.Monk:
                return RoleEnum.Melee
            case JobEnum.Ninja:
                return RoleEnum.Melee
            case JobEnum.Dragoon:
                return RoleEnum.Melee
            case JobEnum.Samurai:
                return RoleEnum.Melee
            case JobEnum.Reaper:
                return RoleEnum.Melee
            case JobEnum.Machinist:
                return RoleEnum.PhysicalRanged
            case JobEnum.Bard:
                return RoleEnum.PhysicalRanged
            case JobEnum.Dancer:
                return RoleEnum.PhysicalRanged
            case JobEnum.DarkKnight:
                return RoleEnum.Tank
            case JobEnum.Gunbreaker:
                return RoleEnum.Tank
            case JobEnum.Warrior:
                return RoleEnum.Tank
            case JobEnum.Paladin:
                return RoleEnum.Tank
            case JobEnum.Pet:
                return RoleEnum.Pet


class SpeedEnum(PlayerEnum):
    NA = 0
    SpS = 1
    SkS = 2

    @staticmethod
    def SpeedType(role):
        match role:
            case RoleEnum.Caster:
                return SpeedEnum.SpS
            case RoleEnum.Healer:
                return SpeedEnum.SpS
            case RoleEnum.Melee:
                return SpeedEnum.SkS
            case RoleEnum.Tank:
                return SpeedEnum.SkS
            case RoleEnum.PhysicalRanged:
                return SpeedEnum.SkS

        return SpeedEnum.NA


class DamageEnum(PlayerEnum):
    DirectDamage = 0
    MagicDoT = 1
    PhysicalDoT = 2
    Auto = 3
    MagicDamage = 4
    PhysicalDamage = 5


class MainStatEnum(PlayerEnum):
    STR = 1
    DEX = 2
    MND = 3
    INT = 4


class PlayerStats:
    def __init__(
        self,
        job: JobEnum,
        wd: int,
        vit: int,
        main: int,
        crit: int,
        det: int,
        dh: int,
        ten: int,
        pie: int,
        sps: int,
        sks: int,
        level: int = 90,
        ilvlsync=None,
        partybonus: float = 1.0,
    ):
        self.Job = job
        self.Role = self.Job.RoleEnum()
        self.SpdType = self.Job.JobStat()

        self.WD = wd
        self.Vit = vit
        self.Main = main

        self.Crit = crit
        self.Det = det
        self.DH = dh
        self.Ten = ten
        self.Pie = pie
        self.Sps = sps
        self.Sks = sks

        self.Level = level
        self.iLvlSync = ilvlsync
        self.PartyBonus = partybonus

    def ComputeFunctions(self):
        constants = LevelConstants(self.Level)

        levelMod = constants.LevelMod
        baseMain = constants.BaseMain
        baseSub = constants.BaseSub

        jobMod = JobMod.value_for_name(self.Job.name)

        self.f_WD = (self.WD + math.floor(baseMain * jobMod / 1000)) / 100
        self.f_DET = (
            math.floor(1000 + math.floor(StatInt.Det * (self.Det - baseMain) / levelMod)) / 1000
        )  # Determination damage

        if self.Role == RoleEnum.Tank:
            # Tenacity damage, 1 for non-tank player
            self.f_TEN = (1000 + math.floor(StatInt.Ten * (self.Ten - baseSub) / levelMod)) / 1000
        else:
            self.f_TEN = 1  # if non-tank

        SS = 0
        # Used only for dots
        if self.SpdType == SpeedEnum.SkS:
            SS = self.Sks
        elif self.SpdType == SpeedEnum.SpS:
            SS = self.Sps

        self.f_SPD = (1000 + math.floor(StatInt.SS * (SS - baseSub) / levelMod)) / 1000

        self.CritRate = (
            math.floor((StatInt.Crit * (self.Crit - baseSub) / levelMod + 50)) / 1000
        )  # Crit rate in decimal
        self.CritMult = (
            math.floor(StatInt.Crit * (self.Crit - baseSub) / levelMod + 400)
        ) / 1000  # Crit Damage multiplier
        self.DHRate = math.floor(StatInt.DH * (self.DH - baseSub) / levelMod) / 1000  # DH rate in decimal

        self.SpSGCDReduction = (1000 - (StatInt.SS * (self.Sps - constants.BaseSub) / constants.LevelMod)) / 1000
        self.SkSGCDReduction = (1000 - (StatInt.SS * (self.Sks - constants.BaseSub) / constants.LevelMod)) / 1000
        self.GCDReduction = (1000 - (StatInt.SS * (SS - constants.BaseSub) / constants.LevelMod)) / 1000

    def PrintStats(self):
        print("Job: {:3}".format(self.Job.name))

        print("{:6}  {:4}  {:4}  {:4}  ".format("Level", "WD", "Main", "VIT"))
        print("{:6}  {:4}  {:4}  {:4}  ".format(self.Level, self.WD, self.Main, self.Vit))
        print()

        print("{:4}  {:4}  {:4}  {:4}  {:4}  {:4}  {:4}".format("CRT", "DET", "DIR", "TEN", "PIE", "SPS", "SKS"))
        print(
            "{:4}  {:4}  {:4}  {:4}  {:4}  {:4}  {:4}".format(
                self.Crit, self.Det, self.DH, self.Ten, self.Pie, self.Sps, self.Sks
            )
        )
        print()

        print("{:4}  {:4}  {:4}  {:4}".format("fWD", "fDET", "fTEN", "fSPD"))
        print("{:.3f}  {:.3f}  {:.3f}  {:.3f}".format(self.f_WD, self.f_DET, self.f_TEN, self.f_SPD))
        print()

        print("{:4}  {:4}  {:4}".format("CRT%", "fCRT", "DIR%"))
        print("{:.3f}  {:.3f}  {:.3f}".format(self.CritRate, self.CritMult, self.DHRate))

    @staticmethod
    def from_dict(stats):

        return PlayerStats(
            job=stats['Job'],
            wd=stats["WD"],
            vit=stats["Vit"],
            main=stats["MainStat"],
            crit=stats["Crit"],
            det=stats["Det"],
            dh=stats["DH"],
            ten=stats["Ten"],
            pie=stats["Pie"],
            sps=stats["Sps"],
            sks=stats["Sks"],
            level=stats["Level"],
            ilvlsync=stats["iLvlSync"],
            partybonus=stats["partyBonus"],
        )

    @staticmethod
    def base_stats(job: JobEnum, level: int = 90):
        constants = LevelConstants(level=level)

        return PlayerStats(
            job=job,
            wd=0,
            vit=0,
            main=constants.BaseMain,
            crit=constants.BaseSub,
            det=constants.BaseMain,
            dh=constants.BaseSub,
            ten=constants.BaseSub,
            pie=constants.BaseMain,
            sps=constants.BaseSub,
            sks=constants.BaseSub,
            level=level,
            ilvlsync=None,
            partybonus=1.0,
        )
