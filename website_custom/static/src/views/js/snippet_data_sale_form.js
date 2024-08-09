/* @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.saleOrderFormSnippet = publicWidget.Widget.extend({
    selector: '.s_sale_form_snippet',

    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        this._loadOrders();
        this._bindEvents();
    },

    _bindEvents: function () {
        this.$('.o_select_sale_order').on('', this._set_order_data.bind(this));
    },

    _loadOrders: async function () {
        try {
            const orders = await jsonrpc(
                '/myhome/sale_data_form',
            );
            const ordersContainer = this.el.querySelector('.o_select_sale_order');
            if (ordersContainer) {
                ordersContainer.innerHTML = '<option value="-1">Select order ........</option>' + orders.map(order => `<option value="${order.id}">${order.name}</option>`).join('');
            } else {
                console.error('Orders container not found.');
            }
        } catch (error) {
            console.error('Error loading orders:', error);
        }
    },

    _set_order_data: async function () {
        const ordersContainer = this.el.querySelector('.o_select_sale_order');
        const selectedValue = ordersContainer.value;

        if (selectedValue == -1) {
            this._clear_order_data();
            return;
        }

        try {
            const orderDetails = await jsonrpc(
                '/myhome/sale_selected_data_form',
                {'id': selectedValue}
            );
            this._display_order_data(orderDetails[0]);
        } catch (error) {
            console.error('Error fetching order details:', error);
        }
    },

    _clear_order_data: function () {
        const orderDataShow = this.el.querySelector('.order_data_show');
        if (orderDataShow) {
            orderDataShow.innerHTML = '';
        } else {
            console.error('Order data container not found.');
        }
    },

    _display_order_data: function (orderDetails) {
        const orderDataShow = this.el.querySelector('.order_data_show');
        if (orderDataShow) {
            orderDataShow.innerHTML = `
                <div class="alert alert-light text-dark border rounded-4" role="alert">
                    <div class="order-details">
                        <h3>Order Details</h3>
                        <p><strong>Order ID:</strong> ${orderDetails.id}</p>
                        <p><strong>Customer Name:</strong> ${orderDetails.partner}</p>
                        <p><strong>Order Date:</strong> ${orderDetails.order_date}</p>
                        <p><strong>Total Amount:</strong> ${orderDetails.total_amount}</p>
                        <h4>Items</h4>
                        <div class="row row-cols-1 row-cols-md-2 g-4">
                            ${orderDetails.items.map(item => `
                                <div class="card m-3" style="max-width: 540px;">
                                    <div class="row g-0">
                                        <div class="col-md-4">
                                            <img src="${item.product_image}" class="img-fluid rounded-start" alt="${item.product_name}">
                                        </div>
                                        <div class="col-md-8">
                                            <div class="card-body">
                                                <h5 class="card-title">${item.product_name}</h5>
                                                <p class="card-text">Quantity: ${item.quantity}</p>
                                                <p class="card-text">Price: ${item.price_subtotal}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        } else {
            console.error('Order data container not found.');
        }
    },
});

export default publicWidget.registry.saleOrderFormSnippet;
