/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PlanningGanttController } from '@planning/views/planning_gantt/planning_gantt_controller';
import { useService } from "@web/core/utils/hooks";

patch(PlanningGanttController.prototype, {
    setup() {
        super.setup();
        this.notificationService = useService("notification");
        this.actionService = useService('action');
    },

    async actionPlanningList() {
        console.log("hello brother");
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
        },
});