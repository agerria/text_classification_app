import { proxy } from 'valtio';
import { BaseTableStore } from '../../Table/store';

class DatasetsTableStore extends BaseTableStore {
    url = `${process.env.REACT_APP_SERVER_URL}/datasets/table`
}

export const datasetsTableStore = proxy(new DatasetsTableStore());