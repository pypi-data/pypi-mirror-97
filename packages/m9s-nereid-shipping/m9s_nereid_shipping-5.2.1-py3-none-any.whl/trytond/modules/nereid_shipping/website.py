# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import ModelSQL, fields


class Website(metaclass=PoolMeta):
    __name__ = 'nereid.website'

    carriers = fields.Many2Many(
        "nereid.website.website-carrier", "website", "carrier", "Carriers")


class WebsiteCarrier(ModelSQL):
    "Website Carrier"
    __name__ = "nereid.website.website-carrier"

    website = fields.Many2One(
        "nereid.website", "Website", ondelete='CASCADE', select=True,
        required=True)
    carrier = fields.Many2One(
        "carrier", "Carrier", ondelete='CASCADE', select=True, required=True)
