import { useState, Fragment } from 'react';
import { DndContext } from '@dnd-kit/core';
import { restrictToHorizontalAxis } from '@dnd-kit/modifiers';
import { SortableContext, useSortable, horizontalListSortingStrategy } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { useSnapshot } from 'valtio';
import { Spin, Tag } from "antd";


import { comparisonReportStore as store } from '../store';
import ColumnCell from "./Cell";
import { TITLE_HEIGHT, ROW_HEIGHT } from "../consts";

const TitleTag = ({ color, obj }) => {
    const { title, args } = obj;
    const tags = args ? Object.keys(args).map(key => `${key}: ${args[key]}`) : [];

    return (
        <Tag color={color} className="text-sm w-[200px] p-1 flex flex-col justify-between ">
            {title}
            <div className='flex flex-col overflow-x-hidden'>
                {tags &&
                    tags.map((tag, i) =>
                        (<Tag className="text-wrap" key={i}>{tag}</Tag>)
                    )
                }
            </div>
        </Tag>
    )
}

const Card = ({ title }) => {
    return (
        <div className="flex flex-col font-bold  space-y-1 max-h-[150px] overflow-y-auto overflow-x-hidden">
            {/* <TitleTag color='blue' title={title.dataset}/> */}
            <TitleTag color='green' obj={title.vectorizer} />
            <TitleTag color='red' obj={title.classifier} />
        </div>
    )
}



// const ColumnData = ({ column, columns, index, expandedKeys }) => {
//     const $store = useSnapshot(store);
//     const INDICATORS = $store.indicators;
//     const isFirstColumn = index === 0;
//     return (
//         <div className="w-full">
//             {INDICATORS.flatMap(indicator => [
//                 <div key={`${column.hash}-${indicator.key}`} className={`p-2 border-b ${ROW_HEIGHT} flex items-center`}>
//                     <ColumnCell
//                         value={column.indicators[indicator.key]}
//                         dimension={indicator.dimension}
//                         compareType={indicator.compareType}
//                         valueType={indicator.valueType}
//                         referenceValue={columns[0].indicators[indicator.key]}
//                         showComparison={!isFirstColumn}
//                     // bold
//                     />
//                 </div>,
//                 ...(expandedKeys.includes(indicator.key)
//                     ? indicator.children.map(child => (
//                         <div key={`${column.hash}-${child.key}`} className={`p-2 border-b ${ROW_HEIGHT} flex items-center pl-12`}>
//                             <ColumnCell
//                                 value={column.indicators[child.key]}
//                                 dimension={child.dimension}
//                                 compareType={child.compareType}
//                                 valueType={child.valueType}
//                                 referenceValue={columns[0].indicators[child.key]}
//                                 showComparison={!isFirstColumn}
//                             />
//                         </div>
//                     ))
//                     : [])
//             ])}
//         </div>
//     );
// };

const ColumnData = ({ column, columns, index, expandedKeys }) => {
    const $store = useSnapshot(store);
    const INDICATORS = $store.indicators;

    const renderCell = (indicator, level = 0) => {
        const hasChildren = indicator.children?.length > 0;
        const paddingLeft = `${level * 12 + 12}px`; // +16px для базового отступа

        return (
            <Fragment key={`${column.hash}-${indicator.key}`}>
                <div
                    className={`p-2 border-b ${ROW_HEIGHT} flex items-center`}
                    style={{ paddingLeft }}
                >
                    <ColumnCell
                        value={column.indicators[indicator.key]}
                        dimension={indicator.dimension}
                        compareType={indicator.compareType}
                        referenceValue={columns[0].indicators[indicator.key]}
                        valueType={indicator.valueType}
                        showComparison={index !== 0}
                    />
                </div>

                {expandedKeys.includes(indicator.key) &&
                    indicator.children?.map(child =>
                        renderCell(child, level + 1)
                    )}
            </Fragment>
        );
    };

    return (
        <div className="">
            {INDICATORS.map(indicator => renderCell(indicator))}
        </div>
    );
};


const SortableColumn = ({ id, title }) => {
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({ id });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition: transition || 'transform 150ms ease',
        zIndex: isDragging ? 1000 : 1,
        position: 'relative',
    };

    return (
        <div
            ref={setNodeRef}
            style={style}
            className="bg-gray-50 p-1 rounded-lg shadow-sm border"
        >
            <div className="flex items-center gap-2">
                <button
                    {...attributes}
                    {...listeners}
                    className="cursor-grab active:cursor-grabbing text-gray-400 hover:text-gray-600"
                >
                    ⠿
                </button>
                <Card title={title} />
            </div>
            {isDragging && <div className="absolute inset-0 bg-white opacity-50" />}
        </div>
    );
};


const DndColumns = ({ expandedKeys }) => {
    const $store = useSnapshot(store);

    const handleDragEnd = ({ active, over }) => {
        if (!over) return;

        const oldIndex = $store.columns.findIndex(c => c.hash === active.id);
        const newIndex = $store.columns.findIndex(c => c.hash === over.id);

        if (oldIndex !== newIndex) {
            const newColumns = [...$store.columns];
            const [removed] = newColumns.splice(oldIndex, 1);
            newColumns.splice(newIndex, 0, removed);
            store.setColumns(newColumns);
        }
    };

    return (
        <DndContext
            onDragEnd={handleDragEnd}
            modifiers={[restrictToHorizontalAxis]}
        >
            <SortableContext
                items={$store.columns.map(c => c.hash)}
                strategy={horizontalListSortingStrategy}
            >
                <div className="flex gap-4 p-4 w-full  overflow-x-auto overflow-y-hidden h-fit">
                    {$store.columns.map((column, index) => (
                        <div
                            key={column.hash}
                            className="border rounded-lg bg-white shadow-sm h-fit"
                        >
                            <div className={`p-2  border-b ${TITLE_HEIGHT} w-[250px] `}>
                                <SortableColumn id={column.hash} title={column.title} />
                            </div>
                            <ColumnData
                                column={column}
                                columns={$store.columns}
                                index={index}
                                expandedKeys={expandedKeys}
                            />
                        </div>
                    ))}
                </div>
            </SortableContext>
        </DndContext>
    )
}

export default DndColumns;