CREATE TABLE IF NOT EXISTS product_ad_sales (
    date TEXT,
    item_id INTEGER,
    ad_sales REAL,
    impressions INTEGER,
    ad_spend REAL,
    clicks INTEGER,
    units_sold INTEGER
);


CREATE TABLE IF NOT EXISTS product_total_sales (
    date TEXT,
    item_id INTEGER,
    total_sales REAL,
    total_units_ordered INTEGER
);


CREATE TABLE IF NOT EXISTS product_eligibility (
    eligibility_datetime_utc TEXT,
    item_id INTEGER,
    eligibility BOOLEAN,
    message TEXT
);
