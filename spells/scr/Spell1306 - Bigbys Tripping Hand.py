from toee import *
import tpdp
import d20class

debug = True

def Debug(*args):
	if debug:
		print "Bigby's Tripping Hand:",
		for arg in args:
			print arg,
		print ""

def OnBeginSpellCast(spell):
	Debug("OnBeginSpellCast")

	game.particles("sp-evocation-conjure", spell.caster)

def OnSpellEffect(spell):
	caster = spell.caster
	spell_stat = d20class.get_spell_stat(spell.caster_class)
	spell_mod = caster.stat_level_get(stat_str_mod + spell_stat)

	monster_proto_id = 14629

	remove = []
	for target_item in spell.target_list:
		target = target_item.obj
		remove.append(target)

		game.particles("sp-Bigby's Tripping Hand", target)

		if target.d20_query(Q_Prone): continue

		saved = target.saving_throw_spell(
				spell.dc, D20_Save_Reflex, D20STD_F_NONE, caster, spell.id)

		if saved: continue

		monster = game.obj_create(monster_proto_id, target.location)
		monster.stat_base_set(stat_strength, 14)
		monster.obj_set_int(obj_f_description,15500)
		monster.obj_set_int(obj_f_critter_description_unknown, 15500)

		will = caster.stat_level_get(stat_save_willpower)
		monster.condition_add_with_args(
				"sp-Bigby's Tripping Hand", spell_stat, spell_mod,
				spell.caster_level, will, 0)

		atk = monster.perform_touch_attack(target, 1)
		if not (atk & D20CAF_HIT): continue
		if not monster.trip_check(target): continue

		target.fall_down()
		target.condition_add('Prone')
		target.float_mesfile_line('mes\\combat.mes', 104, 1) # Tripped!

		monster.destroy()

	spell.target_list.remove_list(remove)
	spell.spell_end(spell.id)

