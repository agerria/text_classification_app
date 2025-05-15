import { proxy } from 'valtio';
import api from '../../../../api';

export const to_vl = (str) => {
    return {
        label: str,
        value: str,
    }
}

export const to_vls = (list) => {
    if(!list)
        return []
    return  list.map((s) => to_vl(s))
}

export const separators = [
    {
        label: ';',
        value: ';',
    },
    {
        label: ',',
        value: ',',
    },
    {
        label: '\\t',
        value: '\t',
    },
]

class AddDatasetStore {
    BASE_URL = `${process.env.REACT_APP_SERVER_URL}/upload`

    name = null;
    description = null;

    file = null;
    files = [];

    separator = ';';
    headers = [];

    classHeader = null;
    dataHeader = null;

    setName(value) {
        this.name = value;
    }

    setDescription(value) {
        this.description = value;
    }

    setSeparator(value) {
        this.separator = value;
    }
    setFile(value) {
        this.file = value;
    }

    setClassHeader(value) {
        this.classHeader = value;
    }
    setDataHeader(value) {
        this.dataHeader = value;
    }

    async fetchFiles() {
        try {
            const data = await api.get(`${this.BASE_URL}/list/`).json();
            this.files = data;
        } catch (error) {
            console.log('error', error);
        }
    }

    async fetchHeaders() {
        if(!this.file)
            return;

        try {
            const data = await api.get(
                `${this.BASE_URL}/headers/?filename=${this.file}&separator=${this.separator}`
            ).json();
            this.headers = to_vls(data.headers);
            this.classHeader = null;
            this.dataHeader = null;
        } catch (error) {
            console.log('error', error);
        }
    }


    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        try {
            const response = await api.post(`${this.BASE_URL}/`, {
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                this.setFile(data.value);
                this.fetchHeaders()
                // message.success('Файл успешно загружен!');
                return null;
            } else {
                return `Ошибка загрузки файла: ${response.statusText}`;
            }
        } catch (error) {
            return `Произошла ошибка: ${error.message}`;
        }
    }

    async addDataset() {
        try {
            const body = {
                name: this.name,
                file: this.file,
                class_header: this.classHeader,
                data_header: this.dataHeader,
                separator: this.separator,
                description: this.description,
            };
            await api.post(`${this.BASE_URL}/add/`, {
                json: body
            });
            return null;
        } catch (error) {
            return `Произошла ошибка: ${error.message}`;
        }
    }
}

export const addDatasetStore = proxy(new AddDatasetStore());
