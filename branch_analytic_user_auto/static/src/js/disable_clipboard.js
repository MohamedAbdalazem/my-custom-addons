odoo.define('branch_analytic_user_auto.disable_clipboard', function (require) {
    "use strict";

    var RPCErrorDialog = require('web.rpc_error_dialog');

    // override function onClickClipboard
    RPCErrorDialog.include({
        onClickClipboard: function () {
            // Do nothing to avoid TypeError
            console.warn('Clipboard copy disabled to prevent error.');
        },
    });
});
