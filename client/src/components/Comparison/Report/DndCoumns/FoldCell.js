import { useState, useEffect } from 'react'
import { COMPARE_TYPES } from "../consts";
import { Tooltip } from 'antd'


const CpmResultViz = ({ result, compareType }) => {
  const getStatus = () => {
    // Обработка невалидных результатов
    if (!result?.is_valid) {
      return {
        color: "bg-gray-400",
        mainLabel: "❔ Не применимо",
        tooltipContent: (
          <div className="text-xs space-y-2">
            <p>Метод сравнения неприменим:</p>
            <ul className="list-disc pl-4">
              <li>Некорректные входные данные</li>
              <li>Неподходящий метод анализа</li>
            </ul>
          </div>
        )
      }
    }

    // Обработка идентичных данных
    const isIdentical = result.p_value === null
    const isSignificant = !isIdentical && result.p_value < 0.05
    const pValuePercent = isIdentical 
      ? '100%' 
      : (result.p_value * 100).toFixed(1)
    const isMcNemar = compareType === 'predicts'

    // Форматирование основной метки
    const effectLabel = isIdentical 
      ? "≡ Идентично" 
      : isMcNemar 
        ? `χ²=${result.statistic?.toFixed(1) || '?'}`
        : isSignificant 
          ? `${result.difference > 0 ? "▲" : "▼"} ${(Math.abs(result.difference)*100).toFixed(1)}%`
          : "≈ Нет различий"

    const getTestDescription = () => {
      switch(compareType) {
        case 'ttest': return "Парный t-тест (сравнение средних)"
        case 'wilcoxon': return "Тест Вилкоксона (ранговый анализ)"
        case 'bootstrap': return "Бутстреп-анализ (стабильность)"
        case 'predicts': return "Тест МакНемара (сравнение классификаторов)"
        default: return "Статистический анализ"
      }
    }

    const getColor = () => {
      if (isIdentical) return "bg-gray-300"
      if (isMcNemar) return isSignificant ? "bg-purple-500" : "bg-yellow-400"
      return isSignificant 
        ? (result.difference > 0 ? "bg-green-500" : "bg-red-500")
        : "bg-yellow-400"
    }

    const tooltipContent = (
      <div className="text-xs space-y-2">
        <div>
          <p className="font-medium mb-1">📌 Метод анализа</p>
          <p>{getTestDescription()}</p>
        </div>

        {isIdentical ? (
          <div>
            <p className="font-medium mb-1">🔍 Результат</p>
            <p>Модели показали абсолютно идентичные результаты</p>
          </div>
        ) : isMcNemar ? (
          <div>
            <p className="font-medium mb-1">📌 Интерпретация</p>
            <p>
              {isSignificant 
                ? "Обнаружены статистически значимые различия"
                : "Значимые различия отсутствуют"}
            </p>
          </div>
        ) : isSignificant ? (
          <div>
            <p className="font-medium mb-1">📌 Практический эффект</p>
            <p>
              {result.difference > 0 ? "Улучшение" : "Ухудшение"} на<br/>
              <strong>{(Math.abs(result.difference)*100).toFixed(1)}%</strong>
            </p>
          </div>
        ) : (
          <div>
            <p className="font-medium mb-1">📌 Ключевой вывод</p>
            <p>Различия не превышают случайные колебания</p>
          </div>
        )}

        <div>
          <p className="font-medium mb-1">📊 Статистическая значимость</p>
          <p>
            {isIdentical ? (
              <span className="text-gray-600">Модели идентичны</span>
            ) : isSignificant ? (
              <span className="text-green-600">p = {pValuePercent} &lt; 5%</span>
            ) : (
              <span className="text-amber-600">p = {pValuePercent} ≥ 5%</span>
            )}
          </p>
        </div>

        {!isIdentical && compareType !== 'bootstrap' && result.statistic !== undefined  && (
          <div>
            <p className="font-medium mb-1">🔍 Значение статистики</p>
            <p>
              {compareType === 'wilcoxon' ? `W = ${result.statistic.toFixed(1)}` :
               compareType === 'predicts' ? `χ² = ${result.statistic.toFixed(1)}` :
               `t = ${result.statistic.toFixed(1)}`}
            </p>
          </div>
        )}
      </div>
    )

    return {
      color: getColor(),
      mainLabel: effectLabel,
      tooltipContent
    }
  }

  const { color, mainLabel, tooltipContent } = getStatus()

  return (
    <div className="w-[200px] h-[30px] flex items-center justify-between px-2 bg-white">
      <span className="text-[13px] font-medium text-gray-800">
        {mainLabel}
      </span>

      <Tooltip 
        title={tooltipContent}
        overlayClassName="max-w-[260px]"
        placement="bottomRight"
      >
        <div className={`w-3 h-3 rounded-full ${color} shadow-md cursor-help 
          hover:scale-110 transition-transform`} />
      </Tooltip>
    </div>
  )
}

const FoldCell = ({ value, compareType, referenceValue, showComparison }) => {
    if (!showComparison)
        return ''
    const hash = referenceValue?.hash;
    const cmps = value?.cmps;
    const cmpRes = cmps[hash];

    return (<CpmResultViz result={cmpRes} compareType={compareType}/>)
}

export default FoldCell;