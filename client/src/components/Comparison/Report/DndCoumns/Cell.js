import FoldCell from "./FoldCell";

import { COMPARE_TYPES } from "../consts";

const COMPARE_FUNC = {
    [COMPARE_TYPES.LESS]: (a, b) => a < b,
    [COMPARE_TYPES.GREATER]: (a, b) => a > b,
};




const formatValue = (value, dimension) => {
    if (value === null)
        return 
    if (typeof value == 'number')
        return value.toFixed((dimension == 'с') ? 1 : 3);
    return value;
}

const ComparisonResult = ({ value, compareType, referenceValue }) => {
    if (typeof value !== 'number' || typeof referenceValue !== 'number') return null;

    const diff = value - referenceValue;
    const percentage = ((diff / referenceValue) * 100).toFixed(1);
    const isBetter = COMPARE_FUNC[compareType](value, referenceValue);

    return (
        <span className={`text-xs ml-2 ${isBetter ? 'text-green-600' : 'text-red-600'}`}>
            {diff > 0 ? '+' : ''}{percentage}%
        </span>
    );
};


const ColumnCell = ({ value,  dimension, compareType, valueType, referenceValue, showComparison, bold=false }) => {
    if( valueType === 'fold') {
        return (<FoldCell value={value} compareType={compareType} referenceValue={referenceValue} showComparison={showComparison}/>) 
    }

    return (
        <div className={`flex justify-between w-full ${bold ? 'font-bold' : ''}`}>
            <span>
                {formatValue(value, dimension) || '-'}
                {dimension && <span className="ml-1 text-gray-500 italic">{dimension}</span>}
            </span>
            {showComparison && (
                <ComparisonResult
                    value={value}
                    compareType={compareType}
                    referenceValue={referenceValue}
                />
            )}
        </div>
    )
}

export default ColumnCell;