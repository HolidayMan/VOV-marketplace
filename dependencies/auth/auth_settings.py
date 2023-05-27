from auth.dependencies import get_current_user, get_user_role, verify_customer, verify_moderator, verify_seller, \
    require_auth, require_role

# verify_customer = fake_verify_customer
# verify_seller = fake_verify_seller
# verify_moderator = fake_verify_moderator
# get_user_role = fake_get_user_role
# get_user = fake_get_user

get_user = get_current_user
