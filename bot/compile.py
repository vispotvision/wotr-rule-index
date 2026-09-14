"""Turn Discord messages into a scene: the prose, and the speaker-tagged cast script.

A message from a Tupperbox proxy (a webhook) carries the character's name as its author;
a message from a person carries their display name. Out-of-character lines start with
"((" or "//" and are dropped, as are bot messages, slash-command echoes and empty posts.
The scene markdown is plain paragraphs (the archive wants prose, not a chat log); the
cast script is the same text with [Name] tags at every change of voice, which is exactly
what scenes/cast/<scene>.cast.md holds, so the narrator can voice it.
"""
import re

OOC = re.compile(r"^\s*(\(\(|//)")


def usable(m) -> bool:
    if not m.content or OOC.match(m.content):
        return False
    if m.author.bot and not m.webhook_id:  # our own or another bot's messages; a Tupperbox proxy is a webhook
        return False
    if m.type.name not in ("default", "reply"):
        return False
    return True


def speaker_of(m) -> str:
    return m.author.display_name if hasattr(m.author, "display_name") else m.author.name


def compile_scene(title: str, messages: list) -> tuple[str, str, list[str]]:
    """(scene markdown, cast script, speakers) from messages in chronological order."""
    paras, tagged, speakers = [], [], []
    last = None
    for m in messages:
        if not usable(m):
            continue
        who = speaker_of(m)
        text = re.sub(r"[ \t]+", " ", m.content.strip())
        text = re.sub(r"\n{3,}", "\n\n", text)
        for para in [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]:
            paras.append(para)
            tagged.append((f"[{who}] " if who != last else "") + para)
            last = who
        if who not in speakers:
            speakers.append(who)
    md = f"# {title}\n\n" + "\n\n".join(paras) + "\n"
    script = f"# {title}\n\n" + "\n\n".join(tagged) + "\n"
    return md, script, speakers
