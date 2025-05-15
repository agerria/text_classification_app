from typing import Optional, Tuple, Any
import numpy as np
import math
from scipy.stats import ttest_rel, wilcoxon
from pydantic import BaseModel, validator



class CmpResult(BaseModel):
    is_valid: bool  # Применим ли метод к данным
    p_value: Optional[float] = None  # Значимость различий
    statistic: Optional[float] = None  # Статистика теста (t, W и т.д.)
    difference: Optional[float] = None  # Средняя разница между folds1 и folds2
    confidence_interval: Optional[Tuple[float, float]] = None  # ДИ для разницы
    
    
    class Config:
        json_encoders = {
            float: lambda v: None if math.isnan(v) else v
        }


def paired_t_test(folds1: list[float], folds2: list[float]) -> CmpResult:
    """
    Парный t-тест для сравнения средних на одних и тех же фолдах.
    Предполагает нормальность распределения разниц (но робастен при n >= 30).
    """
    n = len(folds1)
    if len(folds1) != len(folds2) or n < 2:
        return CmpResult(is_valid=False)

    try:
        t_stat, p_val = ttest_rel(folds1, folds2)
    except Exception:
        return CmpResult(is_valid=False)

    diffs = np.array(folds1) - np.array(folds2)
    # avg_diff = float(np.mean(diffs))
    avg_diff = float(np.mean(diffs) / np.mean(folds2))

    return CmpResult(
        is_valid=True,
        p_value=float(p_val),
        statistic=float(t_stat),
        difference=avg_diff,
    )


def wilcoxon_signed_rank_test(folds1: list[float], folds2: list[float]) -> CmpResult:
    """
    Тест знаковых рангов Вилкоксона (непараметрический аналог t-теста).
    Требует ненулевых разниц между фолдами.
    """
    n = len(folds1)
    if len(folds1) != len(folds2) or n < 2:
        return CmpResult(is_valid=False)

    diffs = np.array(folds1) - np.array(folds2)
    if np.all(diffs == 0):
        return CmpResult(is_valid=False)

    try:
        res = wilcoxon(diffs)
    except Exception:
        return CmpResult(is_valid=False)

    # avg_diff = float(np.mean(diffs))
    avg_diff = float(np.mean(diffs) / np.mean(folds2))

    return CmpResult(
        is_valid=True,
        p_value=float(res.pvalue),
        statistic=float(res.statistic),
        difference=avg_diff,
    )


def bootstrap_mean_difference(
    folds1: list[float],
    folds2: list[float],
    n_bootstrap: int = 1000,
    ci: int = 95
) -> CmpResult:
    """
    Бутстреп-метод для оценки доверительного интервала средней разницы.
    Не предоставляет p-значение, но показывает неопределенность в оценке.
    """
    n = len(folds1)
    if len(folds1) != len(folds2) or n < 2:
        return CmpResult(is_valid=False)

    diffs = np.array(folds1) - np.array(folds2)
    # avg_diff = float(np.mean(diffs))
    avg_diff = float(np.mean(diffs) / np.mean(folds2))

    # Генерация бутстреп-выборок
    bootstrap_means = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(diffs, size=n, replace=True)
        bootstrap_means.append(np.mean(sample))

    # Расчет доверительного интервала
    alpha = (100 - ci) / 2
    lower = float(np.percentile(bootstrap_means, alpha))
    upper = float(np.percentile(bootstrap_means, 100 - alpha))

    return CmpResult(
        is_valid=True,
        difference=avg_diff,
        confidence_interval=(lower, upper),
    )
    
    
from statsmodels.stats.contingency_tables import SquareTable
import numpy as np

def mcnemar_test(result_a, result_b):
    # Проверка совпадения тестовых данных
    test_a_decoded = [result_a["classes"][i] for i in result_a["test"]]
    test_b_decoded = [result_b["classes"][i] for i in result_b["test"]]
    if test_a_decoded != test_b_decoded:
        return CmpResult(is_valid=False)

    # Строим матрицу сопряжённости
    k = len(result_a["classes"])
    contingency_matrix = np.zeros((k, k), dtype=int)
    
    for a_pred, b_pred in zip(result_a["predicts"], result_b["predicts"]):
        contingency_matrix[a_pred][b_pred] += 1

    # Проводим тест
    table = SquareTable(contingency_matrix)
    result = table.homogeneity()
    
    return CmpResult(
        is_valid=True,
        statistic=result.statistic,
        p_value=result.pvalue,
    )
    return {"statistic": result.statistic, "pvalue": result.pvalue}