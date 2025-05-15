import { useEffect, useContext } from "react";
import { useSnapshot } from "valtio";

import { Descriptions, Table, Tag } from "antd";

import { TitleContext } from "../../TitleContext";

import { datasetInfoStore as store } from "./store";
import DatasetRowsTable from "./RowsTable";

const DatasetDesc = ({ info }) => {
    const labelStyle = {
        width: '160px'
    }

    const title = (<span className="mx-3">Общая информация</span>)

    return (
        <Descriptions className="p-1" bordered column={1} title={title} size="small" labelStyle={labelStyle}>
            <Descriptions.Item label='Название' >           {info.name} </Descriptions.Item>
            <Descriptions.Item label='Имя файла' >          {info.file} </Descriptions.Item>
            <Descriptions.Item label='Разделитель' >        {info.separator} </Descriptions.Item>
            <Descriptions.Item label='Заголовок класса' >   {info.class_header} </Descriptions.Item>
            <Descriptions.Item label='Заголовок данных ' >  {info.data_header} </Descriptions.Item>
            <Descriptions.Item label='Количество строк' >   {info.rows_count} </Descriptions.Item>
            <Descriptions.Item label='Описание' >           {info.description} </Descriptions.Item>
        </Descriptions>
    );
};

const ClassesTable = ({ classes, colors }) => {
    const columns = [
        {
            key: 'name',
            dataIndex: 'name',
            title: 'Класс',
            // width: '3%',
            render: (name) => (
                <Tag color={colors[name]}>{name}</Tag>
            )
        },
        {
            key: 'rows_count',
            dataIndex: 'rows_count',
            title: 'Количество',
            // width: '3%',
        },
        {
            key: 'percent',
            dataIndex: 'percent',
            title: 'Процент',
            // width: '3%',
            render: (x) => {
                const ix = x.toFixed(2);
                return (
                    <div className="w-full h-full align-middle flex items-center">
                        <div className="absolute top-[12px] left-0 h-[20px] rounded-lg bg-blue-400" style={{width: `${ix}%`}}></div>
                        <span className="relative z-10 text-center text-black w-full  flex items-center justify-center">{ix}%</span>
                    </div>
                )
            }
        },
    ]

    return (
        <Table
            columns={columns}
            dataSource={classes}
            size="middle"
            pagination={false}
            className=""
            rowClassName={(_, i) => Boolean(i % 2) && "bg-gray-100"}
        />
    )
}

const DatasetsInfo = ({ id }) => {
    const $store = useSnapshot(store);
    const { setTitle } = useContext(TitleContext);

    useEffect(() => {
        store.fetch(id)
    })

    useEffect(() => {
        setTitle(
            `Датасеты / ${$store.info.name}`
        )    
    }, [$store.info, setTitle])

    return (
        <div className="flex h-full space-x-3">
            <div className="flex flex-col w-1/3 space-y-3 h-full  overflow-y-auto">
                <div className="card-div h-[600px] overflow-y-auto">
                    <DatasetDesc info={$store.info} />
                </div>
                <div className="card-div overflow-y-auto h-full">
                    <ClassesTable classes={$store.info.classes} colors={$store.class_colors}/>
                </div>
            </div>
            <div className="w-2/3">
                <DatasetRowsTable id={id} colors={$store.class_colors}/>
            </div>
        </div>
    )
}

export default DatasetsInfo;