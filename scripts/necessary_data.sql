# Adding roles
INSERT INTO vov_database.user_role (id, name) VALUES (1, 'customer');
INSERT INTO vov_database.user_role (id, name) VALUES (3, 'moderator');
INSERT INTO vov_database.user_role (id, name) VALUES (2, 'seller');

# Adding users
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (1, 'Vlad', 'vlad@gmail.com', '$2b$12$3DMcWqyvXTd2GUnJLa79Le379rKv2AKXfC7IOCYCOHMyEvK5WUwWu', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (2, 'Oleksiy', 'alex@gmail.com', '$2b$12$zhCEhiljh1EnCGyyK5ZO9eEMBR1D8Zs/MMeF3XwcG/NyElg9Y21ru', 2);

# Adding categories
INSERT INTO vov_database.category (id, parent_id, name) VALUES (1, null, 'Tools');
INSERT INTO vov_database.category (id, parent_id, name) VALUES (2, null, 'Food');
INSERT INTO vov_database.category (id, parent_id, name) VALUES (3, null, 'Animals');

# Adding customer_order statuses
INSERT INTO vov_database.order_status (name, id) VALUES ('canceled', 3);
INSERT INTO vov_database.order_status (name, id) VALUES ('closed', 2);
INSERT INTO vov_database.order_status (name, id) VALUES ('in_process', 1);
