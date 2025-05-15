import { useEffect } from 'react';

import { Button, Modal, Upload, message, Select, Input } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

import { useSnapshot } from 'valtio';
import { addDatasetStore as store, separators } from './store';


import { datasetsTableStore } from "../store";

const Title = () => {
    const $store = useSnapshot(store);
    return (
        <div>
            <div className='flex justify-between pr-4 items-center'>
                <span>Добавление датасета</span>
                <Input
                    placeholder='Название'
                    className='w-[250px]'
                    value={$store.name}
                    onChange={(e) => store.setName(e.target.value)}
                />
            </div>
            <div className='border-[1px] border-grey-200 mt-2 mr-3' />
        </div>
    )
}


const AddModal = ({ open, setOpen }) => {
    const $store = useSnapshot(store);

    const onOk = async () => {
        const error = await store.addDataset()
        if (error) {
            message.error(error)
        } else {
            message.success('Файл успешно загружен!')
            setOpen(false);
            datasetsTableStore.fetch();
        }
    }
    const onCancel = () => {
        setOpen(false);
    }


    useEffect(() => {
        store.fetchFiles()
    }, [])

    const onChangeFile = (file) => {
        store.setFile(file);
        store.fetchHeaders()
    }

    const onChangeSeparator = (separator) => {
        store.setSeparator(separator);
        store.fetchHeaders()
    }


    const handleUpload = async (file) => {
        const error = await store.uploadFile(file);

        if (error) {
            message.error(error)
        } else {
            message.success('Файл успешно загружен!')
            store.fetchFiles();
        }
    };

    const props = {
        accept: '.csv',
        customRequest: ({ file, onSuccess, onError }) => {
            handleUpload(file)

        },
        showUploadList: false,
    };

    console.log('options in Select', $store.files);



    return (
        <Modal
            title={<Title />}
            cancelText='Отменить'
            open={open}
            onOk={onOk}
            onCancel={onCancel}
            centered
            width={550}
            okButtonProps={{
                disabled:
                    !Boolean( $store.name && $store.file && $store.classHeader && $store.dataHeader)
            }}
        >
            <div className='flex flex-col space-y-2 pr-4'>
                <div className='flex justify-between'>
                    <div className='flex justify-between w-[300px]'>
                        <Select
                            options={separators}
                            value={$store.separator}
                            onChange={onChangeSeparator}
                            className='w-70[px]'
                        />
                        <Select
                            placeholder='Имя файла'
                            value={$store.file}
                            options={$store.files || []}
                            onChange={onChangeFile}
                            className='w-[230px]'
                        />
                    </div>
                    <Upload
                        {...props}
                    >
                        <Button icon={<UploadOutlined />}>Загрузить CSV</Button>
                    </Upload>
                </div>
                <div className='flex space-x-3 justify-between'>
                    <Select
                        options={$store.headers}
                        value={$store.classHeader}
                        onChange={(v) => store.setClassHeader(v)}
                        className='w-[300px]'
                    />
                    <span className='mt-1 text-nowrap'>Имя поля для класса</span>
                </div>
                <div className='flex space-x-3 justify-between'>
                    <Select
                        options={$store.headers}
                        value={$store.dataHeader}
                        onChange={(v) => store.setDataHeader(v)}
                        className='w-[300px]'
                    />
                    <span className='mt-1 text-nowrap'>Имя поля для данных</span>
                </div>
                
                <Input.TextArea
                    placeholder='Описание'  
                    rows={3}
                    value={$store.description}
                    onChange={(e) => store.setDescription(e.target.value)}
                />
            </div>

        </Modal>
    )
}

export default AddModal;