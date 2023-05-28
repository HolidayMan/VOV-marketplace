SELECT_USER_BY_ID = """
SELECT user.id, user.name, email, password, role.name as role FROM user
JOIN user_role role ON user.role_id = role.id
WHERE user.id = %s;
"""
