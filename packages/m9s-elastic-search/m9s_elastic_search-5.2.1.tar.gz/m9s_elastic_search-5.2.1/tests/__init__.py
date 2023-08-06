# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.elastic_search.tests.test_elastic_search import suite
except ImportError:
    from .test_elastic_search import suite

__all__ = ['suite']
