from pydantic import BaseModel
from typing import List, Dict
from enum import Enum
import re

from app.models import Classification
from app.logic.fold.consts import FoldType


class COMPARE_TYPES(str, Enum):
    GREATER = 'greater'
    LESS = 'less'

    FOLD_TTEST = 'ttest'
    FOLD_WILCOXON = 'wilcoxon'
    FOLD_BOOTSTRAP = 'bootstrap'

    PREDICTS = 'predicts'

    EMPTY = ''


class VALUE_TYPE(str, Enum):
    NUMBER = 'number'
    FOLD = 'fold'
    EMPTY = ''


class SIndicator(BaseModel):
    key: str
    label: str
    compareType: str
    valueType: VALUE_TYPE = VALUE_TYPE.NUMBER
    dimension: str = ''
    isDatasetClass: bool = False
    children: List['SIndicator'] = []


class ClassificationReport:
    def __init__(self, clsf: Classification):
        self.clsf = clsf
        self.report = clsf.report

    def get_data(self) -> dict:
        return {}

    def get_indicators(self) -> List[SIndicator]:
        return []


class BaseReport(ClassificationReport):
    METRIC_LABELS = {
        'accuracy': 'Точность',
        'recall': 'Полнота',
        'f1score': 'F1-мера',
        'precision': 'Точность (прецизия)',
        'macro_avg': 'Макро-среднее',
        'weighted_avg': 'Взвешенное среднее'
    }

    TIME_KEY_MAP = {
        'Общее время': 'total_time',
        'Загрузка данных': 'load_data',
        'Векторизация': 'vectorization',
        'Разбиение': 'splitting',
        'Обучение': 'training',
        'Классификация': 'classification'
    }

    def generate_key(self, label: str) -> str:
        # Кастомные ключи для времени
        if label in self.TIME_KEY_MAP:
            return self.TIME_KEY_MAP[label]

        # Общая транслитерация для остальных
        translit_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
        }

        key = label.lower().strip()
        key = ''.join([translit_map.get(c, c) for c in key])
        key = re.sub(r'[^a-z0-9]+', '_', key)
        return key

    def _process_table(self) -> List[SIndicator]:
        indicators = []
        table = self.report.get('table', {})

        # Accuracy
        if 'accuracy' in table:
            indicators.append(SIndicator(
                key='accuracy',
                label=self.METRIC_LABELS['accuracy'],
                compareType=COMPARE_TYPES.GREATER,
                dimension=''
            ))

        # Метрики
        for metric in ['recall', 'f1score', 'precision']:
            children = []

            # Macro Avg
            if 'macro avg' in table and metric in table['macro avg']:
                children.append(SIndicator(
                    key=f'macro_avg_{metric}',
                    label=self.METRIC_LABELS['macro_avg'],
                    compareType=COMPARE_TYPES.GREATER,
                    dimension=''
                ))

            # Weighted Avg
            if 'weighted avg' in table and metric in table['weighted avg']:
                children.append(SIndicator(
                    key=f'weighted_avg_{metric}',
                    label=self.METRIC_LABELS['weighted_avg'],
                    compareType=COMPARE_TYPES.GREATER,
                    dimension=''
                ))

            # Динамические классы
            dynamic_classes = [k for k in table if k not in
                               ['accuracy', 'macro avg', 'weighted avg']]
            for cls_name in dynamic_classes:
                cls_key = self.generate_key(cls_name)
                children.append(SIndicator(
                    key=f'{cls_key}_{metric}',
                    label=cls_name,
                    compareType=COMPARE_TYPES.GREATER,
                    dimension='',
                    isDatasetClass=True
                ))

            if children:
                indicators.append(SIndicator(
                    key=metric,
                    label=self.METRIC_LABELS[metric],
                    compareType=COMPARE_TYPES.GREATER,
                    dimension='',
                    children=children
                ))

        return indicators

    def _process_times(self) -> List[SIndicator]:
        times = self.report.get('times', [])
        children = []

        for time_item in times:
            label, value = time_item
            if label == 'Общее время':
                continue

            children.append(SIndicator(
                key=self.generate_key(label),
                label=label,
                compareType=COMPARE_TYPES.LESS,
                dimension='с'
            ))

        return [SIndicator(
            key='total_time',
            label='Общее время',
            compareType=COMPARE_TYPES.LESS,
            dimension='с',
            children=children
        )]

    def get_indicators(self) -> List[SIndicator]:
        indicators = []
        indicators.extend(self._process_times())
        indicators.extend(self._process_table())

        root = SIndicator(
            key='root',
            label='Основная выборка',
            compareType=COMPARE_TYPES.EMPTY,
            children=indicators
        )
        return [root]

        return indicators

    def get_data(self) -> Dict[str, float]:
        if not self.report:
            return {}
        data = {}
        table = self.report.get('table', {})
        times = self.report.get('times', [])

        # Обработка времени
        for label, value in times:
            key = self.generate_key(label)
            data[key] = round(value, 3)

        # Accuracy
        if 'accuracy' in table:
            data['accuracy'] = table['accuracy']

        # Метрики
        for metric in ['recall', 'f1score', 'precision']:
            # Macro Avg
            if 'macro avg' in table and metric in table['macro avg']:
                data[f'macro_avg_{metric}'] = table['macro avg'][metric]

            # Weighted Avg
            if 'weighted avg' in table and metric in table['weighted avg']:
                data[f'weighted_avg_{metric}'] = table['weighted avg'][metric]

            # Динамические классы
            dynamic_classes = [k for k in table if k not in
                               ['accuracy', 'macro avg', 'weighted avg']]
            for cls_name in dynamic_classes:
                cls_key = self.generate_key(cls_name)
                if metric in table[cls_name]:
                    data[f'{cls_key}_{metric}'] = table[cls_name][metric]

        return data


class FoldReport(ClassificationReport):
    FILDS = {
        'fold-wa-f1': ['table', 'weighted avg', 'f1score'],
        'fold-wa-rc': ['table', 'weighted avg', 'recall'],
        'fold-wa-pr': ['table', 'weighted avg', 'precision'],

        'fold-ma-f1': ['table', 'macro avg', 'f1score'],
        'fold-ma-rc': ['table', 'macro avg', 'recall'],
        'fold-ma-pr': ['table', 'macro avg', 'precision'],
    }

    SCOPE_LABELS = {
        'fold-wa-f1': 'f1 (Взвешенное среднее)',
        'fold-wa-rc': 'Полнота (Взвешенное среднее)',
        'fold-wa-pr': 'Точность (Взвешенное среднее)',

        'fold-ma-f1': 'f1 (Макро среднее)',
        'fold-ma-rc': 'Полнота (Макро среднее)',
        'fold-ma-pr': 'Точность (Макро среднее)',
    }

    TEST_LABELS = {
        'ttest': ['Парный t-тест', COMPARE_TYPES.FOLD_TTEST],
        'wilcoxon': ['Тест Уилкоксона', COMPARE_TYPES.FOLD_WILCOXON],
        # 'bootstrap': ['Бутстреп-метод', COMPARE_TYPES.FOLD_BOOTSTRAP],
    }

    FOLD_LABELS = {
        FoldType.random: 'Случайный',
        FoldType.stratified: 'Стратифицированный',
    }

    def __init__(self, clsf):
        super().__init__(clsf)

        self.folds = {
            ft: []
            for ft in FoldType
        }

        for fold in clsf.folds:
            self.folds[fold.fold_type].append(fold.report)

    def get_indicators(self):
        data = []
        for test in self.TEST_LABELS.keys():
            scope_children = []
            for key in self.FILDS.keys():
                children = [
                    SIndicator(
                        key=f'{key}-{test}-{ft.value}',
                        label=self.FOLD_LABELS[ft],
                        compareType=self.TEST_LABELS[test][1],
                        valueType=VALUE_TYPE.FOLD
                    )
                    for ft in FoldType
                ]
                scope_children.append(
                    SIndicator(
                        key=key,
                        label=self.SCOPE_LABELS[key],
                        compareType=COMPARE_TYPES.EMPTY,
                        valueType=VALUE_TYPE.EMPTY,
                        children=children
                    )
                )

            data.append(
                SIndicator(
                    key=f'{key}-{test}',
                    label=self.TEST_LABELS[test][0],
                    compareType=COMPARE_TYPES.EMPTY,
                    valueType=VALUE_TYPE.EMPTY,
                    children=scope_children
                )
            )
        return data

    def get_data(self):
        # return {}
        data = {}
        for prefix, fields in self.FILDS.items():
            for test in self.TEST_LABELS.keys():
                for ft in FoldType:
                    values = []
                    key = f'{prefix}-{test}-{ft.value}'
                    for fold in self.folds[ft]:
                        values.append(self._get_fold_value(fold, fields))

                    data[key] = values

        return data

    def _get_fold_value(self, fold, fields):
        v = fold or {}
        for field in fields:
            v = (v.get(field) or {})
        if v == {}:
            return None
        return v


class PredictReport(ClassificationReport):
    KEY = 'predicts'
    LABEL = 'Тест МакНемара'
    FOLD_LABELS = {
        FoldType.random: 'Случайный',
        FoldType.stratified: 'Стратифицированный',
    }

    def __init__(self, clsf):
        super().__init__(clsf)

        self.folds = {
            ft: None
            for ft in FoldType
        }

        for fold in clsf.folds:
            if fold.fold_num == 1:
                self.folds[fold.fold_type] = fold.report['predicts'] if fold.report else {}

    def get_data(self):
        data = {
            f'{self.KEY}-{ft.value}': self.folds[ft]
            for ft in FoldType
        }
        return data

    def get_indicators(self):
        children = [
            SIndicator(
                key=f'{self.KEY}-{ft.value}',
                label=self.FOLD_LABELS[ft],
                compareType=COMPARE_TYPES.PREDICTS,
                valueType=VALUE_TYPE.FOLD
            )
            for ft in FoldType
        ]

        data = [
            SIndicator(
                key=self.KEY,
                label=self.LABEL,
                compareType=COMPARE_TYPES.EMPTY,
                children=children
            )
        ]
        return data


class ReportMaker(ClassificationReport):
    Reports = [BaseReport, FoldReport, PredictReport]
    # Reports = [PredictReport]

    def __init__(self, clsf):
        self.reports: list[ClassificationReport] = [
            Report(clsf)
            for Report in self.Reports
        ]

    def get_data(self) -> dict:
        data = {}
        for report in self.reports:
            data.update(report.get_data())

        return data

    def get_indicators(self) -> List[SIndicator]:
        data = []
        for report in self.reports:
            data += report.get_indicators()
        return data
