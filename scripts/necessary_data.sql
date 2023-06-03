# Adding roles
INSERT INTO vov_database.user_role (id, name) VALUES (1, 'customer');
INSERT INTO vov_database.user_role (id, name) VALUES (3, 'moderator');
INSERT INTO vov_database.user_role (id, name) VALUES (2, 'seller');


# Adding statuses for requests
INSERT INTO vov_database.request_status (name, id) VALUES ('in_process', 1);
INSERT INTO vov_database.request_status (name, id) VALUES ('accepted', 2);
INSERT INTO vov_database.request_status (name, id) VALUES ('declined', 3);


# Adding categories
INSERT INTO vov_database.category (parent_id, name) VALUES (null, 'Tools');
INSERT INTO vov_database.category (parent_id, name) VALUES (null, 'Food');
INSERT INTO vov_database.category (parent_id, name) VALUES (null, 'Animals');


# Adding order_status statuses
INSERT INTO vov_database.order_status (name, id) VALUES ('canceled', 3);
INSERT INTO vov_database.order_status (name, id) VALUES ('closed', 2);
INSERT INTO vov_database.order_status (name, id) VALUES ('in_process', 1);


# Adding statuses for order items
INSERT INTO vov_database.order_item_status (name, id) VALUES ('accepted', 2);
INSERT INTO vov_database.order_item_status (name, id) VALUES ('canceled', 4);
INSERT INTO vov_database.order_item_status (name, id) VALUES ('declined', 3);
INSERT INTO vov_database.order_item_status (name, id) VALUES ('in_process', 1);


