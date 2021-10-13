# We can make our application load this AppConfig subclass by default by
# specifying the 'default_app_config' in the polls/__init__.py
default_app_config = 'polls.apps.PollsConfig'
#
# Doing this will cause PollConfig to be used when INSTALLED_APPS just contaion 'polls'.
# This allows us to make use of AppConfig features without requiring our uses to update their INSTALLED_APPS setting 