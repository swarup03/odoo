/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { CustomDroapdownPopup } from "@school/pos/custom_droapdown_popup"
import { useState } from "@odoo/owl";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
// import { useService, watch } from "@web/core/utils/hooks";



export class OrderlocationButton extends Component {
    static template = "point_of_sale.locationButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
        this.orm = useService("orm");
        this.state = useState({ locationText: _t("Location"), locationAdded: false  });
        // watch(this.pos.get_order(), 'partner', this._onPartnerChange.bind(this));
    }
    _onPartnerChange(newPartner) {
        if (!newPartner) {
            this.state.locationText = _t("Location");
            this.state.locationAdded = false;
        }
    }
    async onClick() {
        let status = true;
        while (status) {
            console.log(this.pos.get_order().partner)
            const selectedOrderline = this.pos.get_order().get_selected_orderline();
            
        
            // console.log(this.pos)
            // FIXME POSREF can this happen? Shouldn't the orderline just be a prop?
            if (!selectedOrderline) {
                return;
            }
            if (this.pos.get_order().partner){
                const locations = await this.orm.call('pos.order', 'get_location', ['true']);
                // console.log(locations)
                const { confirmed, payload: selectedLocation } = await this.popup.add(CustomDroapdownPopup, {
                    // startingValue: selectedOrderline.get_customer_note(),
                    title: _t("Add Location"),
                    locations: locations, 
                });
                if (confirmed) {
                    const order = this.pos.get_order();
                    console.log(selectedLocation)
                    if (!selectedLocation){
                        await this.popup.add(ErrorPopup, {
                            title: _t("Invalid Location"),
                            body: _t("Please select the proper location."),
                            cancelKey: true,
                        });
                    }
                    else{
                        // console.log(selectedLocation)
                        order.setLocationWith(selectedLocation)
                        this.state.locationText = selectedLocation || _t("Location");
                        this.state.locationAdded = !!selectedLocation;
                        break
                        
                    }
                }
                else{
                    break
                }
            }else{
                await this.popup.add(ErrorPopup, {
                    title: _t("Select Partner"),
                    body: _t("Please select the Partner."),
                    cancelKey: true,
                });
                break
            }
        }
    }
    getButtonClass() {
        return this.state.locationAdded ? 'text-success' : 'text-danger';
    }
}


ProductScreen.addControlButton({
    component: OrderlocationButton,
    // condition: function () {
    //     return this.pos.config.enable_school;
    // },
});

