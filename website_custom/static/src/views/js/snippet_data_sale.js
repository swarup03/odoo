/* @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

// publicWidget.registry.s_sale_order_snippet = publicWidget.Widget.extend({
//     selector: '.s_sale_order_snippet',

//     start: async function () {
//         this._super.apply(this, arguments);
//         this.rpc = useService("rpc");
//         // this._bindEvents();
//         this._loadOrders();
//         console.log("hello Brother")
//         const orders = await this.rpc({
//             route: '/myhome/sale_data',
//         });
//         this._renderOrders(orders);
//     },

//     // _bindEvents: function () {
//     //     // Add any event bindings if necessary
//     // },

//     _loadOrders: async function () {
//         const orders = await this.rpc({
//             route: '/myhome/sale_data',
//         });
//         this._renderOrders(orders);
//     },

//     _renderOrders: function (orders) {
//         const ordersContainer = this.el.querySelector('.orders');
//         ordersContainer.innerHTML = orders.map(order => `<p>${order.name}</p>`).join('');
//     },
// });

// export default publicWidget.registry.s_sale_order_snippet;


publicWidget.registry.saleOrderName = publicWidget.Widget.extend({
    selector: '.s_sale_order_snippet',

    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        this._loadOrders();
    },

    _loadOrders: async function () {
        try {
            const orders = await jsonrpc(
                '/myhome/sale_data',
                {},
            );
            const ordersContainer = this.el.querySelector('.orders');
            if (ordersContainer) {
                // console.log(orders.map(order => `<p><a href="/saleOrder/${order.id}?access_token=${order.access_token}">${order.name}</a></p>`));
                ordersContainer.innerHTML = orders.map(order => `<p><a href="/saleOrder/${order.id}?access_token=${order.access_token}">${order.name}</a></p>`).join('');
            } else {
                console.error('Orders container not found.');
            }
        } catch (error) {
            console.error('Error loading orders:', error);
        }
    },
});

export default publicWidget.registry.saleOrderName;
