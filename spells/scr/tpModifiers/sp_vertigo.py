from toee import *
import tpdp
from templeplus.pymod import PythonModifier
from spell_utils import *

def Descr(spell_id):
	packet = tpdp.SpellPacket(spell_id)

	return game.get_spell_mesline(packet.spell_enum)

def Penalty(attachee, args, evt_obj):
	spell_id = args.get_arg(0)

	evt_obj.bonus_list.add(-2, 0, Descr(spell_id))
	return 0

def reflex_roll_delta(target, dc):
	dice = dice_new('1d20')

	reflex_mod = target.stat_level_get(stat_save_reflexes)
	bonus = tpdp.BonusList()
	bonus.add(reflex_mod, 0, "~Reflex~[TAG_SAVE_REFLEX] Saves")
	roll = dice.roll()

	hist = tpdp.create_history_dc_roll(
			target, dc, dice, roll, "Reflexive Balance", bonus)

	game.create_history_from_id(hist)

	print roll

	return roll + reflex_mod - dc

def Balance(target, args, evt_obj):
	# swap the commenting on the `result` lines if balance is
	# valid in the module you are playing and you want to use it.

	# result = target.skill_roll_delta(skill_balance, 10, 1)
	result = reflex_roll_delta(target, 10)

	if result >= 0:
		return 0
	elif result < -4:
		target.fall_down()

	target.condition_add_with_args('Unsteady', 0, 0)
	return 0

def Remove(attachee, args, evt_obj):
	args.condition_remove()
	return 0

vertigo = PythonModifier('sp-Vertigo', 4)
vertigo.AddHook(ET_OnGetTooltip, EK_NONE, spellTooltip, ())
vertigo.AddHook(ET_OnGetEffectTooltip, EK_NONE, spellEffectTooltip, ())
vertigo.AddHook(ET_OnToHitBonus2, EK_NONE, Penalty, ())
vertigo.AddHook(ET_OnSaveThrowLevel, EK_NONE, Penalty, ())
vertigo.AddHook(ET_OnD20Signal, EK_S_BeginTurn, Balance, ())
vertigo.AddHook(ET_OnD20Signal, EK_S_Killed, Remove, ())
vertigo.AddHook(ET_OnD20Signal, EK_S_Dismiss_Spells, checkRemoveSpell, ())
vertigo.AddSpellDispelCheckStandard()
vertigo.AddSpellTeleportPrepareStandard()
vertigo.AddSpellTeleportReconnectStandard()
vertigo.AddSpellCountdownStandardHook()

def Unsteady(attachee, args, evt_obj):
	# flags, newCap, capType, mesline
	evt_obj.bonus_list.set_overall_cap(1, 0, 0, 1004)
	evt_obj.bonus_list.set_overall_cap(2, 0, 0, 1004)
	return 0

def UTooltip(attachee, args, evt_obj):
	evt_obj.append('Unsteady')
	return 0

def UETooltip(attachee, args, evt_obj):
	key = tpdp.hash('UNSTEADY')
	evt_obj.append(key, -2, '')
	return 0

unsteady = PythonModifier('Unsteady', 2)
unsteady.AddHook(ET_OnGetTooltip, EK_NONE, UTooltip, ())
unsteady.AddHook(ET_OnGetEffectTooltip, EK_NONE, UETooltip, ())
unsteady.AddHook(ET_OnGetMoveSpeed, EK_NONE, Unsteady, ())
unsteady.AddHook(ET_OnD20Signal, EK_S_EndTurn, Remove, ())
unsteady.AddHook(ET_OnD20Signal, EK_S_Combat_End, Remove, ())
unsteady.AddHook(ET_OnD20Signal, EK_S_Killed, Remove, ())
