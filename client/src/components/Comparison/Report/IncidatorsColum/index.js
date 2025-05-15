import { Fragment, useEffect } from 'react';
import { Link, useNavigate } from "react-router-dom";
import { useSnapshot } from 'valtio';
import { Tag, Button } from 'antd';
import { RightOutlined, DownOutlined, UpOutlined, ExportOutlined } from '@ant-design/icons';

import { INDICATOR_HEIGHT, ROW_HEIGHT } from '../consts';
import { comparisonReportStore as store } from '../store';
import { datasetInfoStore } from '../../../Datasets/Info/store';

const DatasetTag = () => {
    const $store = useSnapshot(store);
    const datasetId = $store.dataset?.id

    useEffect(() => {
        if (datasetId)
            datasetInfoStore.fetch(datasetId);
    }, [datasetId])

    return (
        <div className='flex '>
            <Tag className=' w-fit text-xl font-bold' color='blue'>
                {$store.dataset.title}
            </Tag>
            <Link
                to={`/datasets/${datasetId}`}
                target="_blank"
            >
                <Button
                    icon={<ExportOutlined />}
                    // disabled={!$store.datasetId}
                />
            </Link>
        </div>
    )
}

const IndicatorLabel = (indicator, $datasetInfoStore) => {

    const label = indicator?.label;

    if (!indicator?.isDatasetClass)
        return label


    return (
        <Tag color={$datasetInfoStore.class_colors[label]}>{label}</Tag>
    )
}

const IndicatorsColumn = ({ expandedKeys, setExpandedKeys }) => {
    const $store = useSnapshot(store);
    const $datasetInfoStore = useSnapshot(datasetInfoStore);
    const INDICATORS = $store.indicators;
    console.log('INDICATORS', INDICATORS)

    const toggleExpand = (key) => {
        setExpandedKeys(prev =>
            prev.includes(key)
                ? prev.filter(k => k !== key)
                : [...prev, key]
        );
    };

    const collapseAll = () => {
        setExpandedKeys([])
    }
    const expandAll = () => {
        const collectKeys = (items) => {
            let keys = [];
            items.forEach(item => {
                keys.push(item.key);
                if (item.children && item.children.length > 0) {
                    keys = keys.concat(collectKeys(item.children));
                }
            });
            return keys;
        };
        const allKeys = collectKeys(INDICATORS);
        setExpandedKeys(allKeys);
    }




    const renderIndicator = (indicator, level = 0) => {
        const hasChildren = indicator.children?.length > 0;
        const paddingLeft = `${level * 12}px`;

        return (
            <Fragment key={indicator.key}>
                <div
                    className={`flex items-center px-4 border-b ${ROW_HEIGHT}`}
                    style={{ paddingLeft }}
                >
                    {hasChildren && (
                        <button
                            onClick={() => toggleExpand(indicator.key)}
                            className="w-6 hover:bg-gray-100 rounded text-xs"
                        >
                            {expandedKeys.includes(indicator.key) ? <DownOutlined /> : <RightOutlined />}
                        </button>
                    ) || (
                            <span className='ml-6' />
                        )
                    }
                    {/* <span className={hasChildren ? 'font-bold' : ''}>{indicator.label}</span> */}
                    <span className={hasChildren ? 'font-bold' : ''}>{IndicatorLabel(indicator, $datasetInfoStore)}</span>
                </div>

                {expandedKeys.includes(indicator.key) && indicator.children?.map(child =>
                    renderIndicator(child, level + 1)
                )}
            </Fragment>
        );
    };

    return (
        <div className="w-[370px] border-r">
            <div className={`p-4 border-b ${INDICATOR_HEIGHT} grid grid-rows-[auto_1fr_auto]`}>
                <DatasetTag />
                {/* <div className={`font-semibold `}>Показатели</div> */}
                <div className='text-xl space-x-1 self-end'>
                    <button className='w-6 hover:bg-gray-100 rounded' onClick={expandAll}><DownOutlined /></button>
                    <button className='w-6 hover:bg-gray-100 rounded' onClick={collapseAll}><UpOutlined /></button>
                </div>
            </div>
            <div className="">
                {INDICATORS.map(indicator => renderIndicator(indicator))}
            </div>
        </div>
    );
};

export default IndicatorsColumn;