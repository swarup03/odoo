/* @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.searchCategoryDirect = publicWidget.Widget.extend({
    selector: '#o_search_modal_category',

    /**
     * @override
     */
    start: function () {
        console.log("Widget initialized");
        this._super.apply(this, arguments);
        this._bindEvents();
    },

    _bindEvents: function () {
        this.$('.input_search_category').on('input', this._get_category_data.bind(this));
        this.$('.o_search_button').on('click', this._search_category_action(this))
    },

    _search_category_action: function () {

    },

    _get_category_data: function () {
        const query = this.$('.input_search_category').val();
        if (query.length > 0) {
            jsonrpc('/get_categories', { query: query }).then((categories) => {
                this._renderCategoryList(categories);
            });
        }
        else{
        const $categoryList = this.$('.category_list');
        $categoryList.empty();
        }
    },

    _renderCategoryList: function (categories) {
        const $categoryList = this.$('.category_list');
        $categoryList.empty();

        if (categories.length > 0) {
            categories.forEach(category => {
                const $item = $('<p>').text(category.name).data('category-id', category.id).addClass('category-item p-3 fs-5 border round-4');
                $categoryList.append($item);

                $item.on('click', this._redirectToCategoryPage.bind(this));
            });
        } else {
            const $noRecord = $('<p>').text('No records found').addClass('text-center text-muted p-3 fs-5');
            $categoryList.append($noRecord);
        }
    },


    _redirectToCategoryPage: function (event) {
        const categoryId = $(event.currentTarget).data('category-id');
        window.location.href = `/shop/category/${categoryId}`;
    },
});

export default publicWidget.registry.searchCategoryDirect;
