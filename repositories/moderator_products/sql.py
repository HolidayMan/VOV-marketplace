SELECT_OPEN_PRODUCT_REQUESTS = """
SELECT seller_id, product_data_id as id, product_data.name, product_data.approved, refuse_reason, 
product_data.description, product_data.image_file_path, request_status.name as request_status_name, 
moderator_id, creation_date, check_date
       FROM add_product_request
JOIN product_data ON product_data_id = product_data.id
JOIN request_status ON request_status_id = request_status.id
WHERE request_status.name = 'in_process' AND product_data.approved = 0;
"""

DECLINE_PRODUCT_REQUEST = """
UPDATE add_product_request SET request_status_id = (SELECT id FROM request_status WHERE name = 'declined'),
                               refuse_reason = %s, moderator_id = %s WHERE product_data_id = %s;
"""


ACCEPT_PRODUCT_REQUEST = """
UPDATE add_product_request SET request_status_id = (SELECT id FROM request_status WHERE name = 'accepted'),
                                 moderator_id = %s WHERE product_data_id = %s;
"""
