INSERT_INTO_SHOP_DATA = """
    INSERT INTO shop_data(name, description)
    VALUES (%s, %s) 
"""
INSERT_INTO_SHOP = """
    INSERT INTO shop (seller_id,shop_data_id) 
    VALUES (%s,%s)
"""
SELECT_GET_SHOP = """
    SELECT * FROM  shop_data;
"""
SELECT_SHOP_BY_SELLER = """
SELECT sd.name AS name, sd.description, sd.approved AS description
FROM shop AS s
JOIN shop_data AS sd ON s.shop_data_id = sd.id
WHERE s.seller_id = %s;
"""
UPDATE_SHOP_DATA_ID = """
UPDATE shop SET shop_data_id = %s
WHERE seller_id=%s
"""



