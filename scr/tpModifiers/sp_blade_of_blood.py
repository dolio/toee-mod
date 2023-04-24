from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from spell_utils import verifyItem

# args:
#  0: spell_id
#  1: duration
#  2: boost
#  3: extra

print "Registering sp_blade_of_blood"

def AddChar(weapon, args, evt_obj):
	spell_id = args.get_arg(0)
	duration = args.get_arg(1)
	boost = args.get_arg(2)

	weapon.item_condition_add_with_args(
			'Blade of Blood', boost, 0, 0, 0, spell_id)
	parent = weapon.obj_get_obj(obj_f_item_parent)

	return 0

def Ending(weapon, args, evt_obj):
	args.remove_spell()
	args.remove_spell_mod()
	return 0

def OnEnd(weapon, args, evt_obj):
	weapon.item_condition_remove('Blade of Blood', args.get_arg(0))
	return 0

wpn = PythonModifier('sp-Blade of Blood', 4)
wpn.AddHook(ET_OnConditionAdd, EK_NONE, AddChar, ())
wpn.AddHook(ET_OnD20Signal, EK_S_Dismiss_Spells, Ending, ())
wpn.AddHook(ET_OnConditionRemove, EK_NONE, OnEnd, ())

wpn.AddSpellDispelCheckStandard()
wpn.AddSpellTeleportPrepareStandard()
wpn.AddSpellTeleportReconnectStandard()
wpn.AddSpellCountdownStandardHook()

# args:
# 0: boost
# 1: discharged
# 2: weapon location #
# 3: extra
# 4: spell id

def BonusDmg(char, args, evt_obj):
	weapon = evt_obj.attack_packet.get_weapon_used()
	target = evt_obj.attack_packet.target

	boost = args.get_arg(0)

	if not verifyItem(weapon, args): return 0
	if args.get_arg(1): return 0 # already discharged somehow
	if target.is_category_type(mc_type_construct): return 0
	if target.is_category_type(mc_type_undead): return 0

	# set to discharge
	args.set_arg(1, 1)

	dice = dice_new('1d6')
	if boost: dice.num = 3

	evt_obj.damage_packet.add_dice(dice, D20DT_UNSPECIFIED, 3500)

	return 0

def Glow(char, args, evt_obj):
	if args.get_arg(1): return 0 # discharged somehow
	if verifyItem(evt_obj.get_obj_from_args(), args):
		if evt_obj.return_val < 3:
			evt_obj.return_val = 3

	return 0

def CheckEnd(char, args, evt_obj):
	weapon = evt_obj.attack_packet.get_weapon_used()

	if not verifyItem(weapon, args): return 0

	weapon.d20_send_signal(S_Dismiss_Spells, args.get_arg(4))

	return 0

def InvEnd(char, args, evt_obj):
	# Gets called on re-equipping. Presume this is the trigger that
	# ends the spell when the wielder has lost contact.
	inv_loc = args.get_arg(2)

	if inv_loc < 200: return 0

	weapon = char.item_worn_at(inv_loc-200)

	weapon.d20_send_signal(S_Dismiss_Spells, args.get_arg(4))

	return 0

cha = PythonModifier('Blade of Blood', 5, 0)
cha.AddHook(ET_OnDealingDamage, EK_NONE, BonusDmg, ())
cha.AddHook(ET_OnWeaponGlowType, EK_NONE, Glow, ())
cha.AddHook(ET_OnDealingDamage2, EK_NONE, CheckEnd, ())
cha.AddHook(ET_OnD20Signal, EK_S_Inventory_Update, InvEnd, ())
