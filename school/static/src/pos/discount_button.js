/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";


export class OrderDiscountButton extends Component {
    static template = "point_of_sale.discountButton";

    setup() {
        super.setup();
        this.pos = usePos();
        this.popup = useService("popup");
        this.orm = useService("orm")

    }

    async showPopup(){
        const { confirmed, payload: inputNote } = await this.popup.add(TextInputPopup, {
            title: _t("Add Discount in percentage (%)"),
            // startingValue: _t("%"),
            placeholder: _t("%"),
            confirmText: _t("Add Discount"),
            cancelText: _t("Cancel"),
        });
        return { confirmed, inputNote };
    }

    async onClickDiscount() {
        console.log(this.pos.get_order())
        let status = true;
        while (status) {
            const orderLines = this.pos.get_order().get_orderlines();
            if (!orderLines.length) {
                return;
            }

            const { confirmed, inputNote } = await this.showPopup();
            const values = Number(inputNote);
            
            if (confirmed) {
                if (values){
                    if (values < 100 && values >= 0) {
                        for (const orderline of orderLines) {
                            orderline.set_discount(values);
                        }
                        status = false;
                    } else {
                        await this.popup.add(ErrorPopup, {
                            title: _t("Invalid Discount"),
                            body: _t("You can't add a discount of %s%. Please enter a value between 0% and 100%.", values),
                            cancelKey: true,
                        });
                    }
                
                }else{
                    await this.popup.add(ErrorPopup, {
                        title: _t("Invalid input"),
                        body: _t("You can't add a discount because you enter incorrect data."),
                        cancelKey: true,
                    });
                }
            }else{
                break;
            }

        }
    }
    async onClickDiscountDefault(){
        const Orderlines = this.pos.get_order().get_orderlines();
        const order = this.pos.get_order();
        console.log(Orderlines)
        console.log(this.pos.get_order())
        console.log(this.pos.get_order().get_current_screen_data())
        const result = await this.orm.call('pos.order', 'get_discount', ['true']);
         for (let orderLine of Orderlines){
            orderLine.set_discount(result);
           }
        order.setCustomDiscount(true);
    }
}

ProductScreen.addControlButton({
    component: OrderDiscountButton,
    condition: function () {
        return this.pos.config.enable_school;
    },
});
