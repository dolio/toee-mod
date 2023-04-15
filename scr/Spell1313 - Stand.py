from toee import *

debug = True

def Debug(*args):
	if debug:
		print "Stand:",
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
	do_event = False
	for target_item in spell.target_list:
		target = target_item.obj

		save = False
		if not target.is_friendly(spell.caster):
			save = target.saving_throw_spell(
					spell.dc, D20_Save_Will, D20STD_F_NONE, spell.caster, spell.id)

		if save or not target.d20_query(Q_Prone):
			game.particles('Fizzle', target)
			remove.append(target)
			continue

		do_event = True
		game.sound(32242)
		target.fade_to(0, 10, 50)
		target.d20_send_signal(S_Standing_Up)
		target.turn_towards(target)

	if do_event: game.timeevent_add(FadeUp, (spell,), 1000, 1)

	spell.target_list.remove_list(remove)
	spell.spell_end(spell.id)

def OnEndSpellCast(spell):
	Debug("OnEndSpellCast")
	Debug("spell.id = ", spell.id)

def FadeUp(spell):
	remove = []
	for target_item in spell.target_list:
		target = target_item.obj
		remove.append(target)

		vis = 255

		game.sound(32241)
		if target.d20_query(Q_Critter_Is_Invisible): vis = 128
		target.fade_to(vis, 15, 5)

	spell.target_list.remove_list(remove)
	spell.spell_end(spell.id)
