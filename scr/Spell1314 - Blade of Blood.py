from toee import *

def OnBeginSpellCast(spell):
	game.particles('sp-necromancy-conjure', spell.caster)

def OnSpellEffect(spell):
	spell.duration = spell.caster_level
	caster = spell.caster

	arg = spell.spell_get_menu_arg(RADIAL_MENU_PARAM_MIN_SETTING)

	boost = 0
	fizzle = False
	if arg == 2:
		boost = 1
		hp = caster.stat_level_get(stat_hp_current)
		if hp < 5:
			fizzle = True
		else:
			dmg = caster.obj_get_int(obj_f_hp_damage)
			caster.set_hp_damage(dmg + 5)
			caster.float_text_line("5 HP", tf_red)

	remove = []
	for item in spell.target_list:
		target = item.obj

		if fizzle or target.type != obj_t_weapon:
			remove.append(target)
			game.sound(7461, 1)
			game.particles('Fizzle', target)
			target.float_mesfile_line('mes\\spell.mes', 30003)
			continue

		game.sound(32262)
		target.d20_status_init()
		target.condition_add_with_args(
				'sp-Blade of Blood', spell.id, spell.duration, boost, 0)

	spell.target_list.remove_list(remove)
	spell.spell_end(spell.id)

def OnEndSpellCast(spell):
	print "End Blade of Blood"
