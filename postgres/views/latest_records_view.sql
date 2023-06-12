-- View: public.latest_records

-- DROP VIEW public.latest_records;

CREATE OR REPLACE VIEW public.latest_records
 AS
 WITH latest_records AS (
         SELECT sub.processed_at,
            sub.region,
            sub.item_id,
            sub.item_main_category,
            sub.item_sub_category,
            sub.current_stock,
            sub.total_trades,
            sub.base_price,
            sub.rn
           FROM ( SELECT bdo_world_market_data.processed_at,
                    bdo_world_market_data.region,
                    bdo_world_market_data.item_id,
                    bdo_world_market_data.item_main_category,
                    bdo_world_market_data.item_sub_category,
                    bdo_world_market_data.current_stock,
                    bdo_world_market_data.total_trades,
                    bdo_world_market_data.base_price,
                    row_number() OVER (PARTITION BY bdo_world_market_data.region, bdo_world_market_data.item_id ORDER BY bdo_world_market_data.processed_at DESC) AS rn
                   FROM bdo_world_market_data) sub
          WHERE sub.rn <= 2
        ), diffs AS (
         SELECT latest_records.processed_at,
            latest_records.region,
            latest_records.item_id,
            latest_records.item_main_category,
            latest_records.item_sub_category,
            latest_records.current_stock,
            latest_records.total_trades,
            latest_records.base_price,
            latest_records.rn,
            latest_records.current_stock - lead(latest_records.current_stock, 1) OVER (PARTITION BY latest_records.region, latest_records.item_id ORDER BY latest_records.processed_at DESC) AS current_stock_diff,
            latest_records.total_trades - lead(latest_records.total_trades, 1) OVER (PARTITION BY latest_records.region, latest_records.item_id ORDER BY latest_records.processed_at DESC) AS total_trades_diff,
            latest_records.base_price - lead(latest_records.base_price, 1) OVER (PARTITION BY latest_records.region, latest_records.item_id ORDER BY latest_records.processed_at DESC) AS base_price_diff
           FROM latest_records
        )
 SELECT diffs.processed_at,
    diffs.region,
    diffs.item_id,
    diffs.item_main_category,
    diffs.item_sub_category,
    diffs.current_stock,
    diffs.total_trades,
    diffs.base_price,
    diffs.current_stock_diff,
    diffs.total_trades_diff,
    diffs.base_price_diff
   FROM diffs
  WHERE diffs.rn = 1;

ALTER TABLE public.latest_records
    OWNER TO bdo_data;
