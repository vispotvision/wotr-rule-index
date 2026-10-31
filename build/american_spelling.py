"""British to American spelling (Isaac is American, 2026-10-30). Used by verify.py (a FAIL) and for bulk conversion."""
import re

# British -> American. Keys are regex stems with optional suffix groups.
PAIRS=[
 (r'colour(s|ed|ing|ful|less|ist|ists|ation|ings)?',r'color\1'),
 (r'favour(s|ed|ing|ite|ites|able|ably)?',r'favor\1'),
 (r'honour(s|ed|ing|able|ably)?',r'honor\1'),
 (r'humour(s|ed|ing|ous|ist|ists)?',r'humor\1'),
 (r'neighbour(s|ed|ing|hood|hoods|ly)?',r'neighbor\1'),
 (r'labour(s|ed|er|ers|ing)?',r'labor\1'),
 (r'flavour(s|ed|ing|ful|some)?',r'flavor\1'),
 (r'harbour(s|ed|ing)?',r'harbor\1'),
 (r'rumour(s|ed)?',r'rumor\1'),
 (r'vapour(s)?',r'vapor\1'),
 (r'odour(s)?',r'odor\1'),
 (r'behaviour(s|al)?',r'behavior\1'),
 (r'savour(s|ed|ing|y)?',r'savor\1'),
 (r'armour(s|ed|er|ers|y)?',r'armor\1'),
 (r'endeavour(s|ed|ing)?',r'endeavor\1'),
 (r'parlour(s)?',r'parlor\1'),
 (r'rigour(s|ous)?',r'rigor\1'),
 (r'vigour(ous|ously)?',r'vigor\1'),
 (r'valour',r'valor'),
 (r'clamour(s|ed|ing|ous)?',r'clamor\1'),
 (r'splendour(s)?',r'splendor\1'),
 (r'candour',r'candor'),
 (r'fervour',r'fervor'),
 (r'saviour(s)?',r'savior\1'),
 (r'arbour(s)?',r'arbor\1'),
 (r'ardour',r'ardor'),
 (r'tumour(s)?',r'tumor\1'),
 (r'demeanour',r'demeanor'),
 (r'grey(s|ed|ing|er|est|ish|ness)?',r'gray\1'),
 (r'defence(s|less)?',r'defense\1'),
 (r'offence(s)?',r'offense\1'),
 (r'pretence(s)?',r'pretense\1'),
 (r'licence(s|d)?',r'license\1'),
 (r'practise(s|d)?',r'practice\1'),
 (r'centre(s|d|piece|pieces)?',r'center\1'),
 (r'metre(s)?',r'meter\1'),
 (r'litre(s)?',r'liter\1'),
 (r'fibre(s)?',r'fiber\1'),
 (r'theatre(s)?',r'theater\1'),
 (r'sabre(s)?',r'saber\1'),
 (r'mould(s|ed|ing|y)?',r'mold\1'),
 (r'moustache(s|d)?',r'mustache\1'),
 (r'plough(s|ed|ing|man|men|share)?',r'plow\1'),
 (r'towards',r'toward'),
 (r'whilst',r'while'),
 (r'amongst',r'among'),
 (r'artefact(s)?',r'artifact\1'),
 (r'sulphur(ous|ic|ates?)?',r'sulfur\1'),
 (r'manoeuvr(e|es|ed|ing)',r'maneuver\1'),
 (r'judgement(s)?',r'judgment\1'),
 (r'ageing',r'aging'),
 (r'catalogue(s|d)?',r'catalog\1'),
 (r'travell(ed|er|ers|ing)',r'travel\1'),
 (r'levell(ed|ing)',r'level\1'),
 (r'fuell(ed|ing)',r'fuel\1'),
 (r'labell(ed|ing)',r'label\1'),
 (r'modell(ed|ing)',r'model\1'),
 (r'signall(ed|ing)',r'signal\1'),
 (r'marvellous(ly)?',r'marvelous\1'),
 (r'jewellery',r'jewelry'),
 (r'counsellor(s)?',r'counselor\1'),
 (r'woollen',r'woolen'),
 (r'burnt',r'burned'),
 (r'learnt',r'learned'),
 (r'spilt',r'spilled'),
 (r'dreamt',r'dreamed'),
 (r'leant',r'leaned'),
 (r'smelt',r'smelled'),
 (r'kerb(s)?',r'curb\1'),
 (r'tyre(s)?',r'tire\1'),
 (r'cheque(s)?',r'check\1'),
 (r'aluminium',r'aluminum'),
 (r'cosy',r'cozy'),
 (r'pyjamas',r'pajamas'),
 (r'plait(s|ed|ing)?',r'braid\1'),
]
COMPILED=[(re.compile(r'\b'+a+r'\b',re.I),b) for a,b in PAIRS]
def conv(m,repl):
    src=m.group(0)
    out=m.expand(repl.replace('\\1','\\1')) if '\\1' in repl else repl
    # m.expand with unmatched group gives ''; ok in py3.5+ for optional groups
    if src.isupper() and len(src)>1: return out.upper()
    if src[0].isupper(): return out[0].upper()+out[1:]
    return out
def convert(text):
    n=0
    for rx,rep in COMPILED:
        def f(m):
            nonlocal n
            n+=1
            return conv(m,rep)
        text=rx.sub(f,text)
    return text,n


def british(text):
    """Distinct British spellings found in text, as (found, american) pairs."""
    seen = {}
    for rx, rep in COMPILED:
        for m in rx.finditer(text):
            seen.setdefault(m.group(0).lower(), conv(m, rep).lower())
    return sorted(seen.items())
