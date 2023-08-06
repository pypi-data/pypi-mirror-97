# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import suite as test_suite
from trytond.pool import Pool
from trytond.tests.tools import activate_modules


class ElectronicMailTestCase(ModuleTestCase):
    'Test Electronic Mail module'
    module = 'electronic_mail'

    @classmethod
    def setUpClass(cls):
        super(ElectronicMailTestCase, cls).setUpClass()
        activate_modules(['party', 'electronic_mail'])

    @with_transaction()
    def test_template(self):
        'Test electronic mail template'
        pool = Pool()
        Party = pool.get('party.party')
        Model = pool.get('ir.model')
        Template = pool.get('electronic.mail.template')
        Lang = pool.get('ir.lang')

        lang, = Lang.search([('code', '=', 'ca')])
        mparty, = Model.search([('model', '=', 'party.party')])

        template, = Template.create([{
                'name': 'Test Party',
                'model': mparty,
                'from_': 'from@domain.com',
                'sender': 'sender@domain.com',
                'to': "${record.get_mechanism('email') or ''}",
                'cc': 'suport@domain.com',
                'bcc': 'bbc@domain.com',
                'subject': 'Email ${record.name}',
                'language': "${record.lang and record.lang.code or 'en'}",
                'plain': 'Hello ${record.name}',
                'html': 'Hello <strong>${record.name}</strong>',
                }])
        self.assertEqual(template.wizard.name, 'Test Party')

        party, = Party.create([{
                'name': 'Iona',
                'lang': lang.id,
                'contact_mechanisms': [('create', [{
                                'type': 'email',
                                'value': 'iona@domain.com',
                                }])]
                }])
        self.assertEqual(party.get_mechanism('email'), 'iona@domain.com')
        self.assertEqual(template.eval(template.language, party), 'ca')

        data, = template.pre_render([party])
        self.assertEqual(data['to'], 'iona@domain.com')
        self.assertEqual(data['plain'], 'Hello Iona')
        self.assertEqual(data['subject'], 'Email Iona')

        data['subject'] = 'A coffe break, ${record.name}'
        val, = Template.render(template, [party], data)
        self.assertEqual(val['subject'], 'A coffe break, Iona')


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ElectronicMailTestCase))
    return suite
