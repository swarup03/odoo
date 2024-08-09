/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { TextAreaPopup } from "@point_of_sale/app/utils/input_popups/textarea_popup";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
// import { Order } from "@point_of_sale/app/store/models";
// import { patch } from "@web/core/utils/patch";

export class OrderNoteButton extends Component {
    static template = "point_of_sale.notesButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");

    }
    async onClick() {
        const selectedOrderline = this.pos.get_order().get_selected_orderline();
        const order = this.pos.get_order();
        // console.log()
        // console.log(this.pos.get_order())
        // console.log(this.pos.get_order().set_screen_data("fvjwrbre"))
        // console.log(this.pos.get_order().save_to_db("mmvmds"))
        // console.log(this.pos.get_order().get_total_for_taxes())
        // console.log(this.pos.get_order().get_total_discount())
        // console.log(this.pos.get_order().get_subtotal())
        // console.log(selectedOrderline.set_discount(20))
        console.log(selectedOrderline)
        // FIXME POSREF can this happen? Shouldn't the orderline just be a prop?
        if (!selectedOrderline) {
            return;
        }
        const { confirmed, payload: inputNote } = await this.popup.add(TextAreaPopup, {
            // startingValue: selectedOrderline.get_customer_note(),
            title: _t("Add Customer Notes for order"),
        });

        // if (confirmed) {
        //     this.customerNote = inputNote || "";
        //     const result = await this.orm.call('pos.order', 'added_note', [(inputNote,order_name)]);
        //     console.log(this.pos.get_order().name)
        //     console.log(result)

        // }
        if (confirmed) {
            let note = document.getElementsByClassName("order-note")
            if (note.length > 0){
                note[0].innerText = inputNote
            }
            order.setCustomNote(inputNote);
            
        }
    }
}


ProductScreen.addControlButton({
    component: OrderNoteButton,
    condition: function () {
        return this.pos.config.enable_school;
    },
});

