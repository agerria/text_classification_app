import { useSnapshot } from "valtio";
import { classificationStore as store } from "../../store";

// CrossValidation.js
// import FoldBlock from './FoldBlock';

// FoldBlock.js

// import FoldCell from './FoldCell';
const FoldCell = ({ id, value, isFirst, isLast }) => {
    const $store = useSnapshot(store);
    const getColor = () => {
        if (value === null) return 'bg-red-500';
        if (Object.keys(value).length === 0) return 'bg-yellow-400';
        return 'bg-green-500';
    };

    const handleClick = () => {
        console.log(value, id);
        store.setVisibleReport(value, id);
    };

    const isActive = id == $store.activeFoldId;

    return (
        <button
            onClick={handleClick}
            className={`w-12 h-6 ${getColor()} ${isFirst ? 'rounded-l-lg' : ''} ${isLast ? 'rounded-r-lg' : ''
                } transition-opacity hover:opacity-80 ${isActive ? 'border-2 border-black' : ''}`}
        />
    );
};

// export default FoldCell;

const FoldBlock = ({ title, data, row }) => {
    if (!data)
        return (<></>)
    const entries = Object.entries(data).sort(
        (a, b) => parseInt(a[0]) - parseInt(b[0])
    );

    return (
        <div className="flex items-center">
            <div className="w-48 font-bold">{title}</div>
            <div className="flex gap-x-1">
                {entries.map(([key, value], index) => (
                    <FoldCell
                        key={key}
                        id={`${row}-${index}`}
                        value={value}
                        isFirst={index === 0}
                        isLast={index === entries.length - 1}
                    />
                ))}
            </div>
        </div>
    );
};

const CrossValidation = ({ folds }) => {
    const $store = useSnapshot(store);
    return (
        <div className="p-4 border w-fit my-3 rounded-lg card-div">
            <div className="flex items-center">
                <h2 className="w-48 font-bold text-lg ">Базовый</h2>
                <FoldCell
                    // key={key}
                    id='base'
                    value={$store.baseReport}
                    isFirst={true}
                    isLast={true}
                />
            </div>
            <div className="h-0 border-[1px] my-2 border-primary" />
            <h2 className="text-lg font-bold mb-4">Кросс-валидация</h2>
            <div className="space-y-6">
                <FoldBlock title="Случайный" data={folds?.random} row={1} />
                <FoldBlock title="Стратифицированный" data={folds?.stratified} row={2} />
            </div>
        </div>
    );
};


// export default FoldBlock;

export default CrossValidation