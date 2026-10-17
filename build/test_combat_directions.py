"""Regression checks for Isaac's combat prose directions (R77-1 of October 8, R79-6 of October 17)."""
import unittest
from pathlib import Path

import verify
from common import load_rules, normalise


class CombatDirectionsTests(unittest.TestCase):
    def check(self, text, **kwargs):
        return verify.run(text, **kwargs)

    def jargon(self, result):
        return [w for w in result['warns'] if w.startswith('European fencing jargon:')]

    def readout(self, result):
        return [w for w in result['warns'] if 'no readouts inside a fight' in w]

    def test_recorded_jargon_and_existing_manual_terms_warn(self):
        for term in ('Vor', 'Nach', 'Indes', 'Zufechten', 'Krieg', 'Vom Tag',
                     'Ochs', 'Pflug', 'Alber', 'Zornhau', 'Winden', 'Absetzen',
                     'Durchwechseln', 'Krumphau', 'Zwerchhau', 'Schielhau',
                     'Scheitelhau', 'Mutieren', 'Duplieren'):
            with self.subTest(term=term):
                self.assertEqual(len(self.jargon(self.check('She uses ' + term + '.'))), 1)

    def test_jargon_warns_in_dialogue_and_without_combat_flag(self):
        self.assertTrue(self.jargon(self.check('"VOR," she says.')))

    def test_jargon_is_not_positive_blade_evidence(self):
        result = self.check('Zornhau.', combat=True)
        self.assertTrue(any(w.startswith('no blade body/action vocabulary') for w in result['warns']))
        self.assertTrue(any('combat density: 0 blade body/action terms' in w for w in result['info']))

    def test_plain_actions_are_blade_evidence(self):
        result = self.check('She shifts her weight onto her heel and holds the blade beside her shoulder.', combat=True)
        self.assertFalse(self.jargon(result))
        self.assertFalse(any(w.startswith('no blade body/action vocabulary') for w in result['warns']))

    def test_anatomy_check_accepts_plain_and_clinical_parts(self):
        self.assertTrue(any('check 23' in w for w in self.check('She lifts the blade.', combat=True)['warns']))
        for part in ('clavicle', 'collarbone', 'jaw', 'ribs', 'throat', 'gut', 'knee', 'wrist', 'skull'):
            with self.subTest(part=part):
                self.assertFalse(any('check 23' in w for w in self.check(f'Her blade opens his {part}.', combat=True)['warns']))

    def test_notes_do_not_trigger_jargon_or_supply_blade_evidence(self):
        result = self.check('She waits.\n\n## Author notes\nZornhau. Her blade is raised.', combat=True)
        self.assertFalse(self.jargon(result))
        self.assertTrue(any(w.startswith('no blade body/action vocabulary') for w in result['warns']))

    def test_eastern_terms_free_and_never_required(self):
        for school in ('japanese', 'chinese', 'korean'):
            with self.subTest(school=school):
                result = self.check('He steps in and breaks her jaw.', combat=True, school=school)
                self.assertFalse(any('school vocabulary' in w for w in result['warns']))
                self.assertTrue(any(f'0 {school} school terms' in w for w in result['info']))
        self.assertFalse(self.jargon(self.check('She makes a kesa-giri.', combat=True, school='japanese')))

    def test_roleplay_fights_show_full_mechanism(self):
        text = 'Her blade moves at twenty metres a second; "Forty EU gone," she says.\n\n## Author notes\n40 EU.'
        result = self.check(text, combat=True, turn=True)
        self.assertFalse(any('R77-2' in w for w in result['warns'] + result['info']))
        self.assertFalse(any('author notes' in w for w in result['warns']))

    def test_readout_warns_only_in_a_fight(self):
        text = '[Reserve 40 EU]\n\nHer blade shakes beside her wrist.'
        self.assertTrue(self.readout(self.check(text, combat=True)))
        self.assertTrue(self.readout(self.check(text, combat=True, turn=True)))
        calm = self.check(text, turn=True)
        self.assertFalse(self.readout(calm))
        self.assertTrue(any(w.startswith('readouts: 1') for w in calm['info']))

    def test_fight_figures_live_in_mouths(self):
        narrated = self.check('Her cut costs 40 EU.', combat=True)
        spoken = self.check('"That cut cost forty EU, 40 EU," she says.', combat=True)
        self.assertTrue(any(w.startswith('figure in fight narration:') for w in narrated['warns']))
        self.assertFalse(any(w.startswith('figure in fight narration:') for w in spoken['warns']))
        self.assertFalse(any(w.startswith('figure in fight narration:') for w in self.check('Her cut costs 40 EU.')['warns']))

    def test_fight_abstraction_only_under_combat(self):
        text = 'He closed measure and took the line.'
        self.assertTrue(any(w.startswith('fight abstraction') for w in self.check(text, combat=True)['warns']))
        self.assertFalse(any(w.startswith('fight abstraction') for w in self.check(text)['warns']))
        self.assertFalse(verify.BLADE_ACTION.search('measure tempo'))

    def test_indexed_quotes_are_existing_rulings_not_new_law(self):
        rulings = Path(__file__).resolve().parent.parent.joinpath('RULINGS.md').read_text()
        by_id = {r['id']: r for r in load_rules()}
        for rid in ('R77-1-EUROPEAN_FENCING_ACTIONS', 'R77-2-COMBAT_ROLEPLAY_TELLS'):
            with self.subTest(rule=rid):
                self.assertIn(normalise(by_id[rid]['verbatim']), normalise(rulings))
                self.assertEqual(by_id[rid]['supersedes'], [])
        self.assertIn('Eastern', by_id['R77-1-EUROPEAN_FENCING_ACTIONS']['notes'])
        self.assertIn("Claude's reading", by_id['R77-2-COMBAT_ROLEPLAY_TELLS']['notes'])
        for rid in ('R70-100-MARTIAL_VOCABULARY_NAMES_MOVES', 'R13-4-COMBAT_FLOOR',
                    'R70-76-MUCH_WORLD_MAGIC', 'R71-4-FAR_FROM_FLOOR'):
            self.assertIn('R77-', by_id[rid]['summary'])

    def test_fresh_mcp_verifier_and_gap_fill_use_actions(self):
        import mcp_server
        text = 'Vor. Her blade shakes beside her clavicle.\n\n## Author notes\n40 EU, mechanism and account.'
        report = mcp_server.verify_scene(text, combat=True, turn=True)
        self.assertIn('European fencing jargon:', report)
        self.assertNotIn('R77-2-COMBAT_ROLEPLAY_TELLS', report)
        gap = mcp_server.gap_fill('Her blade strikes because she shifts her weight.')
        self.assertIn('blade body/action terms', gap)
        self.assertNotIn('HEMA terms', gap)


if __name__ == '__main__':
    unittest.main()
