/** @odoo-module **/

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    export_as_JSON() {
        const result = super.export_as_JSON(...arguments);
        result.note = this.note || "";
        result.discount = this.discount || false;
        result.locatin_add = this.locatin_add || "";
        return result;
    },
    setCustomNote(note) {
        this.note = note;
    },
    setCustomDiscount(discount){
        this.discount = discount;
    },
    setCustomSundry(){
        this.sundryNote = "Thank you for being out Sundry user";
    },
    setLocationWith(locatin_add){
        this.locatin_add = locatin_add
    },
    export_for_printing(){
        const result = super.export_for_printing(...arguments);
        result.note = this.note || "";
        result.sundryNote = this.sundryNote || "";
        result.locatin_add = this.locatin_add || "";
        return result;
    }
});