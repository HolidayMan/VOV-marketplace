# Adding roles
INSERT INTO vov_database.user_role (id, name) VALUES (1, 'customer');
INSERT INTO vov_database.user_role (id, name) VALUES (3, 'moderator');
INSERT INTO vov_database.user_role (id, name) VALUES (2, 'seller');

# Adding categories
INSERT INTO vov_database.category (id, parent_id, name) VALUES (1, null, 'Tools');
INSERT INTO vov_database.category (id, parent_id, name) VALUES (2, null, 'Food');
INSERT INTO vov_database.category (id, parent_id, name) VALUES (3, null, 'Animals');

# Adding order statuses
INSERT INTO vov_database.order_status (name, id) VALUES ('canceled', 3);
INSERT INTO vov_database.order_status (name, id) VALUES ('closed', 2);
INSERT INTO vov_database.order_status (name, id) VALUES ('in_process', 1);
