import { useState } from 'react';
import { Link } from "react-router-dom";
import { Button, Tooltip } from 'antd';
import { PlusOutlined } from '@ant-design/icons'

import Table from "../../Table";
import { datasetsTableStore } from "./store";

import AddModal from './AddModal';


const columns = [
    {
        dataIndex: 'id',
        title: 'ID',
        width: '3%',
    },
    {
        dataIndex: 'name',
        title: 'Название',
        width: '20%',
        render: (name, record) => {
            return (
                <Link to={`/datasets/${record.id}`} className='text-blue-600 hover:font-bold'>
                    {name}
                </Link>
            )
        }
    },
    {
        dataIndex: 'class_count',
        title: 'Количество классов',
        width: '10%',
    },
    {
        dataIndex: 'rows_count',
        title: 'Количество элементов',
        width: '10%',
    },
    {
        dataIndex: 'description',
        title: 'Описание',
    },
]

const AddButton = ({ setOpen }) => {
    const onClick = () => {
        setOpen(true)
    }
    return (
        <Tooltip title='Добавить новый датасет'>
            <Button
                // type='primary'
                icon={<PlusOutlined />}
                onClick={onClick}
            />
        </Tooltip>
    )
}

const DatasetsTable = () => {
    const [open, setOpen] = useState(false);

    
    return (
        <div className="w-[99%] px-1">
            <Table
                size="small"
                columns={columns}
                store={datasetsTableStore}
                bordered
                actions={<AddButton setOpen={setOpen}/>}
            />
            <AddModal open={open} setOpen={setOpen}/>
        </div>
    )
}

export default DatasetsTable;