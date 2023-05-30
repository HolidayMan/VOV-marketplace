INSERT_INTO_SHOP_DATA = """
    INSERT INTO shop_data(name, description)
    VALUES (%s, %s) /* here should be input data from createShopForm */
"""
INSERT_INTO_SHOP = """
    INSERT INTO shop (seller_id,shop_data_id) 
    VALUES (%s,%s)
"""

# Данные для вставки
shop_data_values = ("Shop name", "Description")
shop_values = ("Shop name", "Description")

