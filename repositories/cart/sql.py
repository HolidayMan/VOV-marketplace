SELECT_CART_ITEMS = """
SELECT * FROM cart_item JOIN product ON cart_item.product_id = product.id
                        JOIN product_data ON product.product_data_id = product_data.id
                        WHERE cart_item.customer_id = %s;
"""

INSERT_CART_ITEM = """
INSERT INTO cart_item (count, product_id, customer_id) VALUES (%s, %s, %s);
"""

DELETE_CART_ITEM = """
DELETE FROM cart_item WHERE cart_item.customer_id = %s AND cart_item.product_id = %s;
"""

GET_CART_ITEM = """
SELECT * FROM cart_item WHERE cart_item.customer_id = %s AND cart_item.product_id = %s;
"""