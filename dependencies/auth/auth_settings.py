from dependencies.auth.fakes import fake_get_user, fake_get_user_role, fake_verify_customer, fake_verify_seller, \
    fake_verify_moderator

verify_customer = fake_verify_customer
verify_seller = fake_verify_seller
verify_moderator = fake_verify_moderator
get_user_role = fake_get_user_role
get_user = fake_get_user
