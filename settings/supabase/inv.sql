CREATE TABLE public.user_inventory (
    inventory_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    purchase_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.currency_table(user_id),
    CONSTRAINT fk_item FOREIGN KEY (item_id) REFERENCES public.shop_items(item_id)
);
