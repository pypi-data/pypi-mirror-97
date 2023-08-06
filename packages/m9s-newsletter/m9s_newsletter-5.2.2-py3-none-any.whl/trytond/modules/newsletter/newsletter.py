# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields, Unique
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from trytond.i18n import gettext


class Newsletter(ModelSQL, ModelView):
    'Newsletter'
    __name__ = 'newsletter'
    name = fields.Char('Name', required=True)
    subscriptions = fields.Many2Many('newsletter.subscription-newsletter',
        'newsletter', 'newsletter_subscription', 'Subscriptions')
    active = fields.Boolean('Active', select=True)

    @staticmethod
    def default_active():
        return True


class NewsletterSubscription(ModelSQL, ModelView):
    'Newsletter Subscription'
    __name__ = 'newsletter.subscription'
    _rec_name = 'email'
    email = fields.Char('Email', required=True)
    name = fields.Char('Name')
    party = fields.Many2One('party.party', 'Party')
    newsletters = fields.Many2Many('newsletter.subscription-newsletter',
        'newsletter_subscription', 'newsletter', 'Newsletters')
    active = fields.Boolean('Active', select=True)
    lang = fields.Many2One("ir.lang", 'Language')

    @classmethod
    def __setup__(cls):
        super(NewsletterSubscription, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints += [
            ('email_uniq', Unique(t, t.email),
                'Only one subscription per email allowed.'),
            ]

    @staticmethod
    def default_active():
        return True

    @staticmethod
    def default_lang():
        pool = Pool()
        Lang = pool.get('ir.lang')

        if Transaction().language:
            lang, = Lang.search([
                ('code', '=', Transaction().language),
                ], limit=1)
            return lang.id

    @staticmethod
    def default_newsletters():
        Newsletter = Pool().get('newsletter')
        return [n.id for n in Newsletter.search([])]

    @classmethod
    def copy(cls, subscriptions, default=None):
        raise UserError(gettext('copy_not_available'))

    def get_rec_name(self, name):
        name = self.name or self.party and self.party.full_name or ''
        name += ', ' + self.email
        return name

    @classmethod
    def search_rec_name(cls, name, clause):
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [bool_op,
            ('email',) + tuple(clause[1:]),
            ('party.rec_name',) + tuple(clause[1:]),
            ('name',) + tuple(clause[1:]),
            ]

    @fields.depends('email', 'party')
    def on_change_email(self):
        ContactMechanism = Pool().get('party.contact_mechanism')

        if self.email:
            if self.party:
                emails = ContactMechanism.search([
                    ('type', '=', 'email'),
                    ('value', '=', self.email),
                    ])
                if not any(e.party == self.party for e in emails):
                    if len(emails) == 1:
                        self.party = emails[0].party
                        self.name = emails[0].party.full_name
                    else:
                        self.party = None
                        self.name = None
            else:
                emails = ContactMechanism.search([
                    ('type', '=', 'email'),
                    ('value', '=', self.email),
                    ], limit=1)
                if emails:
                    self.party = emails[0].party
                    self.name = emails[0].party.full_name
            self.update_lang()

    @fields.depends('email', 'party')
    def on_change_party(self):
        ContactMechanism = Pool().get('party.contact_mechanism')

        if self.party:
            emails = ContactMechanism.search([
                ('type', '=', 'email'),
                ('party', '=', self.party),
                ])
            if self.email:
                if not any(e.email == self.email for e in emails):
                    if len(emails) == 1:
                        self.email = emails[0].value
                        self.name = emails[0].party.full_name
                    else:
                        self.email = None
            else:
                if len(emails) == 1:
                    self.email = emails[0].value
                    self.name = emails[0].party.full_name
            self.update_lang()

    def update_lang(self):
        pool = Pool()
        Lang = pool.get('ir.lang')

        if self.party and self.party.lang:
            self.lang = self.party.lang
        elif Transaction().language:
            lang, = Lang.search([
                ('code', '=', Transaction().language),
                ], limit=1)
            self.lang = lang


class NewsletterSubscriptionNewsletter(ModelSQL):
    'Newsletter Subscription - Newsletter'
    __name__ = 'newsletter.subscription-newsletter'
    newsletter_subscription = fields.Many2One('newsletter.subscription',
        'Subscription', ondelete='CASCADE', required=True, select=True)
    newsletter = fields.Many2One('newsletter', 'Newsletter',
        ondelete='CASCADE', required=True, select=True)
