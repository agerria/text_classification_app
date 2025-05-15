import { useState } from 'react';
import { Link, useNavigate } from "react-router-dom";
import { Button, Badge, Select } from 'antd';

import Table from "../../Table";
import { comparisonTableStore as store } from './store';

import { hashsToQuery } from '../helpers';
import { useSnapshot } from 'valtio';

const columns = [
    {
        dataIndex: 'hash',
        title: 'HASH',
        // width: '3%',
        render: (name, record) => {
            return (
                <Link to={`/classification/${record.hash}`} className='text-blue-600 hover:font-bold'>
                    {name}
                </Link>
            )
        }
    },
    {
        dataIndex: 'dataset',
        title: 'Датасет',
        // width: '20%',
        render: (name, record) => {
            return (
                <Link to={`/datasets/${record.dataset_id}`} className='text-blue-600 hover:font-bold'>
                    {name}
                </Link>
            )
        }
    },
    {
        dataIndex: 'vectorizer',
        title: 'Векторизатор',
        // width: '20%',

    },
    {
        dataIndex: 'classifier',
        title: 'Классификатор',
        // width: '10%',
    },
    // {
    //     dataIndex: 'rows_count',
    //     title: 'Количество элементов',
    //     width: '10%',
    // },
    {
        dataIndex: 'description',
        title: 'Описание',
    },
]

const CompareButton = ({ selected }) => {
    const navigate = useNavigate();
    const onClick = () => {
        navigate(
            `/comparison/report?hashs=${hashsToQuery(selected)}`
        )
    }

    const count = selected.length;
    const color = (count < 2) ? 'red' : 'green';

    return (
        <Badge count={count} color={color}>
            <Button onClick={onClick} disabled={count < 2} type='primary' >
                Сравнить
            </Button>
        </Badge>
    )
}

const DatasetSelect = () => {
    const $store = useSnapshot(store);
    const render = (option) => {
        const { label, value, filename } = option.data;
        return (
            <div className="flex flex-col">
                <span className="font-semibold">{label}</span>
                <div className="font-thin italic flex space-x-10">
                    <span >id: {value}</span>
                    <span >файл: {filename}</span>
                </div>
            </div>
        )
    }

    const onChange = (value) => {
        store.setDatasetId(value);
    }

    return (

        <Select
            className="w-full"
            placeholder='Выберите датасет'
            showSearch
            options={$store.datasets}
            optionRender={render}
            onChange={onChange}
            value={$store.datasetId}
        />
    )
}



const ComparisonTable = () => {
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const onSelectChange = (newSelectedRowKeys) => {
        setSelectedRowKeys(newSelectedRowKeys);
    };
    const rowSelection = {
        selectedRowKeys,
        onChange: onSelectChange,
    };
    return (
        <div>
            <Table
                size="small"
                columns={columns}
                store={store}
                bordered
                actions={[<CompareButton selected={selectedRowKeys} />, <DatasetSelect />]}
                rowSelection={rowSelection}
            // rowSelection={{}}
            />
        </div>
    )
}

export default ComparisonTable;