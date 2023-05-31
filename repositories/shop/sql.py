INSERT_INTO_SHOP_DATA = """
    INSERT INTO shop_data(name, description)
    VALUES (%s, %s) /* here should be input data from createShopForm */
"""
INSERT_INTO_SHOP = """
    INSERT INTO shop (seller_id,shop_data_id) 
    VALUES (%s,%s)
"""
SELECT_GET_SHOP = """
    SELECT * FROM  shop_data;
"""
# Данные для вставки
shop_data_values = ("Shop name", "Description")
shop_values = ("Shop name", "Description")

SELECT_SHOP_BY_SELLER = """
SELECT sd.name AS name, sd.description, sd.approved AS description
FROM shop AS s
JOIN shop_data AS sd ON s.shop_data_id = sd.id
WHERE s.seller_id = %s;
"""




