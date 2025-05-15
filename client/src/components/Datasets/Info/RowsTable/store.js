import { proxy } from 'valtio';
import { BaseTableStore } from '../../../Table/store';

class DatasetsRowsTableStore extends BaseTableStore {
    url = ({id}) => `${process.env.REACT_APP_SERVER_URL}/datasets/${id}/table`
}

export const datasetsRowsTableStore = proxy(new DatasetsRowsTableStore());