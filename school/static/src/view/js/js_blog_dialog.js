/** @odoo-module **/
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
// import { jsClassDialog } from "./js_blog_dialog";

class jsClassModelInfo extends FormController {
    async actionInfoForm() {
        // var status = alert("hello, Brother");
        const record = this.model.root;
        console.log(record.data.partner_shipping_id);
}
}

jsClassModelInfo.template = "school.modelInfoBtn";

export const modelInfoView = {
    ...formView,
    Controller: jsClassModelInfo,
};

registry.category("views").add("model_info", modelInfoView);
