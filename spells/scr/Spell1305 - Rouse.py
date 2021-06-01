from toee import *

debug = True

def Debug(*args):
	if debug:
		print "Rouse:",
		for arg in args:
			print arg,
		print ""

def OnBeginSpellCast(spell):
	Debug("OnBeginSpellCast")
	Debug("spell.target_list = ", spell.target_list)
	Debug("spell.caster = ", spell.caster, " caster.level = ", spell.caster_level)
	Debug("spell.id = ", spell.id)

	game.particles("sp-enchantment-conjure", spell.caster)

def OnSpellEffect(spell):
	Debug("OnSpellEffect")

	remove = []
	for target in spell.target_list:
		# awaken
		target.obj.d20_send_signal(S_AID_ANOTHER_WAKE_UP)
		remove.append(target)

	spell.remove_list(remove)
	spell.spell_end()

def OnEndSpellCast(spell):
	Debug("OnEndSpellCast")
	Debug("spell.id = ", spell.id)
