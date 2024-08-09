/** @odoo-module **/
import { registry } from '@web/core/registry';
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from '@web/core/utils/hooks';

class jsClassModelListInfo extends ListController {
    setup() {
        super.setup();
        this.orm = useService('orm');
        this.notificationService = useService("notification");
        this.actionService = useService('action');
    }
    async actionSaleList() {
        const records = this.model.root.selection;
        console.log(records)
        const res = await this.orm.call(this.model.config.resModel, 'print_xlsx_report', [records.map((record) => record.resId)]);
        if (res) {
            await this.actionService.doAction(res);
            this.notificationService.add("You closed a deal!", {
                title: "OOPS!",
                type: "danger",
                buttons: [
                    {
                        name: "Something went Wring",
                        onClick: () => {
                            this.actionService.doAction("commission_action");
                        },
                    },
                ],
              });
        }
    }
}
jsClassModelListInfo.template = "school.modelSchoolBtn";

export const modelInfoListView = {
    ...listView,
    Controller: jsClassModelListInfo,
};
registry.category("views").add("student_view_list", modelInfoListView);