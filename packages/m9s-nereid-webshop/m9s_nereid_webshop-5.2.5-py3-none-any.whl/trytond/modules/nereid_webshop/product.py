# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal

from trytond.pool import Pool, PoolMeta
from jinja2.filters import do_striptags
from werkzeug.exceptions import NotFound

from nereid import jsonify, flash, request, url_for, route, redirect, \
    render_template, abort, current_locale, current_website, Markup
from nereid.contrib.locale import make_lazy_gettext
from nereid.globals import session

from .forms import GiftCardForm

_ = make_lazy_gettext('nereid_webshop')


class Product(metaclass=PoolMeta):
    __name__ = "product.product"

    def serialize(self, purpose=None):
        """
        Downstream implementation which adds a key called inventory_status
        to the dictionary if purpose is 'variant_selection'.

        :param purpose: String which decides structure of dictionary
        """
        res = super(Product, self).serialize(purpose=purpose)

        if purpose == 'variant_selection':
            res.update({
                'inventory_status': self.inventory_status(),
            })

        return res

    def get_default_image(self, name):
        "Returns default product image"
        # Fallback condition if there is no default_image_set defined
        images = self.get_images()
        if images:
            return images[0].id
        else:
            # TODO should this be explicitly cached?
            if current_website.default_product_image:
                return current_website.default_product_image.id

    def ga_product_data(self, **kwargs):
        '''
        Return a dictionary of the product information as expected by Google
        Analytics

        Other possible values for kwargs include

        :param list: The name of the list in which this impression is to be
                     recorded
        :param position: Integer position of the item on the view
        '''
        rv = {
            'id': self.code or str(self.id),
            'name': self.name,
            'category': self.account_category and
                self.account_category.name or None,
        }
        rv.update(kwargs)
        return rv

    def json_ld(self, **kwargs):
        '''
        Returns a JSON serializable dictionary of the product with the Product
        schema markup.

        See: http://schema.org/Product

        Any key value pairs passed to kwargs overwrites default information.
        '''
        sale_price = self.sale_price(1)

        return {
            "@context": "http://schema.org",
            "@type": "Product",

            "name": self.name,
            "sku": self.code,
            "description": do_striptags(self.description),
            "offers": {
                 "@type": "Offer",
                 "availability": "http://schema.org/InStock",
                 "price": str(sale_price),
                 "priceCurrency": current_locale.currency.code,
            },
            "image": self.default_image.transform_command().thumbnail(
                500, 500, 'a').url(_external=True),
            "url": self.get_absolute_url(_external=True),
        }

    @classmethod
    @route('/product/<uri>')
    @route('/product/<path:path>/<uri>')
    def render(cls, uri, path=None):
        """
        Render gift card template if product is of type gift card
        """
        render_obj = super(Product, cls).render(uri, path)

        if not isinstance(render_obj, NotFound) \
                and render_obj.context['product'].is_gift_card:
            # Render gift card
            return redirect(
                url_for('product.product.render_gift_card', uri=uri)
            )
        return render_obj

    @classmethod
    @route('/gift-card/<uri>', methods=['GET', 'POST'])
    def render_gift_card(cls, uri):
        """
        Add gift card as a new line in cart
        Request:
            'GET': Renders gift card page
            'POST': Buy Gift Card
        Response:
            'OK' if X-HTTPRequest
            Redirect to shopping cart if normal request
        """
        pool = Pool()
        SaleLine = pool.get('sale.line')
        Cart = pool.get('nereid.cart')

        try:
            product, = cls.search([
                ('displayed_on_eshop', '=', True),
                ('uri', '=', uri),
                ('template.active', '=', True),
                ('is_gift_card', '=', True)
            ], limit=1)
        except ValueError:
            abort(404)

        form = GiftCardForm(product)

        if form.validate_on_submit():
            cart = Cart.open_cart(create_order=True)

            # Code to add gift card as a line to cart
            order_line = SaleLine(**{
                'product': product.id,
                'sale': cart.sale.id,
                'type': 'line',
                'sequence': 10,
                'quantity': 1,
                'unit': None,
                'description': None,
                'recipient_email': form.recipient_email.data,
                'recipient_name': form.recipient_name.data,
                'message': form.message.data,
                'warehouse': cart.sale.warehouse
            })
            order_line.on_change_product()

            # Here 0 means the default option to enter open amount is
            # selected
            if form.selected_amount.data != 0:
                order_line.gc_price = form.selected_amount.data
                order_line.on_change_gc_price()
            else:
                order_line.unit_price = Decimal(form.open_amount.data)
            if getattr(order_line, 'gross_unit_price', None):
                order_line.gross_unit_price = order_line.unit_price

            order_line.save()

            message = _('Gift Card has been added to your cart')
            if request.is_xhr:  # pragma: no cover
                return jsonify(message=message)

            flash(message, 'info')
            return redirect(url_for('nereid.cart.view_cart'))

        return render_template(
            'catalog/gift-card.html', product=product, form=form
        )

    def get_absolute_url(self, **kwargs):
        """
        Return gift card URL if product is a gift card
        """
        if self.is_gift_card:
            return url_for(
                'product.product.render_gift_card', uri=self.uri, **kwargs
            )
        return super(Product, self).get_absolute_url(**kwargs)

    def get_menu_item(self, max_depth):
        """
        Return dictionary with serialized node for menu item
        {
            title: <display name>,
            link: <url>,
            record: <instance of record> # if type_ is record
        }
        """
        return {
            'record': self,
            'title': self.name,
            'image': self.default_image,
            'link': self.get_absolute_url(),
        }

    def get_meta_description(self):
        '''
        Provide a useful description for the meta description tag
        https://support.google.com/webmasters/answer/79812?hl=en&ref_topic=4617741
        https://support.google.com/webmasters/answer/35624?rd=1#1
            <meta name="Description" CONTENT="Author: A.N. Author,
            Illustrator: P. Picture, Category: Books, Price:  £9.24,
            Length: 784 pages">
        '''
        description = self.name
        description += ', Category: %s' % self.template.category.name
        if self.template.brand:
            description += ', Brand: %s' % self.template.brand.rec_name
        return Markup(description)

    @classmethod
    def recent_products_list(cls):
        '''
        Return a list of recently visited products as active records.
        '''
        products = []
        if hasattr(session, 'sid'):
            products = cls.browse(session.get('recent-products', []))
        return products
