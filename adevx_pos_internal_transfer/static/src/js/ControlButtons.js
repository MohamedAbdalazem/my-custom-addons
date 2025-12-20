/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { InternalTransferPopup } from "@adevx_pos_internal_transfer/js/InternalTransferPopup";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
        this.dialog =  useService("dialog");
        this.create_internal_transfer = this.pos.config.create_internal_transfer;
    },

    async OnClickTransfer() {
        let order = this.pos.get_order();
        if (order.get_total_with_tax() <= 0 || order.lines.length == 0) {
              return this.dialog.add(ConfirmationDialog, {
                title: _t('Error'),
                body: _t('Your shopping cart is empty !'),
            })
        }
        await this.dialog.add(InternalTransferPopup, {
            order: order,
            internal_transfer_auto_confirm: this.pos.config.internal_transfer_auto_confirm
        });
    },

});

