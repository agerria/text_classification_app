import { proxy } from "valtio";

class FabricStore {
    schema = {
        "translator": [
            {
                "value": "key1",
                "label": "CSV",
                "args": {
                    // "lang": {"value": null, "title": "Язык", "type": "string"},
                    "url": {"value": null, "title": "Адрес", "type": "string"}
                }
            },
            {
                "value": "key2",
                "label": "Trans 2",
                "args": {
                    "accuracy": {"value": null, "title": "Точность", "type": "number"},
                    "accuracy2": {"value": null, "title": "Точность2", "type": "number"},
                    "accuracy3": {"value": null, "title": "Точность2", "type": "number"},
                    "accuracy4": {"value": null, "title": "Точность2", "type": "number"},
                    "accuracy5": {"value": null, "title": "Точность2", "type": "number"},
                    "accuracy6": {"value": null, "title": "Точность2", "type": "number"},
                }
            }
        ],
        "vectorizator": [
            {
                "value": "key3",
                "label": "TF-IDF",
                // "args": {
                //     "dimension": {"value": null, "title": "Размерность", "type": "number"}
                // }
            },
            {
                "value": "key4",
                "label": "Vec 2",
                "args": {
                    "method": {"value": null, "title": "Метод", "type": "string"}
                }
            }
        ],
        "classifier": [
            {
                "value": "key5",
                "label": "KNN",
                "args": {
                    "threshold": {"value": null, "title": "Количество соседей", "type": "number"}
                }
            },
            {
                "value": "key6",
                "label": "Class 2",
                "args": {
                    "algorithm": {"value": null, "title": "Алгоритм", "type": "string"}
                }
            }
        ],
        "reporter": [
            {
                "value": "key7",
                "label": "Sklearn отчёт классификации",
                // "args": {
                //     "metric": {"value": null, "title": "Метрика", "type": "string"}
                // }
            },
            {
                "value": "key8",
                "label": "Eval 2",
                "args": {
                    "range": {"value": null, "title": "Диапазон", "type": "number"}
                }
            }
        ]
    }
    

    selectors = {
        translator: null,
        vectorizator: null,
        classifier: null,
        reporter: null,
    }

    setSelectorValue(field, value) {
        this.selectors[field] = value;
    }

    setSelectorArg(field, argKey, value) {
        const prev = this.selectors[field]?.args?.[argKey] || {};
        
        // Создаём новый объект args, чтобы изменения отслеживались
        this.selectors[field] = {
            ...this.selectors[field],
            args: {
                ...this.selectors[field]?.args,
                [argKey]: {
                    ...prev,
                    value: value,
                },
            },
        };
    }
    
}

export const fabricStore = proxy(new FabricStore())