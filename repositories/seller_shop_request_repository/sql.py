
CREATE_SHOP_REQUEST = """
INSERT INTO create_shop_request ( shop_data_id, request_status_id, 
creation_date, seller_id) VALUES ( %s, (SELECT request_status.id FROM request_status 
WHERE request_status.name=%s), %s, %s);
"""

GET_SHOP_REQUESTS = """
SELECT rs.name AS status_name, refuse_reason, creation_date, check_date,
       shop_data_id, sd.name AS shop_name, description,
       approved
FROM create_shop_request
JOIN shop_data sd ON sd.id = create_shop_request.shop_data_id
JOIN request_status rs ON rs.id = create_shop_request.request_status_id
WHERE seller_id = %s;
"""

