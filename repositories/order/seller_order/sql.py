GET_ORDER_ITEMS_BY_SELLER_ID = """
SELECT refuse_reason, product_id, p.price AS product_price,
       product_data_id, pd.name as product_name, description, image_file_path,
       approved, order_item.price AS item_price, check_date,
       ois.name AS status_name, count, order_id, creation_date
       FROM order_item
    JOIN product p ON order_item.product_id = p.id
    JOIN `order` o ON o.id = order_item.order_id
    JOIN product_data pd ON p.product_data_id = pd.id
    JOIN order_item_status ois ON order_item.status_id = ois.id
    WHERE p.seller_id = %s ORDER BY o.creation_date;
"""

GET_ORDER_ITEM_BY_ORDER_AND_PRODUCT_IDS = """
SELECT refuse_reason, product_id, p.price AS product_price,
       product_data_id, pd.name as product_name, description, image_file_path,
       approved, order_item.price AS item_price, check_date,
       ois.name AS status_name, count, order_id, creation_date
       FROM order_item
    JOIN product p ON order_item.product_id = p.id
    JOIN `order` o ON o.id = order_item.order_id
    JOIN product_data pd ON p.product_data_id = pd.id
    JOIN order_item_status ois ON order_item.status_id = ois.id
    WHERE o.id = %s AND p.id = %s;
"""

UPDATE_ORDER_ITEM_BY_ORDER_AND_PRODUCT_IDS = """
UPDATE order_item SET order_item.status_id =
    (SELECT order_item_status.id FROM order_item_status WHERE order_item_status.name = %s),
    order_item.check_date = %s,
    order_item.refuse_reason = %s
    WHERE order_item.order_id = %s AND order_item.product_id = %s;
"""

GET_SELLER_ID_BY_PRODUCT_ID = """
SELECT product.seller_id FROM product WHERE product.id = %s;
"""

GET_NOT_PROCESSED_ORDER_ITEMS_BY_SELLER_ID = """
SELECT refuse_reason, product_id, p.price AS product_price,
       product_data_id, pd.name as product_name, description, image_file_path,
       approved, order_item.price AS item_price, check_date,
       ois.name AS status_name, count, order_id, creation_date
       FROM order_item
    JOIN product p ON order_item.product_id = p.id
    JOIN `order` o ON o.id = order_item.order_id
    JOIN product_data pd ON p.product_data_id = pd.id
    JOIN order_item_status ois ON order_item.status_id = ois.id
    WHERE p.seller_id = %s AND order_item.status_id = (SELECT order_item_status.id
                                                      FROM order_item_status
                                                      WHERE order_item_status.name = 'in_process')
    ORDER BY o.creation_date;
"""
