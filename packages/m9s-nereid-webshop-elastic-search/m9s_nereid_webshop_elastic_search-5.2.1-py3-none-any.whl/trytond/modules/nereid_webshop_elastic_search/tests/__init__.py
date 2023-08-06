# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.nereid_webshop_elastic_search.tests.test_nereid_webshop_elastic_search import suite
except ImportError:
    from .test_nereid_webshop_elastic_search import suite

__all__ = ['suite']
