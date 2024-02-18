"""
Things to be used across the entire application
"""
###############################################################################
# Constants
###############################################################################
USERNAME = 'username'


###############################################################################
# TEMPLATES
###############################################################################
# index
INDEX_TEMPLATE = "main/templates/home_page/index.html"

# profile
NEW_USER_FORM_TEMPLATE = "main/templates/profile/new_user_form.html"
USER_PROFILE_TEMPLATE = "main/templates/profile/user_profile.html"
LOGIN_FORM_TEMPLATE = "main/templates/profile/login_form.html"
FORGOT_USERNAME_FORM_TEMPLATE = "main/templates/profile/forgot_username_form.html"
FORGOT_PASSWORD_FORM_TEMPLATE = "main/templates/profile/forgot_password_form.html"
FORGOT_USERNAME_EMAIL = "main/templates/profile/forgot_username_email.html"
PASSWORD_RESET_EMAIL_FORM_TEMPLATE = (
    "main/templates/profile/password_reset_email_form.html"
)
PASSWORD_RESET_CONFIRM_FORM_TEMPLATE = (
    "main/templates/profile/password_reset_confirm_form.html"
)
PASSWORD_RESET_EMAIL_SUBJECT_FILE = "main/templates/profile/password_reset_email_subject.txt"
PASSWORD_RESET_EMAIL_FORM_TEMPLATE = "main/templates/profile/password_reset_email_form.html"

# reviews
CREATE_REVIEW_FORM = "main/templates/reviews/create_review_form.html"
REVIEW_TEMPLATE = "main/templates/reviews/review.html"
