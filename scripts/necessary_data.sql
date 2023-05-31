# Adding roles
INSERT INTO vov_database.user_role (name) VALUES ('customer');
INSERT INTO vov_database.user_role (name) VALUES ('moderator');
INSERT INTO vov_database.user_role (name) VALUES ('seller');

# Adding categories
INSERT INTO vov_database.category (parent_id, name) VALUES (null, 'Tools');
INSERT INTO vov_database.category (parent_id, name) VALUES (null, 'Food');
INSERT INTO vov_database.category (parent_id, name) VALUES (null, 'Animals');

# Adding customer_order statuses
INSERT INTO vov_database.order_status (name) VALUES ('in_process');
INSERT INTO vov_database.order_status (name) VALUES ('closed');
INSERT INTO vov_database.order_status (name) VALUES ('canceled');



# Adding statuses for order items
INSERT INTO vov_database.order_item_status (name) VALUES ('in_process');
INSERT INTO vov_database.order_item_status (name) VALUES ('accepted');
INSERT INTO vov_database.order_item_status (name) VALUES ('declined');
INSERT INTO vov_database.order_item_status (name) VALUES ('canceled');

