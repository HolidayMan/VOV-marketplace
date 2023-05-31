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
