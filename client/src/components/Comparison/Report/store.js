import { proxy } from "valtio";
import api from "../../../api";

class ComparisonReportStore {
    BASE_URL = `${process.env.REACT_APP_SERVER_URL}/comparison/report`

    hashs = []

    columns = []
    indicators = []

    dataset = {}

    async fetchHashsinfo(hashs) {
        this.hashs = hashs;
        const body = {
            hashs: this.hashs,
        }
        const {columns, indicators} = await api.post(`${this.BASE_URL}/info`, { json: body}).json();
        this.columns = columns;
        this.indicators = indicators;

        this.dataset = columns[0]?.title?.dataset;
    }

    setHashs(hashs) {
        this.hashs = hashs;
    }

    setColumns(newColumns) {
        this.columns = newColumns;
    }


}

export const comparisonReportStore = proxy(new ComparisonReportStore());