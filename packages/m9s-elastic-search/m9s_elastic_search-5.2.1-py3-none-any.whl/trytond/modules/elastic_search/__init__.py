# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import index
from . import ir
from . import configuration

__all__ = ['register']


def register():
    Pool.register(
        configuration.Configuration,
        index.IndexBacklog,
        index.DocumentType,
        ir.Cron,
        module='elastic_search', type_='model')
