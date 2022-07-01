# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

{
    "name": "ClicToPay Payment Acquirer",
    "category": "Website",
    "version": "15.0.1",
    "sequence": 1,
    "author": "Wamia Group",
    "depends": ['payment', 'website_sale', 'sale'],
    "data": [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
        'views/payment_views.xml',
        'data/data.xml',
    ],

}
