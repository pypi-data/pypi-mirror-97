from marshmallow import Schema, fields


def create_schema(application):
    class ScriveCredentialsSchema(Schema):
        apitoken = fields.Str(
            title="API Token / Client Credentials Identifier",
            description='Can be found in your Scrive account under "Account" > "Integration Settings" > "Personal Access Credentials".  Example: 0c587256e43c4069_3003',
            required=True)
        apisecret = fields.Str(
            title="API Secret / Client Credentials Secret",
            description='Can be found in your Scrive account under "Account" > "Integration Settings" > "Personal Access Credentials".  Example: 3e9402ac3660674e',
            required=True)
        accesstoken = fields.Str(
            title="Access Token / Token Credentials Identifier",
            description='Can be found in your Scrive account under "Account" > "Integration Settings" > "Personal Access Credentials".  Example: 879fcbaf7c95fe94_6523',
            required=True)
        accesssecret = fields.Str(
            title="Access Secret / Token Credentials Secret",
            description='Can be found in your Scrive account under "Account" > "Integration Settings" > "Personal Access Credentials".  Example: 2bd1bdda9c126a1d',
            required=True)

        class Meta:
                ordered = True

    class ConfigSchema(Schema):
        limeHost = fields.URL(
            title="Lime - Host",
            description="The host of this Lime instance. This needs to be publically accessible. E.g. https://your-lime-instance.com/solution-hello-world",
            required=True)
        limeApiKey =  fields.Str(
            title="Lime - API Key",
            description="An API key to this Lime instance. E.g. 671B538EAC72ED527938D7968BAD9F05C876ACE67F902CA6F35892FC79318F48F7CC533F0AE8EDD27A13",
            required=True)
        scriveHost = fields.URL(
            title="Scrive - Host",
            description="The host of this add-on. E.g. https://lime.scrive.com",
            default="https://lime.scrive.com",
            required=True)
        scriveCredentials = fields.Nested(
            title="Scrive - Personal Access Credentials",
            description="The credentials are only used to fetch information about your Scrive account in order to configure this add-on. These credentials are not used to send documents.",
            nested=ScriveCredentialsSchema(),
            inline=True,
            required=True)

        class Meta:
                ordered = True

    return ConfigSchema()
