{{ config(materialized='table', alias='discounted_product_prices') }}

WITH category_avg AS (
    -- Step 1: Get the average price per category
    SELECT
        category,
        gender,
        brand,
        AVG(price) AS avg_price
    FROM PRODUCTS_DB.PRODUCTS.PRODUCTS
    GROUP BY category, gender, brand
),

discounted_prices AS (
    -- Step 2: Calculate the 50% discount
    SELECT
        category,
        gender,
        brand,
        avg_price,
        avg_price * 0.5 AS discounted_price
    FROM category_avg
),

pricing_tiers AS (
    -- Create a table of pricing tiers
    SELECT pricing_tier FROM (
        VALUES
            (4.99), (7.99), (9.99), (12.99), (14.99), (16.99),
            (19.99), (24.99), (29.99), (34.99), (39.99), (49.99), (59.99), (69.99),
            (79.99), (89.99), (99.99), (119.99), (149.99), (199.99), (249.99)
    ) AS p(pricing_tier)
),

rounded_prices AS (
    -- Step 3: Round to the nearest predefined tier
    SELECT
        d.category,
        d.gender,
        d.brand,
        d.avg_price,
        d.discounted_price,
        p.pricing_tier AS final_price,
        ROW_NUMBER() OVER (
            PARTITION BY d.category, d.gender, d.brand
            ORDER BY ABS(d.discounted_price - p.pricing_tier)
        ) AS rank
    FROM discounted_prices d
    CROSS JOIN pricing_tiers p
)

SELECT 
    category,
    gender,
    brand,
    avg_price,
    discounted_price,
    final_price
FROM rounded_prices
WHERE rank = 1