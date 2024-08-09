/** @odoo-module **/
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


class jsClassModelIcon extends FormController {
    setup() {
        super.setup();
        this.orm = useService('orm');
        this.notificationService = useService("notification");
        this.actionService = useService('action');
    }

    async actionAutoFill() {
        const recordId = this.model.root.resId;
        const result = await this.orm.call(this.model.config.resModel, 'print_report', [recordId]);
        // console.log(result)
        const action = result[0];
        // console.log(action)
        const status = result[1].status;
        // console.log(status)

        if (action) {

            if (status === "pass") {
                this.notificationService.add("You passed the Exam.", {
                    title: "Congratulations!",
                    type: "success",
                });
                await this.actionService.doAction(action);
            } else if (status === "fail") {
                this.notificationService.add("You Failed the Exam.", {
                    title: "OOPS!",
                    type: "danger",
                });
                await this.actionService.doAction(action);
            }else if (status === 'pending'){
                this.notificationService.add("Your Exam is Pending.", {
                    title: "OOPS!",
                    type: "warning",
                });
            }
            else {
                this.notificationService.add("Something went Wrong.", {
                    title: "OOPS!",
                    type: "danger",
                });
            }
        }
    }
    
    async actionFormIcon() {
        // console.log("hello brother");
        this.notificationService.add("You closed a deal!", {
            title: "OOPS!",
            type: "warning",
            buttons: [
                {
                    name: "See your Commission",
                    onClick: () => {
                        this.actionService.doAction("commission_action");
                    },
                },
            ],
          });
    }
}

jsClassModelIcon.template = "school.autoFillBtn";

export const modelIconView = {
    ...formView,
    Controller: jsClassModelIcon,
};

registry.category("views").add("student_view_form", modelIconView);
