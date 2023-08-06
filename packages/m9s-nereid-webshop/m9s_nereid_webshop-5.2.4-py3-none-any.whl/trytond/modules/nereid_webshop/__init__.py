# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import checkout
from . import website
from . import webshop
from . import product
from . import invoice
from . import sale
from . import party
from . import tree


__all__ = ['register']


def register():
    Pool.register(
        checkout.Checkout,
        webshop.ArticleCategory,
        webshop.Company,
        webshop.BannerCategory,
        webshop.Banner,
        webshop.Article,
        webshop.MenuItem,
        webshop.WebShop,
        website.Website,
        product.Product,
        invoice.Invoice,
        party.Address,
        sale.Sale,
        sale.SaleLine,
        tree.Node,
        module='nereid_webshop', type_='model')
