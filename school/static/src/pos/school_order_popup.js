/** @odoo-module **/
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class schoolOrderPopup extends AbstractAwaitablePopup {
    static template = "school.schoolOrderPopup";
    static defaultProps = {
        closeText: _t("Cancel"),
        confirmText: _t("Save"),
        title: _t("Create School Order"),
        // data: [],
        amount: 0,
    };

    setup(){
        super.setup();
        this.pos = usePos();
        this.state = useState({
            inputValue: this.props.startingValue || '',
            note: '',
            deliveryDate: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            schoolId: null,
        });
    }

    getPayload(){
        const schoolId = this.getSchoolId(this.state.inputValue);
        return {
            school_id: schoolId,
            school_name: this.state.inputValue,
            note: this.state.note,
            amount: this.props.amount,
            orderDate: this.props.currentDate,
            deliveryDate: this.state.deliveryDate,
            productOrderLine: this.pos.get_order().get_orderlines(),
        };
    }

    getSchoolId(name){
        // console.log(this.props.data)
        for(var l of this.props.data){
            console.log(l)
            if (l.name === name){
                return l.id;
            }
        }
        return null;
    }
}
