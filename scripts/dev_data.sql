# Adding users
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (1, 'Vlad', 'vlad@gmail.com', '$2b$12$ow7f380oWsGMSkFnhsUCruRETvoXwtM.ccYn/LxMWymD.71tNhlKy', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (5, 'Nina', 'nino@gmail.com', '$2b$12$kV90KcUcv9kG87/3n0W/OeBXWYIFAt.JmVcd721kBiW70EcDsdqou', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (6, 'Alex', 'alex@gmail.com', '$2b$12$qWY.jvzuYa0N/TeC5tGSaOnZb.YJFij41o5iP53zifXNlcGSNhDSC', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (9, 'Nickolas', 'nick@gmail.com', '$2b$12$oaLnes2n3XWedYLXMQim2Orho1bvMzszZEIkitSI5naLn/3i1uz7e', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (10, 'Diana', 'dia@gmail.com', '$2b$12$YJO.At3oZ.gvK6uiMZ3Mm.zjb3uTdKfmBai24Zwvn1xXmSRv8av4G', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (11, 'Georigy', 'georg@gmail.com', '$2b$12$QLfnJJcTzOXjcfGS9/oXEu8LWfu6nKXZ0tC3sGHtjqtr6bpYnpaUi', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (12, 'Ivan', 'ivan@gmail.com', '$2b$12$L68s0AQHozpWbBmGhG5j9eVVr3QWu1G8R1ntwLrGz6hRZ91DYW6bS', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (13, 'Igor', 'igor@gmail.com', '$2b$12$EhazXNEnFyoZkVBNzJ6DOuXZzLLX.w3D/evACq8pNpoR4Utb2SmZG', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (14, 'Liza', 'lisa@gmail.com', '$2b$12$4FaXma42jwwzKl9lcgDb2uwNS7J7VrlSp7OWjgkVVYwHMp/sfJBaO', 1);
INSERT INTO vov_database.user (id, name, email, password, role_id) VALUES (15, 'Anna', 'an@gmail.com', '$2b$12$Jp3P0NLRjzaeIHy3FZYlJ.DOjk3bzPqDXza.QO4CwlT7ODttFe7J6', 1);


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
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Flour', 'For better baking.', 16, 1, 'products/a9074714-3b80-4804-81f0-0b613be2bcfe.png');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Chocolate', 'Delicate milk chocolate.', 17, 1, 'products/432ec27b-7d2b-49f3-82de-d76c2461458e.png');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Hammer', 'For any nail.', 18, 1, 'products/93499a73-e064-4166-9a36-3805d42c1b67.jpg');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Pliers', 'These pliers are spring loaded and are also equipped with wire cutters and regular pliers for round-shape objects', 19, 1, 'products/c18bb2d1-0ec9-465c-a382-b233c75103ea.jpg');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Cat food', 'Balanced meal for your cat.', 20, 1, 'products/bacdc7c0-c340-4ad1-a351-73c0d8babdda.jpg');
INSERT INTO vov_database.product_data (name, description, id, approved, image_file_path) VALUES ('Dog food', 'Balanced meal for your dog.', 21, 1, 'products/23233044-3c46-47e2-845a-710868f01f19.jpg');

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
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (16, 16, 60.00, 2);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (17, 17, 55.00, 2);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (18, 18, 250.00, 4);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (19, 19, 225.00, 4);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (20, 20, 100.00, 7);
INSERT INTO vov_database.product (product_data_id, id, price, seller_id) VALUES (21, 21, 125.00, 7);

# Binding products to categories
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (3, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (6, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (7, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (8, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (9, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (10, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (18, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (19, 1);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (2, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (4, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (11, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (12, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (16, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (17, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (20, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (21, 2);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (1, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (5, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (12, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (13, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (14, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (15, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (20, 3);
INSERT INTO vov_database.product_category (product_id, category_id) VALUES (21, 3);

# Adding requests for products (already approved)
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (2, null, 3, 1, 2, '2023-06-02 14:06:36', '2023-06-02 14:06:39');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (2, null, 3, 2, 2, '2023-06-02 14:06:57', '2023-06-02 14:06:59');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (2, null, 3, 3, 2, '2023-06-02 14:07:08', '2023-06-02 14:07:09');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (2, null, 8, 4, 2, '2023-06-03 18:39:48', '2023-06-04 10:29:06');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (2, null, 8, 5, 2, '2023-06-03 18:43:19', '2023-06-04 10:29:08');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (4, null, 8, 6, 2, '2023-06-03 18:54:35', '2023-06-04 10:29:09');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (4, null, 8, 7, 2, '2023-06-03 18:56:37', '2023-06-04 10:29:10');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (4, null, 8, 8, 2, '2023-06-03 18:58:29', '2023-06-04 10:29:11');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (4, null, 8, 9, 2, '2023-06-03 19:01:15', '2023-06-04 10:29:12');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (4, null, 8, 10, 2, '2023-06-03 19:04:22', '2023-06-04 10:29:13');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (7, null, 8, 11, 2, '2023-06-03 19:38:52', '2023-06-04 10:29:13');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (7, null, 8, 12, 2, '2023-06-03 19:40:13', '2023-06-04 10:29:14');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (7, null, 8, 13, 2, '2023-06-03 19:42:20', '2023-06-04 10:29:14');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (7, null, 8, 14, 2, '2023-06-03 19:43:10', '2023-06-04 10:29:14');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (7, null, 8, 15, 2, '2023-06-03 19:44:02', '2023-06-04 10:29:15');
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (2, null, 8, 16, 2, '2023-06-05 06:41:44', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (2, null, 8, 17, 2, '2023-06-05 06:46:03', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (4, null, 8, 18, 2, '2023-06-05 06:50:32', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (4, null, 8, 19, 2, '2023-06-05 06:52:38', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (7, null, 8, 20, 2, '2023-06-05 06:55:30', null);
INSERT INTO vov_database.add_product_request (seller_id, refuse_reason, moderator_id, product_data_id, request_status_id, creation_date, check_date) VALUES (7, null, 8, 21, 2, '2023-06-05 06:55:55', null);
