CREATE_ORDER = """
INSERT INTO `order` (status_id, customer_id, creation_date) VALUES 
((SELECT order_status.id FROM order_status WHERE order_status.name = %s), %s, %s);
"""

CREATE_ORDER_ITEM = """
INSERT INTO order_item (order_id, count, price, product_id, status_id) 
VALUES (%s, %s, %s, %s, (SELECT order_item_status.id FROM order_item_status WHERE order_item_status.name = %s));
"""

GET_ORDER_IDS_FOR_USER = """
SELECT id FROM `order` AS ord WHERE ord.customer_id = %s;
"""

GET_ORDER_BY_ID = """
SELECT ord.id, ord.customer_id, ord.creation_date, order_status.name as status_name 
FROM `order` AS ord JOIN order_status ON ord.status_id = order_status.id WHERE ord.id = %s;
"""

GET_ORDER_ITEMS_BY_ORDER_ID = """
SELECT * FROM order_item JOIN product ON order_item.product_id = product.id
JOIN product_data ON product.product_data_id = product_data.id
JOIN order_item_status ON order_item.status_id = order_item_status.id
WHERE order_item.order_id = 10;
"""