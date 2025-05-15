import { proxy } from 'valtio';
import { BaseTableStore } from '../../Table/store';

import api from '../../../api';

class ComparisonTableStore extends BaseTableStore {
    url = `${process.env.REACT_APP_SERVER_URL}/comparison/table`

    datasets = []
    async fetchDatasets() {
        const data = await api.get(`${process.env.REACT_APP_SERVER_URL}/classification/datasets/`).json()

        this.datasets = data
    }
}

export const comparisonTableStore = proxy(new ComparisonTableStore());