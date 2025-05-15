import { Tag } from "antd";

import Table from "../../../Table";
import { datasetsRowsTableStore } from "./store";

const DatasetRowsTable = ({id, colors}) => {
    const columns = [
        {
            dataIndex: 'num',
            title: '№',
            width: '7%',
        },
        {
            dataIndex: 'classname',
            title: 'Класс',
            // minWidth: '15%',
            render: (name) => (
                <Tag color={colors[name]}>{name}</Tag>
            )
        },
        {
            dataIndex: 'text',
            title: 'Текст',
        },
    ]

    return(
        <div className="w-full">
            <Table 
                columns={columns}
                store={datasetsRowsTableStore}
                fetch_args={{id: id}}
                tableLayout="auto"
            />
        </div>
    )
}

export default DatasetRowsTable;