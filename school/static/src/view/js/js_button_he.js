/** @odoo-module **/
    import { patch } from "@web/core/utils/patch";
    import { ExpenseListController } from '@hr_expense/views/list';
    patch(ExpenseListController.prototype, {

        async actionhrList() {
            const records = this.model.root.selection;
            console.log(this.model)
            console.log(this.model.root)
            console.log(this.model.root.selection)

            // console.log(typeof records);
            console.log(records);
            let sum=0
            for (var key in records){
                // console.log(records[key])
                // console.log(key + "...." + records[key].resIds)
                sum += records[key].data.total_amount
                // console.log(records[key])
                // let datas = records[key].data
                // console.log(datas)
                // console.log(datas.name)
                // for (var key_1 in records[key]){
                //     console.log(key_1 + "...." + records[key].resId)
                // }
            }
            console.log(sum) 
            // const recordIds = records.map((a) => a.data.total_amount);
            // console.log(recordIds.reduce((a,b)=>a+b,0))
            const res = await this.orm.call(this.model.config.resModel, 'print_report', [records.map((record) => record.resId)]);
            // console.log(res)
            if (res) {
                await this.actionService.doAction(res, {});
            }
            },
    });