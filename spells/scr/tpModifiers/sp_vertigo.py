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

def Balance(target, args, evt_obj):
	result = target.skill_roll_delta(skill_tumble, 10, 1)
	print result
	if result >= 0:
		return 0
	elif result < -4:
		target.fall_down()

	target.condition_add_with_args('Dizzy', 0, 0)
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
vertigo.AddSpellDispelCheckStandard()
vertigo.AddSpellTeleportPrepareStandard()
vertigo.AddSpellTeleportReconnectStandard()
vertigo.AddSpellCountdownStandardHook()

def Dizzy(attachee, args, evt_obj):
	# flags, newCap, capType, mesline
	evt_obj.bonus_list.set_overall_cap(1, 0, 0, 1004)
	evt_obj.bonus_list.set_overall_cap(2, 0, 0, 1004)
	return 0

def DTooltip(attachee, args, evt_obj):
	evt_obj.append('Dizzy')
	return 0

def DETooltip(attachee, args, evt_obj):
	key = tpdp.hash('DIZZY')
	evt_obj.append(key, -2, '')
	return 0

dizzy = PythonModifier('Dizzy', 2)
dizzy.AddHook(ET_OnGetTooltip, EK_NONE, DTooltip, ())
dizzy.AddHook(ET_OnGetEffectTooltip, EK_NONE, DETooltip, ())
dizzy.AddHook(ET_OnGetMoveSpeed, EK_NONE, Dizzy, ())
dizzy.AddHook(ET_OnD20Signal, EK_S_EndTurn, Remove, ())
dizzy.AddHook(ET_OnD20Signal, EK_S_Combat_End, Remove, ())
dizzy.AddHook(ET_OnD20Signal, EK_S_Killed, Remove, ())
