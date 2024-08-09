/** @odoo-module **/

import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";

class BookedOrdersTempButton extends Component {
static template = 'point_of_sale.templateButton';
    setup() {
        this.orm = useService("orm");
        this.pos = usePos();
    }
    async onClickShowTemp() {
       var self = this
       await this.orm.call("school.profile","pass_in_pos",['true'],{}
       ).then(function(result) {
            self.pos.showScreen('BookedSchoolScreen',{
                data: result,
            });
        });
    }
}
ProductScreen.addControlButton({
    component: BookedOrdersTempButton,
    condition: () => true
})