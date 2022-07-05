#########################################
########## MACHINIST SPELL  #############
#########################################
import copy
from Jobs.Base_Spell import DOTSpell, Melee_AA, Queen_AA, empty, WaitAbility
from Jobs.Ranged.Machinist.Machinist_Player import Queen
from Jobs.Ranged.Ranged_Spell import MachinistSpell

Lock = 0

#Special

def AddGauge(Player, Battery, Heat):
    Player.BatteryGauge = min(100, Player.BatteryGauge + Battery)
    Player.HeatGauge = min(100, Player.HeatGauge + Heat)

def RemoveGauge(Player, Battery, Heat):
    Player.BatteryGauge = max(0, Player.BatteryGauge - Battery)
    Player.HeatGauge = max(0, Player.HeatGauge - Heat)
#Requirement

def OverheatedRequirement(Player, Spell):
    return Player.HyperchargeTimer > 0, -1 #True if Overheated

def WildFireRequirement(Player, Spell):
    return Player.WildFireCD <= 0, Player.WildFireCD

def AirAnchorRequirement(Player, Spell):
    return Player.AirAnchorCD <= 0, Player.AirAnchorCD

def BarrelStabilizerRequirement(Player, Spell):
    return Player.BarrelStabilizerCD <= 0, Player.BarrelStabilizerCD

def HyperchargeRequirement(Player, Spell):
    return Player.HyperchargeCD <= 0 and Player.HeatGauge >= 50, -1

def ReassembleRequirement(Player, Spell):
    return Player.ReassembleStack > 0, -1

def GaussRoundRequirement(Player, Spell):
    return Player.GaussRoundStack > 0, -1

def RicochetRequirement(Player, Spell):
    return Player.RicochetStack > 0, -1

def DrillRequirement(Player, Spell):
    return Player.DrillCD <= 0, Player.DrillCD

def OverdriveRequirement(Player, Spell):
    return Player.Overdrive, -1

def ChainSawRequirement(Player, Spell):
    return Player.ChainSawCD <= 0, Player.ChainSawCD

def AutomatonRequirement(Player, Spell):
    return (not Player.Overdrive) and Player.BatteryGauge >= 50, -1

def TacticianRequirement(Player, Spell):
    return Player.TacticianCD <= 0, Player.TacticianCD

#Apply

def ApplyTactician(Player, Enemy):
    Player.TacticianCD = 90

def ApplyScattergun(Player, Enemy):
    AddGauge(Player, 0, 10)

def ApplyBioblaster(Player, Enemy):
    ApplyDrill(Player, Enemy)
    if Player.BioblasterDOT == None:
        Player.BioblasterDOT = copy.deepcopy(BioblasterDOT)
        Player.DOTList.append(Player.BioblasterDOT)
        Player.BioblasterDOTTimer = 15
        Player.EffectCDList.append(BioblasterDOTCheck)
    Player.BioblasterDOTTimer = 15

def ApplyWildFire(Player, Enemy):
    Player.WildFireCD = 120
    Player.WildFireTimer = 10
    Player.EffectList.append(WildFireEffect)
    Player.EffectCDList.append(WildFireCheck)

def ApplyAirAnchor(Player, Enemy):
    AddGauge(Player, 20, 0)
    Player.AirAnchorCD = 40

def ApplyBarrelStabilizer(Player, Enemy):
    AddGauge(Player, 0, 50)
    Player.BarrelStabilizerCD = 120

def ApplyHeatBlast(Player, Enemy):
    Player.GaussRoundCD = max(0, Player.GaussRoundCD - 15)
    Player.RicochetCD = max(0, Player.RicochetCD - 15)

def ApplyHypercharge(Player, Enemy):
    Player.HyperchargeTimer = 8
    Player.HyperchargeCD = 10
    RemoveGauge(Player, 0, 50)#cost
    Player.EffectList.append(HyperchargeEffect)
    Player.EffectCDList.append(HyperchargeCheck)

def ApplyReassemble(Player, Enemy):
    if Player.ReassembleStack == 2:
        Player.EffectCDList.append(ReassembleStackCheck)
        Player.ReassembleCD = 55
    Player.ReassembleStack -= 1
    Player.Reassemble = True
    
def ApplyGaussRound(Player, Enemy):
    if Player.GaussRoundStack == 3:
        Player.EffectCDList.append(GaussRoundStackCheck)
        Player.GaussRoundCD = 30
    Player.GaussRoundStack -= 1

def ApplyRicochet(Player, Enemy):
    if Player.RicochetStack == 3:
        Player.EffectCDList.append(RicochetStackCheck)
        Player.RicochetCD = 30
    Player.RicochetStack -= 1

def ApplyDrill(Player, Enemy):
    Player.DrillCD = 20

def ApplyOverdrive(Player, Enemy):
    Player.Overdrive = False
    Player.Queen.ActionSet.insert(0,Collider)
    Player.Queen.ActionSet.insert(0,Bunker)

def ApplyChainSaw(Player, Enemy):
    AddGauge(Player, 20, 0)
    Player.ChainSawCD = 60

def ApplyAutomaton(Player, Enemy):
    Player.QueenStartUpTimer = 5
    Player.EffectCDList.append(QueenStartUpCheck)

def SummonQueen(Player, Enemy):
    #input("SummoningQueen at : " + str(Player.CurrentFight.TimeStamp))
    Player.AutomatonQueenCD = 6

    QueenTimer = (Player.BatteryGauge - 50)/5 + 5 #Queen timer by linearly extrapolating 10 sec base + extra battery Gauge
    #Queen Timer = (ExtraBatteryGauge) / BatteryPerSec - StartUpTimer + BaseTimer = Battery/5 - 5 + 10
    Player.BatteryGauge = 0
    if Player.Queen == None : Queen(Player, 10)#Creating new queen
    Player.Queen.Timer = 15 #Setting Queen Timer
    #Will have to depend on battery Gauge
    #Timer is set at 10 so we can have 2 GCD to do finisher move if reaches before
    Player.Queen.EffectCDList.append(QueenCheck)
    Player.Queen.ActionSet.append(Queen_AA)
    Player.Queen.ActionSet.append(WaitAbility(QueenTimer - 3)) #Gives 3 last sec to do finishing move
    Player.Queen.TrueLock = False #Delocking the queen if she was in a locked state, would happen is resummoned

def ApplyCollider(Queen, Enemy):#Called on queen
    Queen.Master.QueenOnField = False

#Combo Actions

def ApplySplitShot(Player, Enemy):
    AddGauge(Player, 0, 5)
    Player.EffectList.append(SplitShotEffect)

def ApplySlugShot(Player, Enemy):
    AddGauge(Player, 0, 5)
    Player.EffectList.append(SlugShotEffect)

def ApplyCleanShot(Player, Enemy):
    AddGauge(Player, 10, 5)

#Effect

def WildFireEffect(Player, Spell):
    if isinstance(Spell, MachinistSpell) and Spell.Weaponskill : Player.WildFireStack +=1

def HyperchargeEffect(Player, Spell):
    if Spell.Weaponskill : Spell.Potency += 20

#Combo Actions effect

def SplitShotEffect(Player, Spell):
    if Spell.id == 5:

        Spell.Potency =+ 160
        Player.EffectToRemove.append(SplitShotEffect)

def SlugShotEffect(Player, Spell):
    if Spell.id == 6:

        Spell.Potency += 250
        Player.EffectToRemove.append(SlugShotEffect)


#Check

def QueenStartUpCheck(Player, Enemy):
    if Player.QueenStartUpTimer <= 0:
        SummonQueen(Player, Enemy) #Waits for 5 sec then summons the queen
        Player.EffectToRemove.append(QueenStartUpCheck)

def FlamethrowerDOTCheck(Player, Enemy):
    if Player.FlamethrowerDOTTimer <= 0:
        Player.DOTList.remove(Player.FlamethrowerDOT)
        Player.FlamethrowerDOT = None
        Player.EffectToRemove.append(FlamethrowerDOTCheck )

def BioblasterDOTCheck(Player, Enemy):
    if Player.BioblasterDOTTimer <= 0:
        Player.DOTList.remove(Player.BioblasterDOT)
        Player.BioblasterDOT = None
        Player.EffectToRemove.append(BioblasterDOTCheck)

def WildFireCheck(Player, Enemy):
    if Player.WildFireTimer <= 0:

        WildFireOff = MachinistSpell(1, False, 0, 0, 220 * Player.WildFireStack, 0, empty, [], False)
        #Temporary Spell that will be put in front of the Queue
        Player.ActionSet.insert(Player.NextSpell+1, WildFireOff) #Insert in queue, will be instantly executed
        Player.EffectList.remove(WildFireEffect)
        Player.EffectToRemove.append(WildFireCheck)
        Player.WildFireStack = 0

def HyperchargeCheck(Player, Enemy):
    if Player.HyperchargeTimer <= 0:
        #print("Hypercharge went off at : " + str(Player.CurrentFight.TimeStamp))
        Player.EffectList.remove(HyperchargeEffect)
        Player.EffectToRemove.append(HyperchargeCheck)

def ReassembleStackCheck(Player, Enemy):
    if Player.ReassembleCD <= 0:
        if Player.ReassembleStack == 1:
            Player.EffectToRemove.append(ReassembleStackCheck)
        else:
            Player.ReassembleCD = 55
        Player.ReassembleStack +=1

def GaussRoundStackCheck(Player, Enemy):
    if Player.GaussRoundCD <= 0:
        if Player.GaussRoundStack == 2:
            Player.EffectToRemove.append(GaussRoundStackCheck)
        else:
            Player.GaussRoundCD = 30
        Player.GaussRoundStack +=1

def RicochetStackCheck(Player, Enemy):
    if Player.RicochetCD <= 0:
        if Player.RicochetStack == 2:
            Player.EffectToRemove.append(RicochetStackCheck)
        else:
            Player.RicochetCD = 30
        Player.RicochetStack +=1

def QueenCheck(Player, Enemy):#This will be called on the queen
    if Player.Timer <= 0: 
        #input("Begining at : " + str(Player.CurrentFight.TimeStamp))
        Player.Master.Overdrive = False
        Player.TrueLock = False #Delocking the Queen so she can perform these two abilities
        Player.ActionSet.insert(Player.NextSpell+1,Bunker)
        Player.ActionSet.insert(Player.NextSpell+2,Collider)
        Player.EffectToRemove.append(QueenCheck)
        ##input(Player.ActionSet)
        ##input(Player.NextSpell)
        Player.EffectCDList.append(QueenAACheck)


def QueenAACheck(Player, Enemy):
    if Player.TrueLock:#This function will be called on the Queen once it has finished Collider, it will get rid of AA's
        #It checks for when the Queen is done
        Player.DOTList = [] #Reset DOTList
        Player.EffectToRemove.append(QueenAACheck)



Wildfire = MachinistSpell(0, False, 0, Lock, 0, 0, ApplyWildFire, [WildFireRequirement], False)
AirAnchor = MachinistSpell(2, True, 0, 2.5, 580, 0, ApplyAirAnchor, [AirAnchorRequirement], True)
BarrelStabilizer = MachinistSpell(3, False, 0, Lock, 0, 0, ApplyBarrelStabilizer, [BarrelStabilizerRequirement], False)
HeatBlast = MachinistSpell(7, True, Lock, 1.5, 180, 0, ApplyHeatBlast, [OverheatedRequirement], True)
Hypercharge = MachinistSpell(8, False, 0, Lock, 0, 0, ApplyHypercharge, [HyperchargeRequirement], False)
Reassemble = MachinistSpell(9, False, 0, Lock, 0, 0, ApplyReassemble, [ReassembleRequirement], False)
GaussRound = MachinistSpell(10, False, 0, Lock, 120, 0, ApplyGaussRound, [GaussRoundRequirement], False)
Ricochet = MachinistSpell(11, False, 0, Lock, 120, 0, ApplyRicochet, [RicochetRequirement], False)
Drill = MachinistSpell(12, True, 0, 2.5, 580, 0, ApplyDrill, [DrillRequirement], True)
ChainSaw = MachinistSpell(17, True, 0, 2.5, 580, 0, ApplyChainSaw, [ChainSawRequirement], True)
Tactician = MachinistSpell(18, False, 0, 0, 0, 0, ApplyTactician, [TacticianRequirement], False)
#Combo Action

SplitShot = MachinistSpell(4, True, Lock, 2.5, 200, 0, ApplySplitShot, [], True)
SlugShot = MachinistSpell(5, True, Lock, 2.5, 120, 0, ApplySlugShot, [], True )
CleanShot = MachinistSpell(6, True, Lock, 2.5, 110, 0, ApplyCleanShot, [], True)


#AOE GCD
AutoCrossbow = MachinistSpell(1, True, 0, 1.5, 140, 0, empty, [OverheatedRequirement], True)
Scattergun = MachinistSpell(1, True, 0, 2.5, 150, 0, ApplyScattergun, [], True)
Bioblaster = MachinistSpell(1, True, 0, 0, 50, 0, ApplyBioblaster, [DrillRequirement], True) #Shares CD with Drill
BioblasterDOT = DOTSpell(-2, 50, True)
FlamethrowerDOT = DOTSpell(-3, 80, True)
def Flamethrower(time):
    #This function will apply a dot for the specified duration, and lock the player for this duration



    def FlamethrowerRequirement(Player, Spell):
        return time > 10 and Player.FlamethrowerCD <= 0, Player.FlamethrowerCD

    def ApplyFlamethrower(Player, Enemy):
        Player.FlamethrowerCD = 60
        Player.FlamethrowerDOTTimer = time
        Player.FlamethrowerDOT = copy.deepcopy(FlamethrowerDOT)
        Player.DOTList.append(Player.FlamethrowerDOT)
        Player.EffectCDList.append(FlamethrowerDOTCheck)

    return MachinistSpell(1, True, time, time, 0, 0, ApplyFlamethrower, [FlamethrowerRequirement], False)

#Queen's Ability

#These abilities will write into the Queen's ability list.
#If they are not done the queen will do them automatically
Automaton = MachinistSpell(14, False, 0, Lock, 0, 0, ApplyAutomaton, [], False)
Overdrive = MachinistSpell(13, False, 0, Lock, 0, 0, ApplyOverdrive, [], False)
#These will be casted by the machinist, so they have no damage. Their only effect is to add into Queen's Queue
Bunker = MachinistSpell(15, True, 0, 2.5, 680, 0, ApplyCollider, [], False)   #Triggered by Overdrive
Collider = MachinistSpell(16, True, 0 , 2.5, 780, 0, ApplyCollider, [], False)  #Spell Queen will cast

MachinistAbility = {7411 : SplitShot, 7412 : SlugShot, 25788 : ChainSaw, 25768 : Scattergun, 17209 : Hypercharge, 16889 : Tactician, 16502:Overdrive, 16501:Automaton,
16500 : AirAnchor, 16499 : Bioblaster, 16498:Drill, 16497 : AutoCrossbow, 7418 : Flamethrower, 7414 : BarrelStabilizer, 7413 : CleanShot, 7410 : HeatBlast, 2878 : Wildfire,
2874 : GaussRound, 2890 : Ricochet }