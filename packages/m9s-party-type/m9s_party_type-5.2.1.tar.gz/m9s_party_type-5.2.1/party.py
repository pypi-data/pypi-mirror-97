# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Equal, Eval, Not, Or, Bool
from trytond.transaction import Transaction
from trytond.pool import PoolMeta, Pool

STATES_PERSON = {
    "readonly": Or(
        Not(Bool(Eval('active'))),
        Not(Equal(Eval('party_type'), 'person'))),
    "invisible": Not(Equal(Eval('party_type'), 'person')),
}
STATES_PERSON_DEPENDS = ['active', 'party_type']


class Party(metaclass=PoolMeta):
    __name__ = "party.party"

    party_type = fields.Selection(
        [
            ("organization", "Organization"),
            ("person", "Person"),
        ], "Type", states={
            'readonly': Not(Bool(Eval('active'))),
        }, depends=['active'])
    first_name = fields.Char(
        "First Name", states=STATES_PERSON, depends=STATES_PERSON_DEPENDS)

    @staticmethod
    def default_party_type():
        return Transaction().context.get('party_type', 'person')

    def get_rec_name(self, name):
        res = super(Party, self).get_rec_name(name)
        if self.party_type == 'person':
            full_name = ", ".join(
                x for x in [self.name, self.first_name] if x)
            name_parts = res.split(' ')
            # We assume that the first element is the party name and replace it
            # with full_name, but this could of course be wrong depending on
            # other modules in the super chain.
            # Remove as many elements as full_name contains from name_parts and
            # then insert full_name at the beginning
            elems = len(full_name.split(' ')) - 1
            name_parts = name_parts[elems:]
            name_parts.insert(0, full_name)
            res = ' '.join(name_parts)
        return res

    @classmethod
    def search_rec_name(cls, name, clause):
        parties = cls.search(['OR',
                ('name',) + tuple(clause[1:]),
                ('first_name',) + tuple(clause[1:]),
                ])
        if parties:
            return [('id', 'in', [x.id for x in parties])]
        return super(Party, cls).search_rec_name(name, clause)

    def get_full_name(self, name):
        return " ".join(
            x for x in [self.first_name, self.name] if x)

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        args = []
        for parties, values in zip(actions, actions):
            if ('party_type' in values and
                    values['party_type'] == 'organization'):
                        values['first_name'] = None
            args.extend((parties, values))
        super(Party, cls).write(*args)


class PartyErase(metaclass=PoolMeta):
    __name__ = 'party.erase'

    def to_erase(self, party_id):
        pool = Pool()
        Party = pool.get('party.party')

        to_erase = super(PartyErase, self).to_erase(party_id)
        to_erase += [
            (Party, [('id', '=', party_id)], True,
                ['first_name', 'party_type'],
                [None, None, None]),
            ]
        return to_erase
