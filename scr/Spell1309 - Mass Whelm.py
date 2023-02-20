from toee import *

def OnBeginSpellCast(spell):
	game.particles('sp-illusion-conjure', spell.caster)

def OnSpellEffect(spell):
	caster = spell.caster
	dc = spell.dc

	remove = []
	for target_item in spell.target_list:
		target = target_item.obj
		remove.append(target)

		save = target.saving_throw_spell(
				dc, D20_Save_Will, D20STD_F_NONE, caster, spell.id)

		if save:
			target.float_mesfile_line('mes\\spell.mes', 30001)
			continue
		else:
			target_item.partsys_id = game.particles('sp-Whelm', target)
			target.float_mesfile_line('mes\\spell.mes', 30002)

		dice = dice_new('1d6')
		dice.num = min(10, spell.caster_level)

		target.spell_damage(
				caster, D20DT_SUBDUAL, dice, D20DAP_UNSPECIFIED,
				D20A_CAST_SPELL, spell.id)

	spell.target_list.remove_list(remove)
	spell.spell_end(spell.id)
