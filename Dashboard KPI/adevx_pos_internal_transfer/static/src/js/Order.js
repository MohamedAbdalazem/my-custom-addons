/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {

    _covert_pos_line_to_stock_move: function (line) {
        let line_val = {
            name: line.product_id.display_name,
            product_id: line.product_id.id,
            product_uom_qty: line.qty,
        };
        if (line.uom_id) {
            line_val['product_uom'] = line.uom_id
        }
        else {
            line_val['product_uom'] = line.product_id.uom_id.id
        }
        return [0, 0, line_val];
    }

})
