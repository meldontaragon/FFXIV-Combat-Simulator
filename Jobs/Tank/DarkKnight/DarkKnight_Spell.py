#########################################
########## DARK KNIGHT SKILLS ###########
#########################################
from Jobs.Base_Spell import DOTSpell, buff, empty
import copy
from Jobs.Tank.DarkKnight.DarkKnight_Player import Esteem
from Jobs.Tank.Tank_Spell import DRKSkill
Lock = 0.75

#def DarksideEffect(Player, Spell):
 #   if Player.DarksideTimer > 0:
  #      Spell.Potency *= 1.10

#Requirements for each Skill and Ability.

def BloodRequirement(Player, Spell):
    #print("Delirium stacks: "+ str(Player.DeliriumStacks))
    if Player.DeliriumStacks > 0 and (Spell.id == 4 or Spell.id == 5):
        Spell.BloodCost = 0
        Player.DeliriumStacks -= 1
        return True, -1
    elif Player.Blood >= 50:
        Player.Blood -= 50
        return True, -1
    return False, -1

def EdgeShadowRequirement(Player, Spell):
    if Player.EdgeShadowCD <= 0 :
        if Player.DarkArts:
            Spell.ManaCost = 0
            Player.DarkArts = False
            return True, -1
        elif Player.Mana >= Spell.ManaCost:
            Player.Mana -= Spell.ManaCost
            return True, -1
    return False, -1

def BloodWeaponRequirement(Player, Spell):
    return Player.BloodWeaponCD <= 0, Player.BloodWeaponCD

def DeliriumRequirement(Player, Spell):
    return Player.DeliriumCD <= 0, Player.DeliriumCD

def CarveSpitRequirement(Player, Spell):
    return Player.CarveSpitCD <= 0, Player.CarveSpitCD

def AbyssalDrainRequirement(Player, Spell):
    return Player.AbyssalDrainCD <= 0, Player.AbyssalDrainCD

def SaltedEarthRequirement(Player, Spell):
    return Player.SaltedEarthCD <= 0, Player.SaltedEarthCD

def SaltDarknessRequirement(Player, Spell):
    return Player.SaltedEarthTimer > 0, -1

def ShadowbringerRequirement(Player, Spell):
    return Player.DarksideTimer > 0 and Player.ShadowbringerCharges > 0, -1


def PlungeRequirement(Player, Spell):
    return Player.PlungeCharges > 0, Player.PlungeChargesCD

def TBNRequirement(Player, Spell):
    if Player.Mana >= Spell.ManaCost:
        Player.Mana -= Spell.ManaCost
        return True, -1
    return False, -1

#Effect functions that persist after action use

def BloodWeaponEffect(Player, Spell):
    #print("Blood Weapon active")
    if Spell.GCD:
        Player.Mana = min(Player.Mana + 600, 10000)
        Player.Blood = min(100, Player.Blood + 10)

def DeliriumEffect(Player, Spell):
    #print("Delirium active")
    if Spell.id == Bloodspiller.id:
        Player.Mana = min(Player.Mana + 200, 10000)
    elif Spell.id == Quietus.id:
        Player.Mana = min(Player.Mana + 500, 10000)

def HardSlashEffect(Player, Spell):
    if Spell.id == 2:
        Multiplier = Spell.Potency/120
        BonusDmg = 140 * Multiplier
        Spell.Potency += BonusDmg
        Player.Mana = min(Player.Mana + 600, 10000)
    if (Spell.id == 2) or (Spell.id == 3) or (Spell.id == 1):
        Player.EffectToRemove.append(HardSlashEffect)

def SyphonStrikeEffect(Player, Spell):
    if Spell.id == 3:
        Multiplier = Spell.Potency/120
        BonusDmg = 220 * Multiplier
        Spell.Potency += BonusDmg
        Player.Blood = min(100, Player.Blood + 20)
    if (Spell.id == 2) or (Spell.id == 3) or (Spell.id == 1):
        Player.EffectToRemove.append(SyphonStrikeEffect)

#Cooldown checks to remove effect and restore charges

def BloodWeaponCheck(Player, Spell):
    if Player.BloodWeaponTimer <= 0 or Player.BloodWeaponStacks == 0:
        Player.EffectList.remove(BloodWeaponEffect)
        Player.EffectToRemove.append(BloodWeaponCheck)

def DeliriumCheck(Player, Spell):
    if Player.DeliriumTimer <= 0 or Player.DeliriumStacks == 0:
        Player.EffectList.remove(DeliriumEffect)
        Player.EffectToRemove.append(DeliriumCheck)

def SaltedEarthCheck(Player, Spell):
    if Player.SaltedEarthTimer <= 0:
        Player.DOTList.remove(SaltedEarthDOT)
        Player.SaltedEarthTimer = 0
        Player.EffectToRemove.append(SaltedEarthCheck)

def CheckShadowbringerCharge(Player, Enemy):
    if Player.ShadowbringerCD <= 0:
        if Player.ShadowbringerCharges == 0:
            Player.ShadowbringerCD = 30
        if Player.ShadowbringerCharges == 1:
            Player.EffectToRemove.append(CheckShadowbringerCharge)
        Player.ShadowbringerCharges +=1

def CheckPlungeCharge(Player, Enemy):
    if Player.PlungeCD <= 0:
        if Player.PlungeCharges == 0:
            Player.PlungeCD = 30
        if Player.PlungeCharges == 1:
            Player.EffectToRemove.append(CheckPlungeCharge)
        Player.PlungeCharges +=1


#Apply effects that happen upon action use

def ApplyHardSlashEffect(Player, Spell):
    Player.EffectList.append(HardSlashEffect)

def ApplySyphonEffect(Player, Spell):
    Player.EffectList.append(SyphonStrikeEffect)

def ApplyBloodWeaponEffect(Player, Spell):
    Player.BloodWeaponCD = 60                     
    Player.EffectList.append(BloodWeaponEffect)
    Player.BloodWeaponStacks = 5
    Player.BloodWeaponTimer = 15
    Player.EffectCDList.append(BloodWeaponCheck)

def ApplyDeliriumEffect(Player, Spell):
    Player.DeliriumCD = 60
    Player.EffectList.append(DeliriumEffect)
    Player.DeliriumStacks = 3
    Player.DeliriumTimer = 30 
    Player.EffectCDList.append(DeliriumCheck)

def ApplyEdgeShadowEffect(Player, Spell):
    Player.DarksideTimer = min(60, Player.DarksideTimer + 30)
    if not (CheckEdgeShadow in Player.EffectCDList):
        Player.buffList.append(EdgeShadowBuff)
        Player.EffectCDList.append(CheckEdgeShadow)

def CheckEdgeShadow(Player, Enemy):
    if Player.DarksideTimer <= 0:
        Player.buffList.remove(EdgeShadowBuff)
        Player.EffectCDList.remove(CheckEdgeShadow)

def ApplyCarveSpitEffect(Player, Spell):
    Player.CarveSpitCD = 60
    Player.AbyssalDrainCD = 60
    Player.Mana = min(Player.Mana + 600, 10000)

def ApplyAbyssalDrainEffect(Player, Spell):
    Player.AbyssalDrainCD = 60
    Player.CarveSpitCD = 60

def ApplySaltedEarth(Player, Spell):
    Player.SaltedEarthCD = 90
    Player.SaltedEarthTimer = 15
    Player.DOTList.append(SaltedEarthDOT)

def ApplySaltDarknessEffect(Player, Spell):
    Player.SaltDarknessCD = 15

def SpendShadowbringer(Player, Spell):
    if Player.ShadowbringerCharges == 2 :
        Player.ShadowbringerCD = 60
    Player.ShadowbringerCharges -= 1
    Player.EffectCDList.append(CheckShadowbringerCharge)

def SummonLivingShadow(Player, Spell):
    Actions = [PDelay, PAbyssalDrain, PPlunge, PQuietus, PShadowbringer, PEdgeShadow, PBloodspiller, PCarveSpit]
    Pet = Esteem(2.5,Actions,[],[],Player.CurrentFight,Player)
    Player.CurrentFight.PlayerList.append(Pet)
    Player.EsteemPointer = Pet
    #print("Esteem enters the battlefield.")

def SpendPlunge(Player,Spell):
    if Player.PlungeCharges == 2 :
        Player.PlungeCD = 30
    Player.PlungeCharges -= 1
    Player.EffectCDList.append(CheckPlungeCharge)

def ApplyDarkArts(Player, Spell):
    Player.DarkArts = True


#List of Weaponskills and Spells used by a Dark Knight Player.
DRKGCD = 2.41           #GCD speed
Lock = 0.75             #Fixed value for animation lock.

HardSlash = DRKSkill(1, True, Lock, DRKGCD, 170, 0, 0, ApplyHardSlashEffect, [])
SyphonStrike = DRKSkill(2, True, Lock, DRKGCD, 120, 0, 0, ApplySyphonEffect, [])
Souleater = DRKSkill(3, True, Lock, DRKGCD, 120, 0, 0, empty, [])
Bloodspiller = DRKSkill(4, True, Lock, DRKGCD, 500, 0, 50, empty, [BloodRequirement])
Quietus = DRKSkill(5, True, Lock, DRKGCD, 200, 0, 50, empty, [BloodRequirement])
Unmend = DRKSkill(6, True, Lock, 2.50, 150, 0, 0, empty, [])

#List of Buffs used by a Dark Knight Player.

BloodWeapon = DRKSkill(7, False, Lock, 0, 0, 0, 0, ApplyBloodWeaponEffect, [BloodWeaponRequirement])
Delirium = DRKSkill(8, False, Lock, 0, 0, 0, 0, ApplyDeliriumEffect, [DeliriumRequirement])

#List of Abilities used by a Dark Knight Player.

EdgeShadow = DRKSkill(9, False, Lock, 0, 460, 3000, 0, ApplyEdgeShadowEffect, [EdgeShadowRequirement])
FloodShadow = DRKSkill(10, False, Lock, 0, 160, 3000, 0, ApplyEdgeShadowEffect, [EdgeShadowRequirement])
CarveSpit = DRKSkill(11, False, Lock, 0, 510, 0, 0, ApplyCarveSpitEffect, [CarveSpitRequirement])
AbyssalDrain = DRKSkill(12, False, Lock, 0, 150, 0, 0, ApplyAbyssalDrainEffect, [AbyssalDrainRequirement])
SaltedEarth = DRKSkill(13, False, Lock, 0, 50, 0, 0, ApplySaltedEarth, [SaltedEarthRequirement]) #Ground target DOT, ticks once upon placement.
SaltedEarthDOT = DOTSpell(14, 50, True)
SaltDarkness = DRKSkill(15, False, Lock, 0, 500, 0, 0, empty, [SaltDarknessRequirement])
Shadowbringer = DRKSkill(16, False, Lock, 0, 600, 0, 0, SpendShadowbringer, [ShadowbringerRequirement])
LivingShadow = DRKSkill(17, False, Lock, 0, 0, 0, 50, SummonLivingShadow, [BloodRequirement])
Plunge = DRKSkill(18, False, Lock, 0, 150, 0, 0, SpendPlunge, [PlungeRequirement])

TBN = DRKSkill(27, False, Lock, 0, 0, 3000, 0, ApplyDarkArts, [TBNRequirement])     #Simply makes the next EdgeShadow free for now.

#List of Abilities performed by Living Shadow.

PAbyssalDrain = DRKSkill(19, True, 0.5, 2.36, 300, 0, 0, empty, [])
PPlunge = DRKSkill(20, True, 0.5, 2.36, 300, 0, 0, empty, [])
PQuietus = DRKSkill(21, True, 0.5, 2.36, 300, 0, 0, empty, [])
PShadowbringer = DRKSkill(22, True, 0.5, 2.36, 450, 0, 0, empty, [])
PEdgeShadow = DRKSkill(23, True, 0.5, 2.36, 300, 0, 0, empty, [])
PBloodspiller = DRKSkill(24, True, 0.5, 2.36, 300, 0, 0, empty, [])
PCarveSpit = DRKSkill(25, True, 0.5, 2.36, 300, 0, 0, empty, [])
PDelay = DRKSkill(26, True, 0, 4.50, 0, 0, 0, empty, [])    #6s animation before it starts attacking.

#buff
EdgeShadowBuff = buff(1.1)