/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component } from "@odoo/owl";
import { ask } from "@point_of_sale/app/store/make_awaitable_dialog";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

export class InternalTransferPopup extends Component {
    static template = "adevx_pos_internal_transfer.InternalTransferPopup"
    static components = { Dialog };
    static props = [
        "close",
        "note?",
        "order",
        "internal_transfer_auto_confirm",
        "picking_type_id?",
        "location_dest_id?",
    ];
    static defaultProps = {
        confirmText: _t("Save on backend"),
        cancelText: _t("Close"),
        title: _t("Create Internal Transfer"),
    };

    setup() {
        super.setup();
        this.pos = usePos();
        this.dialog =  useService("dialog");
        this.currentOrder = this.pos.get_order();
        this.orm = useService("orm");
        this.changes = {
            note: this.props.order.note,
            internal_transfer_auto_confirm: this.props.internal_transfer_auto_confirm,
            picking_type_id: null,
            location_dest_id: null,
        }
        this.numberBuffer = useService("number_buffer");
        this.numberBuffer.use({
            triggerAtEnter: () => this.OnConfirmTransfer(),
            triggerAtEscape: () => this.cancel(),
            state: this.changes,
        });
    }

    OnChange(event) {
        let target_name = event.target.name;

        if (event.target.type == 'checkbox') {
            this.changes[event.target.name] = event.target.checked;
        } else if (target_name == 'picking_type_id') {
            let picking_type_id = parseFloat(event.target.value);
            this.changes[event.target.name] = picking_type_id;
            let selectedPickType = this.pos.config.transfer_picking_type_ids.filter(p => p.id === picking_type_id)
            this.changes['location_id'] = parseFloat(selectedPickType[0].default_location_src_id.id)
        } else if (target_name == 'location_dest_id') {
            this.changes[event.target.name] = parseFloat(event.target.value);
        } else {
            this.changes[event.target.name] = event.target.value;
        }
        this.verifyChanges(event)
    }

    verifyChanges(event) {
        let changes = this.changes;
        if (changes.picking_type_id && !changes.picking_type_id){
            return this.dialog.add(ConfirmationDialog, {
                title: _t('Error'),
                body: _t('Please select Picking Type'),
            })
        }
        if (changes.location_id && !changes.location_id){
            return this.dialog.add(ConfirmationDialog, {
                title: _t('Error'),
                body: _t('Please select Source Location'),
            })
        }
    }

    async OnConfirmTransfer() {
        if (!this.changes.note){
            return this.dialog.add(ConfirmationDialog, {
                title: _t('Error'),
                body: _t('Please full fill information of order'),
            })
        }
        let order = this.currentOrder;
        console.log("this.changes.location_id",this.changes.location_id)
        let value = {
            name: order.name,
            note: this.changes.note,
            origin: this.pos.config.name,
            partner_id: order.get_partner() ? order.get_partner().id : false,
            picking_type_id: this.changes.picking_type_id,
            location_id: this.changes.location_id,
            location_dest_id: this.changes.location_dest_id,
            move_ids_without_package: []
        }
        for (var i = 0; i < order.lines.length; i++) {
            var line = order.lines[i];
            var line_val = order._covert_pos_line_to_stock_move(line);
            line_val[2]['location_id'] =  this.changes.location_id;
            line_val[2]['location_dest_id'] =  this.changes.location_dest_id;
            value.move_ids_without_package.push(line_val);
        }
        let result = await this.orm.call(
             "stock.picking",
             "create_from_pos_ui",
             [
                value,
                - this.changes.internal_transfer_auto_confirm
             ]
        )
        this.pos.removeOrder(this.currentOrder);
        this.pos.selectNextOrder();
        this.props.close()
        const confirmed = await ask(this.dialog, {
            body: _t("Successfully Created: %s", result.name),
        });
    }


}
