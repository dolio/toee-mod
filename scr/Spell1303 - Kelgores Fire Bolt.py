from toee import *
import tpdp

debug = False

def Debug(*args):
	if debug:
		print "Kelgore's Fire Bolt:",
		for arg in args:
			print arg,
		print ""

def OnBeginSpellCast(spell):
	Debug("OnBeginSpellCast")
	Debug("spell.target_list =", spell.target_list)
	Debug("spell.caster =", spell.caster, "caster.level =", spell.caster_level)

	game.particles("sp-Fireball-conjure", spell.caster)

def OnBeginProjectile(spell, projectile, index_of_target):
	Debug("OnBeginProjectile")

	part = game.particles('sp-Fireball-proj', projectile)
	projectile.obj_set_int(obj_f_projectile_part_sys_id, part)

def OnEndProjectile(spell, projectile, index_of_target):
	Debug("OnEndProjectile")

	target_item = spell.target_list[index_of_target]
	target = target_item.obj
	caster = spell.caster
	packet = tpdp.SpellPacket(spell.id)

	dice = dice_new("1d6")

	if not packet.check_spell_resistance_force(target):
		dice.num = min(5, spell.caster_level)

	target.spell_damage(
			caster, D20DT_FIRE, dice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id)

	spell.num_of_projectiles -= 1
	if spell.num_of_projectiles == 0:
		spell.spell_end(spell.id, 1)
