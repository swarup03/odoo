/** @odoo-module **/

import { Order } from "@point_of_sale/app/store/models";
import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget";
// import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";


// Extending the Order class
class AllQuantityOrder extends Order {
    static template = 'point_of_sale.QuantityAdded';

    static props = {
       ...OrderWidget.props,
       productCount:{ type: Function, optional: true },
    };
    static defaultProps = {
        productCount: () => this.productCount(),
    };

    productCount(){
        return this.pos.get_order().get_orderlines().length;
    }
}
registry.category("models").add("AllQuantityOrder", AllQuantityOrder);

// Register the new class to be used within the POS system
// export const models = {
//     Order: AllQuantityOrder,
// };

// import { useState, useService } from "@odoo/owl";
// import { registry } from "@web/core/registry";
// import { Component } from "@odoo/owl";

// class QuantityChildAdded extends Component {
//     setup() {
//         this.onClickAction = this.props.onClickAction;
//     }
// }

// QuantityChildAdded.template = "point_of_sale.QuantityChildAdded";
// registry.category("components").add("QuantityChildAdded", QuantityChildAdded);

// export class QuantityAdd extends OrderWidget {
//     setup() {
//         super.setup();
//         this.pos = useService("pos");
//         this.ui = useService("ui");
//         this.state = useState({
//             methodProps: {
//                 partner: this.props.partner,
//             },
//         });
//         this.ActionPartner = this.onClickAction.bind(this);
//     }

//     onClickAction() {
//         console.log("Button clicked!");
//         // Add your custom action logic here
//     }
// }

// QuantityAdd.template = "point_of_sale.QuantityAdded";
// registry.category("pos_screens").add("QuantityAdd", QuantityAdd);
