# Adding roles
INSERT INTO vov_database.user_role (name) VALUES ('customer');
INSERT INTO vov_database.user_role (name) VALUES ('moderator');
INSERT INTO vov_database.user_role (name) VALUES ('seller');


# Adding statuses for requests
INSERT INTO vov_database.request_status (name, id) VALUES ('in_process', 1);
INSERT INTO vov_database.request_status (name, id) VALUES ('accepted', 2);
INSERT INTO vov_database.request_status (name, id) VALUES ('declined', 3);


# Adding categories
INSERT INTO vov_database.category (parent_id, name) VALUES (null, 'Tools');
INSERT INTO vov_database.category (parent_id, name) VALUES (null, 'Food');
INSERT INTO vov_database.category (parent_id, name) VALUES (null, 'Animals');


# Adding order_status statuses
INSERT INTO vov_database.order_status (name) VALUES ('in_process');
INSERT INTO vov_database.order_status (name) VALUES ('closed');
INSERT INTO vov_database.order_status (name) VALUES ('canceled');


# Adding statuses for order items
INSERT INTO vov_database.order_item_status (name) VALUES ('in_process');
INSERT INTO vov_database.order_item_status (name) VALUES ('accepted');
INSERT INTO vov_database.order_item_status (name) VALUES ('declined');
INSERT INTO vov_database.order_item_status (name) VALUES ('canceled');

