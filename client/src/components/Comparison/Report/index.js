import { useEffect, useState, useMemo } from "react";
import { useSearchParams } from "react-router-dom";
import { comparisonReportStore as store } from "./store";

import DndColumns from './DndCoumns';
import IndicatorsColumn from './IncidatorsColum';
import { useSnapshot } from "valtio";


const ComparisonReport = () => {
    const [expandedKeys, setExpandedKeys] = useState([]);
    const [searchParams, setSearchParams] = useSearchParams()
    const hashString = searchParams?.get('hashs') || '';
    const hashs = useMemo(
        () => hashString.split(','),
        [hashString]
    );

    useEffect(() => {
        store.fetchHashsinfo(hashs)
    }, [hashs])

    
    return (
        <div className="flex w-full bg-white rounded-lg h-[calc(100vh-9em)] overflow-y-auto overflow-x-hidden border">
            <IndicatorsColumn expandedKeys={expandedKeys} setExpandedKeys={setExpandedKeys} />
            <DndColumns expandedKeys={expandedKeys} />

        </div>
    );
};

export default ComparisonReport;