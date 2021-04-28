This tweak is an attempt to fix the problems with the core Mystic
Theurge class.  The core idea is that the prestige class/concept
itself is not the problem, but rather the implementation of its
trade-offs. In my mind, the idea behind the Mystic Theurge is thus:

  - A hybrid arcane/divine caster should have to trade some of its top
    end power for additional versatility
  - To this end, the Theurge should be blocked from achieving the
    highest level spells
  - Additional factors like taking the weaker BAB/Saves/etc. from the
    two classes may act as additional mitigating factors

This concept is likely never a recipe for an optimal character at the
highest levels (which people inevitably seem to focus on, but seems
misguided to me). The bigger problem is that the actual execution is a
recipe for being _bad_ (even at the character concept) at the levels
that are normally good to play.

  1. You start as a normal level 1 character, who can die randomly
  2. As normal characters ramp up, you divide your levels so that you
     never really become effective, and are only half a character by
     level 6
  3. From that point you may make up ground because both classes
     progress at once, but you probably won't catch up to being decent
     until late in the prestige class, at which point you're level
     12+, which is toward the end of the sweet spot
  4. Having two casting stats likely means having to split points
     between them, and getting fewer bonus spells. So despite having
     two spell lists, the numeric advantage on spell slots likely
     won't pan out until late.
  5. You end up at 15/15 if you evenly split or 17/13 if you bias
     fully toward one class. The latter barely gets you 9th/7th level
     spells in the prepared cases. The former barely gets 8th in both
     classes.

The clear problem is front-loading the trade-off. If we look at AD&D
multiclassing, we see instead:

  1. You start as level 1 in _both_ classes (and even take the better
     stats from each, aside from casting arcane spells in armor).
  2. Low level growth is exponential, so you are only about 1 level
     behind a pure class until level 7 or so.
  3. Beyond this growth linearizes so that you start to fall behind
     pure classes, gaining only 1/2 their levels in each class.
  4. Experience is a bit weird in 2nd edition, so when a cleric would
     be 20, you're 14/13, which just got 7th level priest spells (the
     highest). A mage would be 17 and only have 8th level spells,
     while you have 6th. Mage 18, which gets 9th level spells, would
     put you at 14/14 to have 7th level spells. Compared to Mage 20
     you'd be 16/15, and almost have 8th level spells.

So you are less behind at low levels when being 1/2 level would be
devastating, and the trade-off grows once it can be afforded. Mystic
Theurge has this backwards.

To that end, my solution is to just allow 'early' entry to the prestige
class. It can be taken at 1 Arcane/1 Divine without any tricks.
However, the number of levels of the prestige class that may be
selected are capped based on the following table:

     A/B | MT
     1/1 | 4
     1/2 | 7
     2/2 | 9
     2/3 | 10
     3/3 | 11
     4/4 | 12

The maximum theurge level is limited by the lower numbers, so having
base class allocation of 1/4 only allows 7 theurge levels, just like
1/2.

I'm sure this approach is more powerful than intended if combined with
other prestige classes to continue the dual progression instead of
taking more base class levels, but it seems simple enough to just
disallow/not use such combinations. That way the pieces can just be
good enough for their intended use, rather than designed around ruling
out character optimization tricks.

Since the only difference between the above and the original prestige
class is the prerequisites for taking each level, and (potentially)
the total number of levels, it's easy to just swap out the logic that
determines that for the existing class. Hence that is the only content
in this subdirectory. It can go in the overrides directory.
