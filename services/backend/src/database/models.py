from tortoise import fields, models

class UserRoles(models.Model):
    id = fields.IntField(pk=True)
    role = fields.CharField(max_length=50, unique=True)
    label = fields.CharField(max_length=100, null=True)

class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    full_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    role = fields.ForeignKeyField("models.UserRoles", related_name="user", null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

class Notes(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=225, null=False)
    content = fields.TextField()
    author = fields.ForeignKeyField("models.Users", related_name="note")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}, {self.author_id} on {self.created_at}"

