from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Str(dump_only=True, validate=validate.Length(max=32))
    email = fields.Email(
        required=True, error_messages={"required": "Email is required."})
    firstName = fields.Str(validate=validate.Length(min=2, max=128),)
    lastName = fields.Str(validate=validate.Length(min=2, max=128),)
    password = fields.Str(
        validate=validate.Length(min=6, max=255),
        required=True,
        load_only=True,
        error_messages={"required": "Password is required."}
    )
    phone = fields.Str(validate=validate.Length(equal=11))
    address = fields.Str(validate=validate.Length(min=6, max=255))
    photo = fields.Url(validate=validate.Length(max=255))
    created_on = fields.DateTime(dump_only=True)
    updated_on = fields.DateTime(dump_only=True)


class AuthSchema(Schema):
    firstName = fields.Str(
        validate=validate.Length(min=3, max=255),
        required=True,
        error_messages={"required": "full name is required."}
    )
    lastName = fields.Str(
        validate=validate.Length(min=2, max=128),
        required=True,
        error_messages={"required": "Name is required."}
    )
    phone = fields.Str(
        validate=validate.Length(min=2, max=128),
        required=True,
        error_messages={"required": "Name is required."}
    )
    password = fields.Str(
        validate=validate.Length(min=3, max=128),
        required=True,
        error_messages={"required": "Password is required."}
    )
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required."}
    )


class ProductSchema(Schema):
    id = fields.Str(dump_only=True, validate=validate.Length(max=32))
    name = fields.Str(required=True, validate=validate.Length(max=255))
    slug = fields.Str(required=True, validate=validate.Length(max=255))
    category = fields.Str(required=True, validate=validate.Length(max=25))
    sub_category = fields.Str(required=True, validate=validate.Length(max=25))
    price = fields.Int(required=True, )
    colors = fields.Str()
    sizes = fields.Str()
    images = fields.Str()
    description = fields.Str()
    inventory = fields.Int()
    discount = fields.Int()
    # merchant = fields.Nested('MerchantSchema', only=(
        # 'id', 'name',), dump_only=True,)