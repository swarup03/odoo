/* @odoo-module */  

import PortalSidebar from "@portal/js/portal_sidebar";

PortalSidebar.include({
    events: {
        "click .o_print_btn": "_onChangeButton",
        // "click .o_portal_invoice_print d-block": "_onChangeButton",
    },
    start: function () {
        this.autoStreetTwo = document.querySelector(".o_portal_sidebar");
        var button = this.autoStreetTwo.querySelector(".o_portal_sale_sidebar");
        button.style.backgroundColor = "#DEDEDE"; 
        button.style.borderRadius = "30px";
        button.style.padding = "20px";
        // this.autoFromFirst = document.querySelector(".o_portal_sidebar_content");
        return this._super.apply(this, arguments);
    },
    _onChangeButton: function () {
        console.log("Hello brother")
        // console.log(this.autoStreetTwo.querySelectorAll(".o_portal_invoice_print"))
        var button = this.autoStreetTwo.querySelector(".o_portal_invoice_print");
        // debugger;
        if (button) {          
            button.style.backgroundColor = "#EA1818"; 
            button.style.color = "#FCFCFC";
            button.style.borderRadius = "30px";
            button.disabled = true;
        }
    },
});