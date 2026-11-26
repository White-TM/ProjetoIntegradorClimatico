-- ============================================================================
-- CONSULTA 1 (KPI 1: Índice de Estresse Térmico e Amplitude Média)
-- Pergunta: Qual foi a temperatura máxima média, a amplitude térmica média e
-- quantos dias ultrapassaram 32 °C (risco de estresse térmico para cultivos)?
-- ============================================================================
SELECT
    localidade,
    COUNT(*) AS total_dias_analisados,
    ROUND(AVG(temp_max_c), 2) AS media_temp_max_c,
    ROUND(AVG(temp_min_c), 2) AS media_temp_min_c,
    ROUND(AVG(temp_max_c - temp_min_c), 2) AS amplitude_termica_media_c,
    SUM(CASE WHEN temp_max_c > 32.0 THEN 1 ELSE 0 END) AS dias_acima_32c
FROM clima_diario
GROUP BY localidade;

-- ============================================================================
-- CONSULTA 2 (KPI 2: Volume Pluviométrico Acumulado e Frequência de Chuva)
-- Pergunta: Qual foi o volume total de precipitação no período e em quantos
-- dias houve chuva relevante (>= 1,0 mm) para manejo agrícola?
-- ============================================================================
SELECT
    localidade,
    ROUND(SUM(precipitacao_mm), 2) AS precipitacao_total_mm,
    ROUND(MAX(precipitacao_mm), 2) AS maior_chuva_diaria_mm,
    SUM(CASE WHEN precipitacao_mm >= 1.0 THEN 1 ELSE 0 END) AS dias_com_chuva_relevante,
    ROUND(
        100.0 * SUM(CASE WHEN precipitacao_mm >= 1.0 THEN 1 ELSE 0 END) / COUNT(*),
        1
    ) AS percentual_dias_chuvosos
FROM clima_diario
GROUP BY localidade;

-- ============================================================================
-- CONSULTA 3 (KPI 3: Identificação de Janelas Críticas de Calor Seco)
-- Pergunta: Quais datas específicas apresentaram combinação crítica de calor
-- elevado (temp_max_c >= 30 °C) sem precipitação (precipitacao_mm = 0)?
-- ============================================================================
SELECT
    data,
    temp_min_c,
    temp_max_c,
    ROUND(temp_max_c - temp_min_c, 2) AS amplitude_dia_c,
    precipitacao_mm
FROM clima_diario
WHERE temp_max_c >= 30.0
  AND precipitacao_mm = 0.0
ORDER BY temp_max_c DESC, data ASC;
