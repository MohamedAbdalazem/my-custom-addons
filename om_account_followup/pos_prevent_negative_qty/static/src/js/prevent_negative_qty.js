/** @odoo-module **/

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(ProductScreen.prototype, {

    async _addProductToOrder(product, options = {}) {
        const order = this.currentOrder;
        const existingLine = order
            .get_orderlines()
            .find(line => line.product.id === product.id);

        const qtyInOrder = existingLine ? existingLine.quantity : 0;
        const requestedQty = qtyInOrder + 1;
        const availableQty = product.qty_available;

        if (availableQty <= 0 || requestedQty > availableQty) {
            await this.dialog.add(AlertDialog, {
                title: "⚠️ تنبيه",
                body: `
                    الكمية غير كافية لهذا المنتج
                    <br/><br/>
                    <b>المتوفر:</b> ${availableQty}
                    <br/>
                    <b>المطلوب:</b> ${requestedQty}
                `,
            });
            return;
        }

        await super._addProductToOrder(product, options);
    },
});
