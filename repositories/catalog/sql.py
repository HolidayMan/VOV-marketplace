SELECT_APPROVED_PRODUCTS = """
SELECT product.id, product.seller_id, product.price, product_data.id as product_data_id,
       product_data.name, product_data.description, product_data.image_file_path
FROM product JOIN product_data ON product.product_data_id = product_data.id WHERE product_data.approved = TRUE;
"""

SELECT_CATEGORIES = """
SELECT * FROM category;
"""

SELECT_APPROVED_PRODUCTS_WITH_CATEGORY = """
SELECT product.id, product.seller_id, product.price, product_data.id as product_data_id,
       product_data.name, product_data.description, product_data.image_file_path
FROM product JOIN product_data ON product.product_data_id = product_data.id WHERE product_data.approved = TRUE
AND product.id IN (SELECT product.id FROM product INNER JOIN product_category
    ON product.id = product_category.product_id INNER JOIN category
    WHERE product_category.category_id = (SELECT category.id FROM category WHERE category.name = %s));
"""

