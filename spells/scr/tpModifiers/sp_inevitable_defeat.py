from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
from spell_utils import *
print "Registering sp_inevitable_defeat"

debug = True

def Debug(charge, *args):
	if debug:
		if charge == 0:
			print "sp-Inevitable Defeat: ",
		else:
			print "Inevitable Defeat: ",

		for arg in args:
			print arg," ",
		print ""

# sp-Inevitable Defeat
#  touch attack charge
#  args: (0-4)
#  0 - spell_id
#  1 - duration
#  2 - charges
#  3 - dc
#  4 - spare

def DamageEffect(caster, target, spell_id):
	Debug(1, "DamageEffect", caster, target)
	dice = dice_new('3d6')

	target.spell_damage(
			caster, D20DT_SUBDUAL, dice, D20DAP_UNSPECIFIED,
			D20A_CAST_SPELL, spell_id)

# gets called on a successful touch attack
def OnTouch(attachee, args, evt_obj):
	resisted = touchPre(args, evt_obj)

	if not resisted:
		action = evt_obj.get_d20_action()
		caster = action.performer
		target = action.target

		spell_id = args.get_arg(0)
		duration = -1 * args.get_arg(1)
		dc = args.get_arg(3)

		DamageEffect(caster, target, spell_id)

		target.condition_add_with_args(
				"Inevitable Defeat", spell_id, duration, dc, 0)

charge = TouchModifier("sp-Inevitable Defeat", 2)
charge.AddTouchHook(OnTouch)

# returns whether the save was successful
def WillSave(caster, target, dc, spell_id):
	Debug(False, "WillSave")
	if target.saving_throw_spell(dc,D20_Save_Will,D20STD_F_NONE,caster,spell_id):
		target.float_mesfile_line('mes\\spell.mes', 30001)
		return True
	else:
		target.float_mesfile_line('mes\\spell.mes', 30002)
		return False

# returns whether the effect should persist
def WillSaveAndDamage(target, caster, spell_id, dc, duration, ticks):
	Debug(False, "WillSaveAndDamage")
	while duration > 0 and ticks > 0:
		duration = duration - 1
		ticks = ticks - 1

		if WillSave(caster, target, dc, spell_id):
			return True

		DamageEffect(caster, target, spell_id)

	return duration <= 0

def CondBeginRound(target, args, evt_obj):
	Debug(False, "CondBeginRound")
	spell_id = args.get_arg(0)
	duration = args.get_arg(1)
	dc = args.get_arg(2)
	ticks = evt_obj.data1

	packet = tpdp.SpellPacket(spell_id)
	caster = packet.caster

	args.set_arg(1, duration-ticks)

	if WillSaveAndDamage(target, caster, spell_id, dc, duration, ticks):
		args.condition_remove()
		packet.remove_target(target)
		if packet.target_count <= 0:
			args.remove_spell()

	return 0

# def CondOnRemove(attachee, args, evt_obj):
#		spellPacket = tpdp.SpellPacket(args.get_arg(0))
#		spellPacket.remove_target(attachee)
#		return 0

def CondSpellActive(attachee, args, evt_obj):
	Debug(False, "CondHasSpellActive")
	if evt_obj.data1 == 1200:
		evt_obj.return_val = 1
	return 0

def CondEnd(attachee, args, evt_obj):
	Debug(False, "CondEnd")
	args.condition_remove()
	args.remove_spell_with_key(EK_S_Concentration_Broken)
	return 0

# Inevitable Defeat
#  ongoing effect
#  args: (0-3)
#  0 - spell_id
#  1 - effect duration
#  2 - effect DC
#  3 - spare

effect = PythonModifier("Inevitable Defeat", 4)
effect.AddHook(ET_OnBeginRound, EK_NONE, CondBeginRound, ())
effect.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, CondSpellActive, ())
effect.AddHook(ET_OnGetTooltip, EK_NONE, spellTooltip, ())
effect.AddHook(ET_OnGetEffectTooltip, EK_NONE, spellEffectTooltip, ())
effect.AddHook(ET_OnD20Signal, EK_S_Killed, CondEnd, ())
# effect.AddHook(ET_OnConditionRemove, EK_NONE, CondEnd, ())
effect.AddSpellDispelCheckStandard()
effect.AddSpellTeleportPrepareStandard()
effect.AddSpellTeleportReconnectStandard()
