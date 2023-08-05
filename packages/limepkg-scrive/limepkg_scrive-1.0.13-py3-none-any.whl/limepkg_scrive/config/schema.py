from marshmallow import Schema, fields


def create_schema(application):
    class ConfigSchema(Schema):
        scriveHost = fields.URL(default="https://lime.scrive.com", required=True)
        scriveClientCredentialsIdentifier = fields.Str(required=True)
        scriveClientCredentialsSecret = fields.Str(required=True)
        scriveTokenCredentialsIdentifier = fields.Str(required=True)
        scriveTokenCredentialsSecret = fields.Str(required=True)
        limeHost = fields.URL(required=True)
        limeApiKey =  fields.Str(required=True)

    return ConfigSchema()
