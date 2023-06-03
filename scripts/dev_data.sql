# Adding users
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (1, 'Vlad', 'vlad@gmail.com', '$2b$12$3DMcWqyvXTd2GUnJLa79Le379rKv2AKXfC7IOCYCOHMyEvK5WUwWu', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (2, 'Oleksiy', 'alex@gmail.com', '$2b$12$3DMcWqyvXTd2GUnJLa79Le379rKv2AKXfC7IOCYCOHMyEvK5WUwWu', 2);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (3, 'Lera', 'lera@gmail.com', '$2b$12$Bfso3NBwQ1Ygw8hBrUIwZel0H428ASTrns5bc.rv5Dd24LFNtNuiC', 3);


# Adding shop data
INSERT INTO vov_database.shop_data (name, description, id, approved) VALUES ('Some shop', 'description', 1, 1);

# Adding shop
INSERT INTO vov_database.shop (shop_data_id, seller_id) VALUES (1, 3);

# Adding create_shop_request
INSERT INTO vov_database.create_shop_request (refuse_reason, shop_data_id, request_status_id, creation_date, check_date, moderator_id, seller_id) VALUES (null, 1, 2, '2023-06-03 17:17:06', '2023-06-03 17:17:09', 2, 3);

# Adding products data
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Spiduh', 'Very spiduh', 1, 1, '/spiduh.jpg');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Apple', 'Very tasty', 2, 0, '/apple.jpg');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Screwdriver', 'Very screw', 3, 0, '/screwdriver.png');

# Adding products
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (1, 1, 15.00, 3);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (2, 2, 5.00, 3);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (3, 3, 40.00, 3);

# Binding products to categories
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (1, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (2, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (3, 1);

# Adding requests for products (already approved)
INSERT INTO add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (3, null, 3, 1, 2, '2023-06-02 14:06:36', '2023-06-02 14:06:39');
INSERT INTO add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (3, null, 3, 2, 2, '2023-06-02 14:06:57', '2023-06-02 14:06:59');
INSERT INTO add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (3, null, 3, 3, 2, '2023-06-02 14:07:08', '2023-06-02 14:07:09');