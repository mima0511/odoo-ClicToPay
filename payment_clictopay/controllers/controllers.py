import logging
import pprint

_logger = logging.getLogger(__name__)
from odoo import http
from odoo.tools.translate import _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import requests
from ast import literal_eval
import json
import werkzeug.utils
from werkzeug.exceptions import BadRequest
from odoo.service import common
import logging
import requests
from urllib.parse import urlencode

_logger = logging.getLogger(__name__)
from odoo.addons.payment_clictopay.models.currency import CURRENCY_CODE


class WebsiteSale(WebsiteSale):
    _paytabs_feedbackUrl = '/payment/clictopay/checkout'
    _return_url = '/clictopay/feedback'

    @http.route([_paytabs_feedbackUrl], type='json', auth='public', website=True)
    def clictopay_payment(self, **post):
        currency = post.get('currency_id', request.env.company.currency_id.name)
        merchant_detail = request.env["payment.acquirer"].sudo().search([("provider", "=", "clictopay")])
        value = request.env['payment.transaction'].sudo().search([])
        clictopay_tx_values = {
            'userName': '0402392401',
            'password': '7VRJpvM5',
            'returnUrl': merchant_detail.clictopay_url().get('return_url'),
            'orderNumber': value[0].reference,
            'currency': int(CURRENCY_CODE.get(currency)),
            'amount': int(value[0].amount * 1000),
            'pageView': "DESKTOP",
            "failUrl": merchant_detail.clictopay_url().get('failUrl'),
            # 'sessionTimeoutSecs':30,
        }
        url = merchant_detail.clictopay_url().get('pay_page_url') + "?" + urlencode(clictopay_tx_values)
        result = requests.post(url=url)
        request_params = literal_eval(result.text)
        _logger.info("-----request_params-%r-", request_params)
        return request_params

    @http.route([_return_url], type='http', auth='public', website=True, csrf=False)
    def clictopay_feedback(self, **post):
        # merchant_detail = request.env["payment.acquirer"].sudo().search([("provider", "=", "clictopay")])
        order_status = 'https://test.clictopay.com/payment/rest/getOrderStatus.do'
        try:
            params = {
                'userName':'0402392401',
                'password': '7VRJpvM5',
                'orderId': post.get('orderId')
            }
            url = str(order_status) + "?" + urlencode(params)
            result = requests.get(url=url)
            request_params = json.loads(result.text)
        except Exception as e:
            request_params = {
                'status': 'cancel',
                "reference_no": request.session.get('so_id'),
                'result': 'The payment is cancelled successfully!',
                'response_code': '403'
            }
            request.session.pop('so_id', None)
        request.env['payment.transaction'].sudo()._handle_feedback_data('clictopay',request_params['OrderNumber'])
        return werkzeug.utils.redirect('/payment/status')

    @http.route(["/payment/clictopay/failed"], type='http', auth='public', website=True)
    def clictopay_failed(self, **post):
        _logger.info("-------------failed-------post %r---", post)
