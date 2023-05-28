SELECT_USER_BY_ID = """
SELECT user.id, user.name, email, password, role.name as role FROM user
JOIN user_role role ON user.role_id = role.id
WHERE user.id = %s;
"""

SELECT_USER_BY_EMAIL_AND_ROLE = """
SELECT user.id, user.name, email, password, role.name as role FROM user
                                          JOIN user_role role ON user.role_id = role.id
                                          WHERE user.email = %s AND role.name = %s;
"""

INSERT_NEW_USER = """
INSERT INTO user (name, email, password, role_id) VALUES (%s, %s, %s, 
                                                          (SELECT id FROM user_role WHERE name = %s));
"""

UPDATE_USER = """
UPDATE user SET name = %s, email = %s, password = %s,
              role_id = (SELECT id FROM user_role WHERE name = %s)
              WHERE id = %s;
"""

DELETE_USER = "DELETE FROM user WHERE id = %s;"
