import { proxy } from 'valtio';
import api from '../../../api';

import { getClassColor } from '../consts';

class DatasetInfoStore {
    url = (id) => (`${process.env.REACT_APP_SERVER_URL}/datasets/${id}`)

    info = {
        id: null,
        name: null,
        description: null,
        file: null,
        separator: null,
        class_header: null,
        data_header: null,
        rows_count: null,
        classes: null,
    }

    class_colors = {}

    fecthing = false;

    async fetch(id) {
        try {
            this.fecthing = true;
            const data = await api.get(this.url(id)).json()
            this.info = data;
            console.log('classes', data.classes)
            this.setClassColors()
            
            this.fecthing = false;
        } catch (error) {
            console.log(error)
            this.fecthing = false;
        }
    }

    setClassColors() {
        const names = this.info.classes.reduce((acc, obj, index) => {
            acc[obj.name] = getClassColor(index);
            return acc;
        }, {});

        this.class_colors = names;
    }

}

export const datasetInfoStore = proxy(new DatasetInfoStore());