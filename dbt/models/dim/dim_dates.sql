{{ 
    config(
        materialized='table',
        unique_key='date_id'
    )
}}

WITH date_spine AS (
    {{ dbt_utils.date_spine(
        start_date="cast('2020-01-01' as date)",
        end_date="cast('2025-12-31' as date)",
        datepart="day"
    ) }}
)
SELECT
    {{ dbt_utils.surrogate_key(['date_day']) }} AS date_id,
    date_day AS date,
    EXTRACT(YEAR FROM date_day) AS year,
    EXTRACT(MONTH FROM date_day) AS month,
    EXTRACT(DAY FROM date_day) AS day,
    EXTRACT(DAYOFWEEK FROM date_day) AS day_of_week,
    EXTRACT(QUARTER FROM date_day) AS quarter
FROM date_spine
