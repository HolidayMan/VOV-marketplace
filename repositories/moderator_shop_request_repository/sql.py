GET_SHOP_REQUESTS_LIST = """
SELECT shop_data_id, seller_id, rs.name AS status_name, refuse_reason, creation_date, check_date,
       sd.name AS shop_name, description, approved
FROM create_shop_request
JOIN shop_data sd ON sd.id = create_shop_request.shop_data_id
JOIN request_status rs ON rs.id = create_shop_request.request_status_id;
"""

GET_SHOP_REQUEST = """
SELECT  shop_data_id, seller_id, rs.name AS status_name, refuse_reason, creation_date, check_date,
       sd.name AS shop_name, description, approved
FROM create_shop_request
JOIN shop_data sd ON sd.id = create_shop_request.shop_data_id
JOIN request_status rs ON rs.id = create_shop_request.request_status_id
WHERE shop_data_id=%s
"""

UPDATE_SHOP_REQUEST_STATUS_BY_SHOP_DATA_ID = """
UPDATE create_shop_request
SET request_status_id = (SELECT request_status.id FROM request_status WHERE request_status.name = %s),
    refuse_reason = %s,
    check_date = %s
WHERE shop_data_id = %s;
"""

APPROVE_SHOP_REQUEST = """
UPDATE create_shop_request
SET request_status_id = (SELECT id FROM request_status WHERE name = 'accepted'),
    moderator_id =%s, check_date = %s 
WHERE shop_data_id =%s;
"""

DECLINE_SHOP_REQUEST = """
UPDATE create_shop_request
SET request_status_id = (SELECT id FROM request_status WHERE name = 'declined'),
    refuse_reason = %s, moderator_id =%s , check_date = %s
WHERE shop_data_id =%s;
"""