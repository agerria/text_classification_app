import { Table } from 'antd';

const ClassificationReportTime = ({ times }) => {
    if (!times)
        return (<></>)

    const dataSource = times.map(([stage, time], index) => ({
        key: index,
        stage,
        time: time.toFixed(4), // Форматируем время с 4 знаками после запятой
    }));

    // Определение колонок
    const columns = [
        {
            title: 'Этап',
            dataIndex: 'stage',
            key: 'stage',
        },
        {
            title: 'Время (сек.)',
            dataIndex: 'time',
            key: 'time',
        },
    ];

    return (
        <div className="p-2 w-1/4">
            <Table
                dataSource={dataSource}
                columns={columns}
                pagination={false}
                bordered
                size='small'
                rowClassName={(record) => (record.stage == 'Общее время') && 'font-bold' }
            />
        </div>
    );
}

export default ClassificationReportTime;
