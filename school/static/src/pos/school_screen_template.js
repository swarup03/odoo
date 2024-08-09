/** @odoo-module **/

import { registry } from "@web/core/registry";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";

class BookedSchoolScreen extends TicketScreen {
    static template = "school.BookedSchoolScreen";
    setup() {
        super.setup();
        this.pos = usePos();
        this.orm = useService("orm");
    }
    back() {
        this.pos.showScreen('ProductScreen');
    }
}
registry.category("pos_screens").add("BookedSchoolScreen", BookedSchoolScreen);
