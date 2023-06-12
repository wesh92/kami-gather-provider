-- Table: public.bdo_world_market_data

-- DROP TABLE IF EXISTS public.bdo_world_market_data;

CREATE TABLE IF NOT EXISTS public.bdo_world_market_data
(
    processed_at timestamp without time zone NOT NULL,
    region text COLLATE pg_catalog."default" NOT NULL,
    item_id bigint NOT NULL,
    item_main_category integer NOT NULL,
    item_sub_category integer NOT NULL,
    current_stock bigint,
    total_trades bigint,
    base_price bigint,
    CONSTRAINT pk__bdo_world_market_data PRIMARY KEY (processed_at, region, item_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bdo_world_market_data
    OWNER to bdo_data;
