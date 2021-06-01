from toee import *
import tpdp

debug = True

def Debug(*args):
	if debug:
		print "Vertigo:",
		for arg in args:
			print arg,
		print ""

def OnBeginSpellCast(spell):
	Debug("OnBeginSpellCast")

	game.particles("sp-illusion-conjure", spell.caster)

def OnSpellEffect(spell):
	Debug("OnSpellEffect")

	caster = spell.caster
	duration = spell.caster_level

	remove = []
	for target_item in spell.target_list:
		target = target_item.obj
		saved = target.saving_throw_spell(
				spell.dc, D20_Save_Will, D20STD_F_NONE, caster, spell.id)

		if saved:
			remove.append(target)
			continue

		target.condition_add_with_args('sp-Vertigo', spell.id, duration, 0, 0)

	spell.target_list.remove_list(remove)
	spell.spell_end(spell.id)
