/** @odoo-module **/

import { Order } from "@point_of_sale/app/store/models";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    async add_product(product, options) {
        const qty_available = product.qty_available || 0;
        const qty_to_add = options?.quantity || 1;
        if (product.type === 'product' && qty_available < qty_to_add) {
            this.env.services.popup.add(ErrorPopup, {
                title: this.env._t("الكمية غير متوفرة"),
                body: this.env._t(
                    `لا يمكن بيع المنتج "${product.display_name}" لأن الكمية (${qty_available}) غير كافية في المخزون.`
                ),
            });
            return;
        }
        await super.add_product(product, options);
    },
});
