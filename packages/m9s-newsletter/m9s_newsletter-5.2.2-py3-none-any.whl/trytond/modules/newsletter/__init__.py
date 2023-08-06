# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import newsletter

__all__ = ['register']


def register():
    Pool.register(
        newsletter.Newsletter,
        newsletter.NewsletterSubscription,
        newsletter.NewsletterSubscriptionNewsletter,
        module='newsletter', type_='model')
