# Adding users
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (1, 'Vlad', 'vlad@gmail.com', '$2b$12$3DMcWqyvXTd2GUnJLa79Le379rKv2AKXfC7IOCYCOHMyEvK5WUwWu', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (5, 'Nina', 'nino@gmail.com', '$2b$12$nZE/yezyHiU1vUhsJMUUqeeIvj0qnJChuMt6x2ia435e9fq18pdX6', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (6, 'Alex', 'alex@gmail.com', '$2b$12$nahxh5vYC8I.tLuzql1OlOga1Cl5rsoTyjnTuD/a08o443iaeV3eS', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (2, 'Oleksiy', 'alex@gmail.com', '$2b$12$3DMcWqyvXTd2GUnJLa79Le379rKv2AKXfC7IOCYCOHMyEvK5WUwWu', 2);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (4, 'Salamon', 'someone@gmail.com', '$2b$12$Y9o.zUIWKa4LLX.ZwV8XmuvyYDCK8bEd4vd.9xQjnTA7JoxblZsta', 2);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (7, 'Riko', 'rik@gmail.com', '$2b$12$4BCe962dVOoOEWbahzWxFOVgG7q80J8ftmFj3Kn7Tabg5UWieK3tS', 2);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (3, 'Lera', 'lera@gmail.com', '$2b$12$Bfso3NBwQ1Ygw8hBrUIwZel0H428ASTrns5bc.rv5Dd24LFNtNuiC', 3);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (8, 'Greg', 'greg@gmail.com', '$2b$12$PZezeOOeTQ8E/DvNqtb9Kud0pLFuKl3sIxJAO6Dwa2Rp1jdElbFjW', 3);


# Adding shop data
INSERT INTO vov_database.shop_data (name, description, id, approved) VALUES ('MegaShop', 'Selling mega products.', 1, 1);
INSERT INTO vov_database.shop_data (name, description, id, approved) VALUES ('BestTools', 'Best tools here.', 2, 1);
INSERT INTO vov_database.shop_data (name, description, id, approved) VALUES ('ZooMag', 'Pets and goods for them.', 3, 1);

# Adding shop
INSERT INTO vov_database.shop (shop_data_id, seller_id) VALUES (1, 2);
INSERT INTO vov_database.shop (shop_data_id, seller_id) VALUES (2, 4);
INSERT INTO vov_database.shop (shop_data_id, seller_id) VALUES (3, 7);

# Adding create_shop_request
INSERT INTO vov_database.create_shop_request (refuse_reason, shop_data_id, request_status_id, creation_date, check_date, moderator_id, seller_id) VALUES (null, 1, 2, '2023-06-03 23:43:07', '2023-06-03 23:43:06', 8, 2);
INSERT INTO vov_database.create_shop_request (refuse_reason, shop_data_id, request_status_id, creation_date, check_date, moderator_id, seller_id) VALUES (null, 2, 2, '2023-06-03 23:43:09', '2023-06-03 23:43:09', 8, 4);
INSERT INTO vov_database.create_shop_request (refuse_reason, shop_data_id, request_status_id, creation_date, check_date, moderator_id, seller_id) VALUES (null, 3, 2, '2023-06-03 23:43:11', '2023-06-03 23:43:11', 8, 7);

# Adding products data
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Spider', 'An exotic pet.', 1, 1, '/spiduh.jpg');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Apple', 'Very tasty.', 2, 1, '/apple.jpg');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Screwdriver', 'An irreplaceable tool. ', 3, 1, '/screwdriver.png');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Rice', 'Very useful grain.', 4, 1, 'products/dc238a6d-cc5b-46d0-a030-392d05670bb8.jpg');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Rat', 'Cute pet.', 5, 1, 'products/2eb8917a-44c0-44a5-a576-afdfa36f088f.png');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Chainsaw', 'Best for cutting wood.', 6, 1, 'products/25f2234c-d943-42c5-bde5-23f251e7a988.jpg');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Wrench', 'Adjustable wrench for different screws.', 7, 1, 'products/d405eb24-ccd8-4fc1-9b12-7258823cb76f.jpg');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Crowbar', 'Very useful in the yard.', 8, 1, 'products/686d1c16-df5d-46f0-81f9-822869765d91.jpg');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Chisel', 'Versatile and indispensable tool.', 9, 1, 'products/98792f1c-2b87-43ba-bd2d-b478a078709c.png');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Axe', 'Perfect for chopping wood.', 10, 1, 'products/c9b256c1-230b-4bc5-a8fd-011585327c82.jpg');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Snickers', 'You are not you when you are hungry.', 11, 1, 'products/611f87fe-774e-4a9e-b5a6-6512b3e461f6.png');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Rat food', 'Balanced meal for rats and mouse.', 12, 1, 'products/f8bd6ba0-db87-4785-872e-e450efb98d23.png');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Wooden chips', 'Good bedding for rodents.', 13, 1, 'products/7b1aaad8-e649-4b99-9636-dca8bd1fca9e.png');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Drinker', 'Drinker for rodents.', 14, 1, 'products/b027baff-ff35-4c0d-87ba-bb6080f7a4e8.');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Cage', 'Cage for small or medium rodents', 15, 1, 'products/3d7f6087-821b-413f-a2c5-75aa2981c530.png');

# Adding products
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (1, 1, 15.00, 2);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (2, 2, 5.00, 2);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (3, 3, 40.00, 2);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (4, 4, 15.50, 2);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (5, 5, 200.00, 2);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (6, 6, 5000.00, 4);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (7, 7, 500.00, 4);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (8, 8, 1500.00, 4);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (9, 9, 750.00, 4);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (10, 10, 1000.00, 4);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (11, 11, 19.00, 7);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (12, 12, 75.00, 7);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (13, 13, 50.00, 7);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (14, 14, 87.00, 7);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (15, 15, 600.00, 7);

# Binding products to categories
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (3, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (6, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (7, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (8, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (9, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (10, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (2, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (4, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (11, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (12, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (1, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (5, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (12, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (13, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (14, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (15, 3);

# Adding requests for products (already approved)
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (2, null, 3, 1, 2, '2023-06-02 14:06:36', '2023-06-02 14:06:39');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (2, null, 3, 2, 2, '2023-06-02 14:06:57', '2023-06-02 14:06:59');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (2, null, 3, 3, 2, '2023-06-02 14:07:08', '2023-06-02 14:07:09');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (2, null, 8, 4, 2, '2023-06-03 18:39:48', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (2, null, 8, 5, 2, '2023-06-03 18:43:19', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (4, null, 8, 6, 2, '2023-06-03 18:54:35', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (4, null, 8, 7, 2, '2023-06-03 18:56:37', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (4, null, 8, 8, 2, '2023-06-03 18:58:29', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (4, null, 8, 9, 2, '2023-06-03 19:01:15', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (4, null, 8, 10, 2, '2023-06-03 19:04:22', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (7, null, 8, 11, 2, '2023-06-03 19:38:52', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (7, null, 8, 12, 2, '2023-06-03 19:40:13', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (7, null, 8, 13, 2, '2023-06-03 19:42:20', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (7, null, 8, 14, 2, '2023-06-03 19:43:10', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (7, null, 8, 15, 2, '2023-06-03 19:44:02', null);
