/* @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.saleOrderFormCreatePortal = publicWidget.Widget.extend({
    selector: '.o_create_order_website',

    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        this._loadPartner();
        this._bindEvents();
    },
    _bindEvents: function () {
        this.$('.o_sale_order_create').on('click', this._create_sale_order.bind(this));
    },
    _loadPartner: async function () {
        try {
            const part = await jsonrpc(
                '/myhome/sale_data_create',
            );
            const ordersContainer = this.el.querySelector('.o_select_partner');
            if (ordersContainer) {
                ordersContainer.innerHTML = '<option value="-1">Select order ........</option>' + part.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
            } else {
                console.error('Orders container not found.');
            }
        } catch (error) {
            console.error('Error loading orders:', error);
        }
    },
    _create_sale_order: async function() {
        const ordersContainer = this.el.querySelector('.o_select_partner');
        const selectedValue = ordersContainer.value;

        if (selectedValue != -1) {
            console.log(selectedValue)
            const order = await jsonrpc(
                '/myhome/sale_data_create',
                {'id': selectedValue}
            );
            if (order.status == "success"){
                window.location.reload();
            }
        }
    }
});

export default publicWidget.registry.saleOrderFormCreatePortal;
