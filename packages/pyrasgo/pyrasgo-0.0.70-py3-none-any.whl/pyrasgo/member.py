import os


class Member(object):

    def __init__(self, api_object):
        self._api_object = api_object

    def id(self):
        return self._api_object["id"]

    def organization_id(self):
        return self._api_object["organizationId"]
    
    def organization_prefix(self):
        org = self._api_object.get("organization", {})
        org_prefix = org.get("code", None)
        if org_prefix:
            return org_prefix
        else:
            raise ValueError('Your organization is missing credentials, please contact Rasgo support.')

    def organization_admin_role(self):
        return f"{self.organization_prefix()}ADMIN" or None

    def organization_publisher_role(self):
        return f"{self.organization_prefix()}PUBLISHER" or None

    def organization_reader_role(self):
        return f"{self.organization_prefix()}READER" or None

    def user_name(self):
        un = self._api_object.get("snowUsername", os.environ.get('SNOWFLAKE_USERNAME', None))
        if un:
            return un
        else:
            raise ValueError('Your user is missing credentials, please contact Rasgo support.')

    def user_role(self):
        return f"{self.organization_prefix()}_{self.user_name()}" or None

    def snowflake_creds(self):
        org = self._api_object.get("organization", {})
        return {
            "user": self.user_name(),
            "password": self._api_object.get("snowPassword", os.environ.get('SNOWFLAKE_PASSWORD', None)),
            "account": org.get("account", os.environ.get("SNOWFLAKE_ACCOUNT")),
            "database": org.get("database", os.environ.get("SNOWFLAKE_DATABASE")),
            "schema": org.get("schema", os.environ.get("SNOWFLAKE_SCHEMA")),
            "warehouse": org.get("warehouse", os.environ.get("SNOWFLAKE_WAREHOUSE")),
            "role": self._api_object.get("role", os.environ.get("SNOWFLAKE_ROLE")) or self.user_role() or self.organization_reader_role() or "PUBLIC"
        }
