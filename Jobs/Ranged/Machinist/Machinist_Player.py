#########################################
########## MACHINIST PLAYER #############
#########################################
from Jobs.Ranged.Ranged_Player import Ranged

class Machinist(Ranged):
    
    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Gauge
        self.BatteryGauge = 0
        self.HeatGauge = 0


        #CD
        self.ChainSawCD = 0
        self.AirAnchorCD = 0
        self.BarrelStabilizerCD = 0
        self.DrillCD = 0
        self.WildFireCD = 0
        self.GaussRoundCD = 0
        self.ReassembleCD = 0
        self.HotShotCD = 0
        self.HyperchargeCD = 0
        self.RicochetCD = 0
        self.AutomatedQueenCD = 0

        #Timer
        self.WildFireTimer = 0
        self.HyperchargeTimer = 0

        #Stacks
        self.GaussRoundStack = 3
        self.ReassembleStack = 2
        self.RicochetStack = 3
        self.WildFireStack = 0  #Used to know how many weaponskills have hit during Wildfire
        self.Reassemble = False

        #Combo Action
        self.SlugShot = False
        self.CleanShot = False

        #Queen
        self.Queen = None
        self.Overdrive = False  #Used to know if we can cast overdrive. Its set to true once the Queen is summoned and set to false when Overdrive is used
        self.QueenOnField = False

        self.MultDPSBonus = 1.2

        

    def updateCD(self, time):
        if (self.ChainSawCD > 0) : self.ChainSawCD = max(0,self.ChainSawCD - time)
        if (self.AirAnchorCD > 0) : self.AirAnchorCD = max(0,self.AirAnchorCD - time)
        if (self.BarrelStabilizerCD > 0) : self.BarrelStabilizerCD = max(0,self.BarrelStabilizerCD - time)
        if (self.DrillCD > 0) : self.DrillCD = max(0,self.DrillCD - time)
        if (self.GaussRoundCD > 0) : self.GaussRoundCD = max(0,self.GaussRoundCD - time)
        if (self.WildFireCD > 0) : self.WildFireCD = max(0,self.WildFireCD - time)
        if (self.HotShotCD > 0) : self.HotShotCD = max(0,self.HotShotCD - time)
        if (self.HyperchargeCD > 0) : self.HyperchargeCD = max(0,self.HyperchargeCD - time)
        if (self.RicochetCD > 0) : self.RicochetCD = max(0,self.RicochetCD - time)
        if (self.AutomatedQueenCD > 0) : self.AutomatedQueenCD = max(0,self.AutomatedQueenCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.WildFireTimer > 0) : self.WildFireTimer = max(0,self.WildFireTimer - time)
        if (self.HyperchargeTimer > 0) : self.HyperchargeTimer = max(0,self.HyperchargeTimer - time)


#Queen Player

class Queen(Ranged):

    def __init__(self, Machinist, Timer):
        super().__init__(Machinist.GCDTimer, [], [], [], Machinist.CurrentFight, Machinist.Stat)


        self.Master = Machinist

        self.Timer = Timer
        self.Master.Queen = self  #Giving the Queen's pointer to the Machinist
        self.Master.CurrentFight.PlayerList.append(self)
        self.MultDPSBonus = 1.2


    def updateCD(self, time):
        pass

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.Timer > 0) : self.Timer = max(0,self.Timer - time)