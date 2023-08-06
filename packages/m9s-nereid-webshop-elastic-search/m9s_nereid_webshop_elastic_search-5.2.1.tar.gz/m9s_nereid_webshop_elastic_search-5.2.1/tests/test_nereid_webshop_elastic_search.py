# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class NereidWebshopElasticSearchTestCase(ModuleTestCase):
    'Test Nereid Webshop Elastic Search module'
    module = 'nereid_webshop_elastic_search'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            NereidWebshopElasticSearchTestCase))
    return suite
