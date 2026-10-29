-- Deduplicate assignments into staging[cite: 7]
CREATE OR REPLACE TABLE stg.assignments AS
SELECT DISTINCT
    user_id,
    variant,
    CAST(assigned_at AS TIMESTAMP) AS assigned_at
FROM raw.assignments;

-- Filter valid events into staging[cite: 7]
CREATE OR REPLACE TABLE stg.events AS
SELECT
    user_id,
    event_name,
    CAST(event_ts AS TIMESTAMP) AS event_ts,
    value
FROM raw.events
WHERE event_ts IS NOT NULL;