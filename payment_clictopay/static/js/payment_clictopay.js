odoo.define('payment_clictopay.clictopay', function (require) {
    "use strict";
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');
    var ajax = require('web.ajax');

    var qweb = core.qweb;
    var _t = core._t;
    var ClicToPayPaymentForm = Widget.extend({
    init: function() {
          console.log(this);
          this.reference = $('#reference').val();
          this.amount = $('#amount').val();
          this.currency = $('#currency').val();
          this.acquirer = $('#acquirer').val();
          this.start();
      },
    start: function() {
          var self = this;
          self._createClickToPayCheckoutId();
      },
    _createClickToPayCheckoutId: function() {
          var self = this;
          ajax.jsonRpc('/payment/clictopay/checkout', 'call', {
              'reference': self.reference,
              'amount': self.amount,
              'currency': self.currency,
              'acquirer': self.acquirer

          })
          .then(function (result) {
            if (result.errorMessage!= 4 &&result.orderId && result.formUrl)  {
                window.location = result.formUrl;
              }
            else {
              var error_note = $('#error_note');
                if (error_note.length) {
                    $('#error_note').text(' ' + result.errorMessage)
                } else {
                   var form_el = $('input[data-provider="clictopay"]').parent().append('<div id="error_note" style="font-weight:bold;color:red;">'+result.errorMessage+'</div>')
                }
                setTimeout(function(){ location.reload(true); }, 5000);
                  }
          });
      },

      });
    new ClicToPayPaymentForm();

});
