INSERT_PRODUCT_DATA = """
INSERT INTO product_data (name, description, approved, image_file_path) VALUES (%s, %s, %s, %s);
"""

INSERT_ADD_PRODUCT_REQUEST = """
INSERT INTO add_product_request (seller_id, refuse_reason, moderator_id, 
product_data_id, request_status_id, check_date)
VALUES (%s, %s, %s, %s, (SELECT id FROM request_status WHERE name = %s), %s);
"""

INSERT_PRODUCT = """
INSERT INTO product (price, product_data_id, seller_id) VALUES (%s, %s, %s);
"""

INSERT_PRODUCT_CATEGORIES = """
INSERT INTO product_category (product_id, category_id) VALUES (%s, %s);
"""

SELECT_PRODUCTS_BY_SELLER_ID = """
SELECT product.id as id, price, product.product_data_id as product_data_id, pd.name as name, pd.description as description,
       pd.image_file_path as image_file_path, pd.approved, rs.name as request_status_name
FROM product
    JOIN product_data pd ON pd.id = product.product_data_id
INNER JOIN add_product_request apr ON product.product_data_id = apr.product_data_id
INNER JOIN request_status rs on apr.request_status_id = rs.id
WHERE product.seller_id = %s
"""

SELECT_PRODUCT_BY_ID = """
SELECT product.id as id, price, product.product_data_id, pd.name as name, pd.description as description,
       pd.image_file_path as image_file_path, pd.approved, pc.category_id as category_id, c.name as category_name,
       rs.name as request_status_name, product.seller_id as seller_id
FROM product
         JOIN product_data pd ON pd.id = product.product_data_id
         INNER JOIN product_category pc ON product.id = pc.product_id
         INNER JOIN category c ON pc.category_id = c.id
         INNER JOIN add_product_request apr ON product.product_data_id = apr.product_data_id
         INNER JOIN request_status rs on apr.request_status_id = rs.id
WHERE product.id = %s
ORDER BY product.id DESC;
"""
