import { Children, useEffect, useState } from "react";
import { useSnapshot } from "valtio";
import { Link, useNavigate } from "react-router-dom";

import { Button, Select, Splitter, Input, InputNumber, Slider, Spin, Popconfirm } from "antd";
import { ExportOutlined, PercentageOutlined, DeleteOutlined } from '@ant-design/icons';

import { classificationStore as store } from "./store";
import ClassificationReportTable from "./Report/Table";
import ClassificationReportTime from "./Report/Times";
import CrossValidation from "./Report/CrossValidation";

const Card = ({ children, title, className }) => {
    return (
        <div className="card-div flex flex-col py-1 px-3 space-y-2">
            <span className="font-bold text-lg mx-2">{title}</span>
            <div className="h-[2px] bg-slate-700 w-1/4" />
            <div className={className}>
                {children}
            </div>
        </div>
    )
}

const DatasetSelect = ({ $store }) => {
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
        <Card title={'Датасет'} className="flex space-x-2">
            <Select
                className="w-full"
                placeholder='Выберите датасет'
                showSearch
                options={$store.datasets}
                optionRender={render}
                onChange={onChange}
                value={$store.datasetId}
                disabled={$store.isViewOnly()}
            />
            <Link
                to={`/datasets/${$store.datasetId}`}
                target="_blank"
            >
                <Button
                    icon={<ExportOutlined />}
                    disabled={!$store.datasetId}
                />
            </Link>
        </Card>
    )
}



const ArgDiv = ({ label, children }) => (
    <div className="flex justify-between items-center px-3">
        <label>{label}</label>
        <div className="w-1/2">
            {children}
        </div>
    </div>
);

const ArgInputField = ({ label, value, onChange, ...props  }) => (
    <ArgDiv label={label}>
        <Input className="w-full" value={value} onChange={(e) => onChange(e.target.value)} {...props}/>
    </ArgDiv>
);

const ArgInputNumberField = ({ label, value, onChange, step = 1, ...props  }) => (
    <ArgDiv label={label}>
        <InputNumber className="w-full" value={value} onChange={onChange} step={step} {...props}/>
    </ArgDiv>
);

const ArgSelectField = ({ label, value, onChange, options, multiple = false, ...props }) => (
    <ArgDiv label={label}>
        <Select
            className="w-full"
            mode={multiple ? "multiple" : undefined}
            value={value}
            onChange={onChange}
            options={options?.map(v => ({ value: v, label: v }))}
            {...props}
        />
    </ArgDiv>
);

const scheme = {
    str: ArgInputField,
    int: ArgInputNumberField,
    float: (props) => <ArgInputNumberField {...props} step={0.01} />,
    select: ArgSelectField,
    multiselect: (props) => <ArgSelectField {...props} multiple />
};


const VectorizerSelect = ({ $store }) => {
    const onChange = (value, obj) => {
        store.setVectorizer(obj)
    }

    console.log('value={$store.vectorizer}', $store.vectorizer)

    return (
        <Card title='Векторизатор' className=' space-y-2'>
            <Select
                placeholder='Выберите векторизатор'
                className="w-full"
                options={$store.vectorizers}
                value={$store.vectorizer}
                onChange={onChange}
                disabled={$store.isViewOnly()}
            />
            {$store.vectorizer &&
                <div>
                    {$store.vectorizer.args.map(arg => {
                        const Component = scheme[arg.type];
                        return (
                            <Component
                                key={arg.key}
                                label={arg.label}
                                value={$store.vectorizerArgs[arg.key]}
                                onChange={(value) => store.setVectorizerArg(arg.key, value)}
                                options={arg.variants}
                                disabled={$store.isViewOnly()}
                            />
                        );
                    })}
                </div>
            }
        </Card>
    )
}



const ClassifierSelect = ({ $store }) => {
    const onChange = (value, obj) => {
        console.log(value, obj)
        // store.setVectorizer(value)
        store.setClassifier(obj)
    }

    return (
        <Card title='Классификатор' className=' space-y-2'>
            <Select
                placeholder='Выберите классификатор'
                className="w-full"
                options={$store.classifiers}
                value={$store.classifier}
                onChange={onChange}
                disabled={$store.isViewOnly()}
            />
            {$store.classifier &&
                <div className="space-y-1">
                    {$store.classifier.args.map(arg => {
                        const Component = scheme[arg.type];
                        console.log('arg', arg, Component)
                        return (
                            // <>{arg.type}</>
                            <Component
                                key={arg.key}
                                label={arg.label}
                                value={$store.classifierArgs[arg.key]}
                                onChange={(value) => store.setClassifierArg(arg.key, value)}
                                options={arg.variants}
                                disabled={$store.isViewOnly()}
                            />
                        );
                    })}
                </div>
            }
        </Card>
    )
}


const TestSize = ({ $store }) => {
    return (
        <Card title={'Размер тестовой выборки'} className='flex space-x-2'>
            <Slider
                min={0}
                max={100}
                onChange={(v) => store.setTestSize(v)}
                value={$store.testSize}
                reverse
                className="w-full"
                disabled={$store.isViewOnly()}
            />
            <Input
                className="w-[75px]"
                onChange={(e) => store.setTestSize(e.target.value)}
                value={$store.testSize}
                min={0}
                max={100}
                suffix={<PercentageOutlined />}
                disabled={$store.isViewOnly()}
            />
        </Card>
    )
}


const DeleteButtonWithConfirmation = ({disabled}) => {
    const onDelete = () => {
        store.removeHashed();

    }

    return (
      <Popconfirm
        title={"Вы уверены, что хотите удалить эту запись?"}
        description="Это действие нельзя будет отменить."
        onConfirm={onDelete}
        okText="Удалить"
        cancelText="Отмена"
        okButtonProps={{ danger: true }}
        // icon={<DeleteOutlined style={{ color: '#ff4d4f' }} />}
      >
        <Button
          type="primary"
          danger
          icon={<DeleteOutlined />}
          disabled={disabled}
        >
          {/* Удалить */}
        </Button>
      </Popconfirm>
    );
  };


const Classification = ({hash}) => {
    const $store = useSnapshot(store);

    const navigate = useNavigate();

    useEffect(() => {
        if(hash)
            store.fetchHashed(hash);
    }, [hash])

    useEffect(() => {
        if($store.hash === null && hash)
            navigate(`/classification`);
    },[hash, $store.hash])


    useEffect(() => {
        store.fetchSchemes();
        store.fetchDatasets();
    }, [store])

    const onRun = async () => {
        const new_hash = await store.runCalculation();
        if(new_hash)
            navigate(`/classification/${new_hash}`);
    }

    return (
        <div>
            <Splitter
                className="w-ful h-full"
            >
                {/* <Spin spinning={$store.calculating} fullscreen/> */}
                <Splitter.Panel defaultSize="30%" className=" mr-1">
                    <div className="flex flex-col h-full space-y-3 border-2 p-2 rounded-lg bg-slate-200">
                        {/* <Input placeholder="Описание" value={$store.description} onChange={(e) => store.setDescription(e.target.value)}/> */}
                        <DatasetSelect $store={$store} />
                        <VectorizerSelect $store={$store} />
                        <ClassifierSelect $store={$store} />
                        <TestSize $store={$store} />
                        <div className="flex justify-between">
                            <DeleteButtonWithConfirmation disabled={!$store.hash}/>
                            <Button
                                style={{ backgroundColor: '#60a5fa' }}
                                // onClick={() => store.runCalculation()}
                                onClick={onRun}
                                disabled={!$store.datasetId || !store.vectorizer || !store.classifier }
                            >
                                Запустить
                            </Button>
                        </div>
                    </div>
                </Splitter.Panel>
                <Splitter.Panel className='h-full ml-1'>
                    <Spin spinning={$store.calculating} fullscreen/>
                    <div className="h-full card-div">
                        <div className="flex justify-between h-[] overflow-y-auto">
                            <ClassificationReportTable report={$store.report?.table} datasetId={$store.datasetId}/>
                            <ClassificationReportTime times={$store.report?.times} />
                        </div>
                    </div>
                </Splitter.Panel>
            </Splitter>
            {$store.folds && <CrossValidation folds={$store.folds}/>}
        </div>
    )
}

export default Classification;