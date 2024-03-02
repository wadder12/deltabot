
create table
  public.shop_items (
    item_id serial,
    name character varying(255) null,
    description text null,
    cost integer null,
    special_identifier character varying(255) null,
    constraint shop_items_pkey primary key (item_id)
  ) tablespace pg_default;

-- how to add items to the shop (example)

INSERT INTO shop_items (name, description, cost, special_identifier) VALUES
('VIP Role', 'Grants you a VIP role with access to exclusive channels.', 500, 'vip_role'),
('Super Supporter Role', 'Grants you the Super Supporter role, with special permissions and recognition.', 1000, 'super_supporter_role'),
('Custom Nickname', 'Allows you to set a custom nickname in the server for a month.', 200, 'custom_nickname'),
('Zeus for a Day', 'Be the Zeus in our next ARMA mission, controlling the game for everyone.', 800, 'zeus_for_a_day'),
('Custom Emoji', 'Add a custom emoji of your choice to the server (subject to approval).', 300, 'custom_emoji'),
('Mystery Box', 'A mystery box that could contain anything from roles to custom privileges.', 250, 'mystery_box');
