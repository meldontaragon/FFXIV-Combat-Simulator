# this file contains job, level, and stat constants

from enum import IntEnum
from aenum import NamedConstant
import math

# from ffxivcalc.Jobs.PlayerEnum import JobEnum


class StatConsant(NamedConstant):
    @classmethod
    def value_for_name(cls, name: str) -> int:
        # maps from name -> id
        if name in cls.__dict__.keys():
            return cls.__dict__[name]
        return 0  # Evaluated as Unknown


class JobMod(StatConsant):
    BlackMage = 115
    RedMage = 115
    Summoner = 115
    Astrologian = 115
    Scholar = 115
    Sage = 115
    WhiteMage = 115
    Dragoon = 115
    Monk = 110
    Ninja = 110
    Reaper = 115
    Samurai = 112
    Bard = 115
    Dancer = 115
    Machinist = 115
    DarkKnight = 105
    Gunbreaker = 100
    Paladin = 100
    Warrior = 105


class StatInt(StatConsant):
    DH = 550
    Crit = 200
    Det = 140
    SS = 130
    Pie = 150
    Ten = 100
    Def = 15
    BlockRate = 30
    BlockStrength = 15
    BaseHP = 22.1
    TankHP = 31.5


class LevelConstants:
    """
    This class contains all constants associated with a single level
    """

    def __init__(self, level: int):

        self._levelmodhp = 0
        self._levelmoddiv = 0
        self._levelmodmain = 0
        self._levelmodsub = 0
        self._apint = 0
        self._tankapint = 0

        match level:
            case 70:
                self._levelmodhp = 1700
                self._levelmoddiv = 900
                self._levelmodmain = 292
                self._levelmodsub = 364
                self._apint = 125
                self._tankapint = 105

            case 80:
                self._levelmodhp = 2000
                self._levelmoddiv = 1300
                self._levelmodmain = 340
                self._levelmodsub = 380
                self._apint = 165
                self._tankapint = 115

            case 90:
                self._levelmodhp = 3000
                self._levelmoddiv = 1900
                self._levelmodmain = 390
                self._levelmodsub = 400
                self._apint = 195
                self._tankapint = 156

                return

    def _get_levelmodhp(self):
        return self._levelmodhp

    def _get_levelmoddiv(self):
        return self._levelmoddiv

    def _get_levelmodsub(self):
        return self._levelmodsub

    def _get_levelmodmain(self):
        return self._levelmodmain

    def _get_apint(self):
        return self._apint

    def _get_tankapint(self):
        return self._tankapint

    ModHP = property(fget=_get_levelmodhp, fset=None, fdel=None, doc='HP Modifier')

    LevelMod = property(fget=_get_levelmoddiv, fset=None, fdel=None, doc='Level Divisor Modifier')

    BaseSub = property(fget=_get_levelmodsub, fset=None, fdel=None, doc='Base Value for Sub Stats')

    BaseMain = property(fget=_get_levelmodmain, fset=None, fdel=None, doc='Base Value for Main Stats')

    APInt = property(fget=_get_apint, fset=None, fdel=None, doc='Main Stat Integer')

    TankAPInt = property(fget=_get_tankapint, fset=None, fdel=None, doc='Tank Main Stat Integer')
