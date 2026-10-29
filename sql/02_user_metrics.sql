CREATE OR REPLACE TABLE mart.user_metrics AS
SELECT
    a.user_id,
    a.variant,
    MAX(CASE WHEN e.event_name = 'return_day_1' THEN 1 ELSE 0 END) AS retained_d1,
    MAX(CASE WHEN e.event_name = 'return_day_7' THEN 1 ELSE 0 END) AS retained_d7,
    COALESCE(SUM(CASE WHEN e.event_name = 'game_round' THEN 1 END), 0) AS rounds_14d
FROM stg.assignments a
LEFT JOIN stg.events e
    ON e.user_id = a.user_id
    AND e.event_ts BETWEEN a.assigned_at AND a.assigned_at + INTERVAL '14 days'
GROUP BY a.user_id, a.variant;