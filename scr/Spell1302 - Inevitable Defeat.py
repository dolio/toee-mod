from toee import *
import tpdp

debug = True

def Debug(*args):
	if debug:
		print "Inevitable Defeat:",
		for arg in args:
			print arg,
		print ""

def OnBeginSpellCast(spell):
	Debug("OnBeginSpellCast")
	Debug("spell.target_list = ", spell.target_list)
	Debug("spell.id = ", spell.id)

	game.particles("sp-enchantment-conjure", spell.caster)

def OnSpellEffect(spell):
	Debug("OnSpellEffect")

	target = spell.target_list[0]

	spell.duration = spell.caster_level

	target.partsys_id = game.particles('sp-Touch of Fatigue', target.obj)
	target.obj.condition_add_with_args(
			'sp-Inevitable Defeat', spell.id, -1 * spell.duration, 1, spell.dc, 0)

def OnBeginRound(spell):
	Debug("OnBeginRound")
	Debug("spell.id = ", spell.id)
	Debug("spell.target_list = ", spell.target_list)

def OnEndSpellCast(spell):
	Debug("OnEndSpellCast")
	Debug("spell.id = ", spell.id)
