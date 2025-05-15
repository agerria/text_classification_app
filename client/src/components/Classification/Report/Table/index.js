import { Table, Tag } from 'antd';
import { useEffect } from 'react';

import { useSnapshot } from 'valtio';
import { datasetInfoStore } from '../../../Datasets/Info/store';

const ClassificationReportTable = ({ report, datasetId }) => {
    const $datasetInfoStore = useSnapshot(datasetInfoStore);

    useEffect(() => {
        if(datasetId)
            datasetInfoStore.fetch(datasetId);
    }, [datasetId])

    if(!report || !$datasetInfoStore.class_colors)
        return (<></>)

    console.log($datasetInfoStore.class_colors)

    // Подготовка данных для отображения в таблице
    const classes = Object.keys(report).filter((key) => key !== 'accuracy' && key !== 'macro avg' && key !== 'weighted avg');

    const dataSource = classes.map((className) => {
        const { precision, recall, f1score, support } = report[className]; // Используем правильный ключ f1score
        return {
            key: className,
            className,
            precision: precision ? precision.toFixed(3) : '-',
            recall: recall ? recall.toFixed(3) : '-',
            f1Score: f1score ? f1score.toFixed(3) : '-', // Теперь f1score
            support: support !== undefined ? support : '-',
        };
    });

    // Добавляем строки для accuracy, macro avg и weighted avg
    const additionalData = [
        {
            key: 'accuracy',
            className: 'Точность',
            precision: report.accuracy ? report.accuracy.toFixed(3) : '-',
            recall: '-',
            f1Score: '-',
            support: '-',
        },
        {
            key: 'macro avg',
            className: 'Макро-среднее',
            precision: report['macro avg'].precision ? report['macro avg'].precision.toFixed(3) : '-',
            recall: report['macro avg'].recall ? report['macro avg'].recall.toFixed(3) : '-',
            f1Score: report['macro avg'].f1score ? report['macro avg'].f1score.toFixed(3) : '-', // Теперь f1score
            support: report['macro avg'].support !== undefined ? report['macro avg'].support : '-',
        },
        {
            key: 'weighted avg',
            className: 'Взвешенное среднее',
            precision: report['weighted avg'].precision ? report['weighted avg'].precision.toFixed(3) : '-',
            recall: report['weighted avg'].recall ? report['weighted avg'].recall.toFixed(3) : '-',
            f1Score: report['weighted avg'].f1score ? report['weighted avg'].f1score.toFixed(3) : '-', // Теперь f1score
            support: report['weighted avg'].support !== undefined ? report['weighted avg'].support : '-',
        },
    ];

    const finalDataSource = [...dataSource, ...additionalData];

    // Колонки для таблицы
    const columns = [
        {
            title: 'Класс',
            dataIndex: 'className',
            key: 'className',
            render: (name) => {
                return classes.includes(name) ? (
                    <Tag color={$datasetInfoStore.class_colors[name]}>{name}</Tag>
                ) : (
                    <span className='font-bold'>{name}</span>
                )
                    
            }
        },
        {
            title: 'Точность',
            dataIndex: 'precision',
            key: 'precision',
        },
        {
            title: 'Полнота',
            dataIndex: 'recall',
            key: 'recall',
        },
        {
            title: 'F1-Score',
            dataIndex: 'f1Score',
            key: 'f1Score',
        },
        {
            title: 'Поддержка',
            dataIndex: 'support',
            key: 'support',
        },
    ];

    return (
        <div className="p-2 w-3/4">
            <Table
                dataSource={finalDataSource}
                columns={columns}
                pagination={false}
                size='small'
                tableLayout="auto"
            />
        </div>
    );
};

export default ClassificationReportTable;
