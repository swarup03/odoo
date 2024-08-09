/**@odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
// import { usePos } from "@point_of_sale/app/store/pos_hook";
// import { CustomAlertPopup } from "@pos_buttons/js/PopUp/pos_pop_up";
import { patch } from "@web/core/utils/patch";
patch(PaymentScreen.prototype, {
	
    async onClickPaymentAdd() {    
        console.log("hello Brother!")
    // this.popup.add(CustomAlertPopup, {
            
    // title: _t('Custom Alert'),
                    
    // body: _t('Choose the alert type')
        
    }
});
	