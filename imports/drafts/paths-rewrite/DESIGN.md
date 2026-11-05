# Paths, layers and Wellsprings: the design and the wiki brief

The law is R85-14 to R85-17 (`rules/doc-directions-2026-11-05-paths.yaml`) and NATALIE.md, THE MAGIC FRAME. This file holds what the wiki rewrite needs on top of that.

## The three Paths

| Path | Plane | Layer | Who | Force | Costs |
|---|---|---|---|---|---|
| Body | Physical World | Aether Shell | hitters | +5 to +20 percent to Strike, Durability, Lifting | Range and Aura Pressure; must close |
| Spirit | Soul Plane | Essence Core | throwers | +5 to +25 percent through projection, none by hand | Durability; survives by being right |
| Fate | Plane of Fate | Attraction Layer | talkers and stayers | smallest direct force; largest Range, Aura Pressure, Domain authority | raw output; strongest at home; Fate Arts rare and very hard |

Fate takes both old crowds. A midwife of forty years and Hyeon Do-sun are both on it, at very different depths: the wide low end is bonds, oaths and presence, and the far end is moving the odds.

## Balance at a glance

| | One Path | Two Paths | Three Paths |
|---|---|---|---|
| Time to master | base | about 2.5 times, for the pair | about 6 times, past a mortal span |
| Gates | at the Stage written | the Path behind opens a Stage late until mastered | two Stages late; high Grades shut |
| Force modifier | full | three-quarters each, for life | half each |
| Seat | clean | rough | rough, with high Dead Set risk |
| The read | an opponent knows what you cannot do | the read fails at first | nobody bothers to read you, which is occasionally a mistake |

A mastered single at equal Stage beats a dual on the single's own ground. A dual beats a single who misreads them, and covers their own counter. Studying gives knowledge and small uses, and no gates.

## What Typology did, and where it goes

| Job | Now |
|---|---|
| Character of a blow | Wellspring and Path |
| Wellspring compatibility | how the qualifier sits with the Path |
| Primary Trait formation | origin, first imprint, lived Path |
| Aether Class trajectory | how the person has lived (R84-10) |
| Lens doubling | the lens at its home Path |
| Catalyst wording in Part Eighteen | moves to the Family pages as the Family's idea, which is not a personal trait |

## Three readings of a Wellspring (samples for every entry)

**Pyreveil (Wild).** Body: the heat lives in the tissue, blows burn on contact and the body stops minding fire. Spirit: thrown fire that burns what is false in a thing before what is solid. Fate: a claim that burns its way through, oaths and rivalries that consume what stands in them, and ground that catches around the person.

**Absolution (Spirit).** Body: old injuries stop costing what they cost; no heat, no glow, just a body that has stopped carrying its history. Spirit, at home: lets the old poison out of a soul, one's own or a willing other's. Fate: a debt or grudge held on the Attraction Layer can be let go, and the thing it was pulling on stops pulling.

**Benediction (Fate).** Body: a bond freely given lends the one blessed a real measure of steadiness, felt in the hands and the footing. Spirit: a working carries the weight of the bond behind it. Fate, at home: a bond the world weighs as a real thing, and an oath under it bears load.

## The wiki rewrite, not started

1. The Four Paths page becomes The Three Paths. Keep the Door Wager with Robin and Hyeon both on Fate, keep recognition, gates, seats and drift, and add one, two and three Paths.
2. The Soul Crystal pages take the layer table and the definition of Essence.
3. The hub: drop Typology, add the qualifiers, a Fate-type encounter (luck goes strange, oaths bite, strangers keep meeting), and Medium as at home on all three.
4. All sixty entries: a Kind line by R85-17 and three lines, On the Body, On the Spirit, On Fate. Rewrite any Wellspring that does not survive this.
5. Fracture pages VII (Part Eighteen) and any gate table: Attraction reads as Fate, Typology removed.
6. The 59 pages naming Typology and the 107 naming a Path, 14 cards included: card Typology lines go, Path lines convert by R85-16, and rule quotes stay intact.
7. Rust: `rust/src/workshop.rs:277-279` lists four Paths and offers Typology; `rust/src/analysis.rs:910` names the layers.
8. Skills and pipelines that name Typology or four Paths.

Rule-quoted passages must survive word for word, or `validate` fails. Run it after every page group.

## Open

- Whether long-lived beings can truly reach three Paths; R85-16 leaves it to the card.
- The Celestial line, "no Choir carries Fate Path at any weight", now also bars what used to be Attraction.
- Cards at three shares convert with 30 percent as the Walked line, so none becomes a true three-Path by accident.
