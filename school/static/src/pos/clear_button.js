/** @odoo-module **/
// import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";

import { usePos } from "@point_of_sale/app/store/pos_hook";
// import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

export class CreateButton extends Component {
	
    static template = "point_of_sale.CreateButton";

    setup() {    
    this.pos = usePos();
    this.numberBuffer = useService("number_buffer")
    
    // this.popup = useService("popup");
        
    }

    async onClearSelected() {  
        const currentOrder = this.pos.get_order();  
        // console.log("selectedOrderline",selectedOrderline);
        // var currentOrder = this.pos.get_order().get_partner()
        const selectedLine = currentOrder.get_selected_orderline();
        // console.log("selectedLine",selectedLine)

        if (!selectedLine) {
            return;
        }
        // this.currentOrder.removeOrderline(selectedLine);
        currentOrder.removeOrderline(selectedLine);

        // this.popup.add(ErrorPopup, {
        //     title: _t("Cannot modify a tip"),
        //     body: _t("Customer tips, cannot be modified directly"),
        // });
        // console.log("frughug");
        
    }
    async onClearAll() {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) {
            return;
        }
        // console.log(this.pos)
        // console.log(this.pos.get_order())
        // console.log(this.pos.get_order().get_orderlines())
        const orderLines = currentOrder.get_orderlines().slice(); // Create a copy of the array
        
        // Iterate over the copied array and remove each order line
        // for (let i = 0; i < orderLines.length; i++) {
        //     currentOrder.removeOrderline(orderLines[i]);
        // }
        for (var i of orderLines) {
            currentOrder.removeOrderline(i);
        }
    }
    async onTestClick(){
        const currentOrder = this.pos.get_order();
        const product = currentOrder.get_selected_orderline();
        this.pos.addProductToCurrentOrder(product)
    }
}
/**
 * Add the OrderlineProductCreateButton component to the control buttons in
   the ProductScreen.
 */
ProductScreen.addControlButton({
    component: CreateButton,
    position: ["before","CustomerButton"],
    condition: function () {
        return this.pos.config.enable_school;
    },
});
