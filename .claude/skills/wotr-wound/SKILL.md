---
name: wotr-wound
description: "Real injury research for War of the Realms fights. Use this BEFORE writing any wound, hit, cut, shot, burn, fall or finisher in WOTR, and whenever Isaac asks what a blow would actually do, how long a man has, whether he can still fight, or what heals. Given weapon, angle, armour tier and the target's Vitality, it returns the anatomy struck, the ATLS haemorrhage class, the minute-by-minute functional timeline, what kills by morning, and what the Ledger records. Trigger even when the beat only implies injury (a fall, a fire, a crush, a ricochet)."
---

# wotr-wound

Fights in WOTR are won by what the body can still do. Never write a wound
from memory. This skill returns a wound brief the prose is then written from.

## Inputs (ask only for what the beat does not supply)

Weapon and its mass. Angle and target region. Armour tier at that region
(none, gambeson, mail, plate, proofed plate; worked or unworked). Target's
Stage and Vitality line via `fow_line`. Distance and whether the man was
moving into or away from the blow.

## Procedure

1. Read `references/injury-tables.md` for the matching weapon class.
2. Search once (WebSearch) for the real injury: the anatomy at that angle, the vessel
   or organ, the bone. Trauma literature, not fiction. Name the source.
3. Search once for the armour interaction at that tier (mail against thrust,
   plate against cut, gambeson against blunt). Pack Eleven: proof-marks are
   texture; a worked cuirass is stopped by the working, never the steel, and
   no sentence explains why a proofed round beats proofed plate (C-001 open).
4. Layer the WOTR modifiers: Vitality Grade shifts the timeline, never the
   anatomy; ATLS class sits on top of Vitality (R14); Resilience decides
   Crystal strain if a working was involved.
5. Write the brief.

## The wound brief (what you hand back, under 250 words)

- **Struck**: anatomy, vessel, bone, organ, in that order.
- **Class**: ATLS haemorrhage class I to IV and the blood volume it implies.
- **Timeline**: at ten seconds, one minute, ten minutes, one hour, morning.
  What he can do at each: stand, swing, walk, speak, hold a working.
- **Kills by**: the mechanism (exsanguination, tension pneumothorax, sepsis at
  day three) and the intervention that changes it, if any, at the setting's
  medicine ceiling.
- **Ledger line**: what persists next scene and what heals by when.
- **On the page**: the three or four physical facts the prose must show,
  from the POV's competence. A soldier sees blood; a surgeon sees the class.

## Standing rules

Gore in full. Never soften. The POV's own body on the page as much as the
opponent's. Kharven medicine speaks in bowls: "the third bowl" is Class III
(pending entry). Nothing invented; an estimate is labelled.
