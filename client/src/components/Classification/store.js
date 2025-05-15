import { proxy } from "valtio";

import api from "../../api";

const getScheme = (schemes, value) => {
    return schemes.find(scheme => scheme.value === value);
}

class ClassificationStore {
    BASE_URL = `${process.env.REACT_APP_SERVER_URL}/classification`

    datasets = []
    classifiers = []
    vectorizers = []

    //-----form------
    description = null;
    datasetId = null;

    vectorizer = null;
    classifier = null;

    vectorizerArgs = {};
    classifierArgs = {};

    testSize = 20
    //---------------

    //----reports----
    hash = '';
    calculating = false;

    report = {};
    baseReport = {};
    folds = {};
    activeFoldId = 'base';

    async fetchSchemes() {
        const data = await api.get(`${this.BASE_URL}/schemes/`).json()

        this.classifiers = data.classifiers
        this.vectorizers = data.vectorizers
    }

    async fetchDatasets() {
        const data = await api.get(`${this.BASE_URL}/datasets/`).json()

        this.datasets = data
    }


    async runCalculation() {
        try {
            this.calculating = true;
            const body = {
                dataset_id: this.datasetId,
                vectorizer: this.vectorizer.value,
                classifier: this.classifier.value,
                vectorizer_args: this.vectorizerArgs,
                classifier_args: this.classifierArgs,
                test_size: this.testSize / 100,
            }

            const data = await api.post(`${this.BASE_URL}/calculate/`, { json: body }).json()
            // this.report = data;
            return data
        } catch (error) {
            console.log(error)
            return `Произошла ошибка: ${error.message}`;
        } finally {
            this.calculating = false;
        }
    }

    setDescription(value) {
        this.description = value;
    }

    setDatasetId(value) {
        this.datasetId = value;
    }

    setVectorizer(obj) {
        console.log('setVectorizer', obj)
        this.vectorizer = obj;
        this.vectorizerArgs = obj.args.reduce((result, arg) => {
            result[arg.key] = arg.default;
            return result;
        }, {});
    }

    setVectorizerArg(key, value) {
        this.vectorizerArgs[key] = value
    }

    setClassifier(obj) {
        this.classifier = obj;
        this.classifierArgs = obj.args.reduce((result, arg) => {
            result[arg.key] = arg.default;
            return result;
        }, {});

        console.log(this.classifierArgs)
    }

    setClassifierArg(key, value) {
        this.classifierArgs[key] = value
    }

    setTestSize(value) {
        this.testSize = value
    }

    async fetchHashed(hash) {
        if(!hash)
            return;

        await this.fetchDatasets()
        await this.fetchSchemes()
        
        const data = await api.get(`${this.BASE_URL}/calculate/${hash}`).json()
        if (data === null) {
            this.hash = null;
            return;
        }
        
        this.baseReport = data.report;
        this.report = this.baseReport;
        this.folds = data.folds
        
        const settings = data.settings;
        
        this.description = data.description;
        this.datasetId = settings.dataset_id;
        
        this.vectorizer = getScheme(this.vectorizers, settings.vectorizer)
        this.vectorizerArgs = settings.vectorizer_args
        
        this.classifier = getScheme(this.classifiers, settings.classifier)
        this.classifierArgs = settings.classifier_args
        
        this.testSize = settings.test_size * 100
        
        this.setHash(hash);
    }

    setHash(hash) {
        this.hash = hash;
        if(!hash)
            this.clear()
    }

    isViewOnly() {
        return !!this.hash;
    }

    setVisibleReport(report, id) {
        this.report = report
        this.activeFoldId = id
    }

    async removeHashed() {
        if (!this.hash)
            return;

        await api.delete(`${this.BASE_URL}/calculate/${this.hash}`);
        this.setHash(null)
    }

    clear() {
        this.datasets = [];
        this.classifiers = [];
        this.vectorizers = [];

        //-----form------
        this.description = null;
        this.datasetId = null;

        this.vectorizer = null;
        this.classifier = null;

        this.vectorizerArgs = {};
        this.classifierArgs = {};

        this.testSize = 20
        //---------------

        //----reports----
        this.hash = null;
        this.calculating = false;

        this.report = {};
        this.baseReport = {};
        this.folds = {};
        this.activeFoldId = 'base';
    }
}

export const classificationStore = proxy(new ClassificationStore())

