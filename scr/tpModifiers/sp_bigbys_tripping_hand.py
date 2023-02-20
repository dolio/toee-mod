from toee import *
import tpdp
from templeplus.pymod import PythonModifier
from spell_utils import *

print "registering sp_bigbys_tripping_hand"

# args
# 0: spell_ability
# 1: spell_ability_mod
# 2: caster_level
# 3: willpower
# 4: spare

def BonusStr(stat):
	str = "Strength"
	if stat == stat_dexterity:
		str = "Dexterity"
	elif stat == stat_constitution:
		str = "Constitution"
	elif stat == stat_intelligence:
		str = "Intelligence"
	elif stat == stat_wisdom:
		str = "Wisdom"
	elif stat == stat_charisma:
		str = "Charisma"

	return "Caster ~{}~[TAG_{}] Bonus".format(str, str.upper())

def BaseToHit(attachee, args, evt_obj):
	bonus = args.get_arg(2) - 1

	evt_obj.bonus_list.add(bonus, 1, 'Caster Level')

	return 0

def ToHit(attachee, args, evt_obj):
	stat = args.get_arg(0)
	bonus = args.get_arg(1)

	evt_obj.bonus_list.add(bonus, 0, BonusStr(stat))
	return 0

def ToTrip(attachee, args, evt_obj):
	bonus = min(5, args.get_arg(2) / 3)

	evt_obj.bonus_list.add(bonus, 0, 'Caster Level Bonus')
	return 0

def Will(attachee, args, evt_obj):
	bonus = args.get_arg(3)
	
	evt_obj.bonus_list.add(bonus, 1, 'Caster Willpower')
	return 0

def NoConceal(attachee, args, evt_obj):
	evt_obj.return_val = 1
	return 0

buff = PythonModifier("sp-Bigby's Tripping Hand", 6)
buff.AddHook(ET_OnToHitBonusBase, EK_NONE, BaseToHit, ())
buff.AddHook(ET_OnToHitBonus2, EK_NONE, ToHit, ())
buff.AddHook(ET_OnGetAbilityCheckModifier, EK_NONE, ToTrip, ())
buff.AddHook(ET_OnD20Query, EK_Q_Critter_Can_See_Invisible, NoConceal, ())
buff.AddHook(ET_OnD20Query, EK_Q_Critter_Can_See_Ethereal, NoConceal, ())
buff.AddHook(ET_OnSaveThrowLevel, EK_SAVE_WILL, Will, ())
