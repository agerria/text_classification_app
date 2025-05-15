import { useEffect, useState } from 'react';
import { Table as AntdTable, Button } from 'antd';
import { FullscreenOutlined, FullscreenExitOutlined } from '@ant-design/icons'
import { Resizable } from 'react-resizable';

import { useSnapshot } from 'valtio';


const ResizableTitle = (props) => {
    const { onResize, width, ...restProps } = props;

    if (!width) {
        return <th {...restProps} />;
    }

    return (
        <Resizable
            width={width}
            height={0}
            handle={
                <span
                    className="react-resizable-handle"
                    onClick={(e) => {
                        e.stopPropagation();
                    }}
                />
            }
            onResize={onResize}
            draggableOpts={{ enableUserSelectHack: false }}
        >
            <th {...restProps} />
        </Resizable>
    );
};




const Table = ({ store, columns, actions, fetch_args, ...props}) => {

    // const {
    //     edit: editAction,
    //     delete: deleteAction,
    //     copy: copyAction,
    // } = rowActions;

    const $store = useSnapshot(store)


    const handlePaginationChange = (nextPage, paginate) => {
        store.paginationChange(nextPage, paginate, fetch_args)
    };

    const pagination = {
        position: ['bottomLeft'],
        pageSize: $store.limit,
        current: $store.page,
        total: $store.total,
        showSizeChanger: true,
        showQuickJumper: true,
        pageSizeOptions: $store.paginateOptions,
        showTotal: (total) => <b>Всего {total}</b>,
        onChange: handlePaginationChange,
    };

    const components = {
        header: {
            cell: ResizableTitle
        }
    }

    // const actionColumns = [
    //     editColumn(editAction),
    //     // deleteColumn(deleteAction),
    //     // copyColumn(copyAction),
    // ].filter(x => x)

    // const columns = [
    //     ...actionColumns,
    //     ...formatColumns($store.settings?.columns || [], store)
    // ]

    useEffect(() => {
        store.fetch(fetch_args)
    }, [fetch_args, store])



    const [isFullScreen, setIsFullScreen] = useState(false);

    const handleFullScreenToggle = () => {
        setIsFullScreen(!isFullScreen);
    };

    const handleKeyDown = (event) => {
        if (event.key === "Escape" && isFullScreen) {
            setIsFullScreen(false);
        }
    };

    useEffect(() => {
        if (isFullScreen) {
            document.addEventListener("keydown", handleKeyDown);
        } else {
            document.removeEventListener("keydown", handleKeyDown);
        }

        return () => {
            document.removeEventListener("keydown", handleKeyDown);
        };
    }, [isFullScreen,]);


    console.log('data', $store.data)

    return (
        <div
            className='h-full card-div'
            style={{
                position: isFullScreen ? "fixed" : "relative",
                top: isFullScreen ? 0 : "auto",
                left: isFullScreen ? 0 : "auto",
                width: isFullScreen ? "100vw" : "auto",
                // height: isFullScreen ? "100vh" : "auto",
                zIndex: isFullScreen ? 1000 : "auto",
                overflow: "auto",
            }}
        >
            <div className=''>
                <div className="flex items-center py-2 px-2">
                    <div className="flex ml-auto flex-shrink-0">
                        <div className='flex flex-row justify-end items-center space-x-3'>
                            {actions}
                            <Button
                                onClick={handleFullScreenToggle}
                                icon={isFullScreen ? <FullscreenExitOutlined /> : <FullscreenOutlined />}
                            />
                        </div>
                    </div>
                </div>
                <div className="flex flex-col">
                    <AntdTable
                        {...props}
                        columns={columns}
                        scroll={
                            isFullScreen
                                ? { y: 'calc(100vh - 12em)' }
                                : { y: 'calc(100vh - 23em)' }
                        }
                        // scroll={{
                        //     y: 'calc(100vh - 18em)'
                        // }}
                        dataSource={$store.data}
                        pagination={pagination}
                        loading={$store.loading}
                        components={components}
                        rowClassName={(_, i) => Boolean(i % 2) && "bg-gray-100"}
                    />
                </div>
            </div>
        </div>
    );
};

export default Table;
