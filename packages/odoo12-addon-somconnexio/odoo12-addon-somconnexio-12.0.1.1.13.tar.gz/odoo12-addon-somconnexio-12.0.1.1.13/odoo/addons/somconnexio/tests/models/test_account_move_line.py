from ..sc_test_case import SCTestCase


class AccountMoveLineTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

    def test_display_name_account_move_line(self):
        move = self.env['account.move'].create({
            'journal_id': self.ref('somconnexio.caixa_guissona_journal'),
            'amount': 100.0,
            'name': 'BGUI/2021/001',
            'ref': 'Ordres de cobrament PAY0024'
        })
        move_line = self.env['account.move.line'].create({
            'move_id': move.id,
            'name': 'Línia L09692 de banc de cobrament',
            'account_id': self.env.ref('l10n_es.1_account_common_4300').id
        })
        self.assertEquals(
            move_line.name_get(),
            [(move_line.id, '{}({})'.format(move.name, move_line.name))]
        )
