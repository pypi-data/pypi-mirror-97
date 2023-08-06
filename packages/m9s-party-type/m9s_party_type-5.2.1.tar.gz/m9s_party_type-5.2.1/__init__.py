# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.
from trytond.pool import Pool
from . import party

__all__ = ['register']


def register():
    Pool.register(
        party.Party,
        module='party_type', type_='model')
    Pool.register(
        party.PartyErase,
        module='party_type', type_='wizard')
