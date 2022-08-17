from tortoise import fields, models


class GGAUser(models.Model):
    id = fields.IntField(pk=True)
    time = fields.DatetimeField()
    name = fields.CharField(max_length=50)
    session = fields.CharField(max_length=50)
    state = fields.IntField()
    h = fields.FloatField()
    b = fields.FloatField()
    l = fields.FloatField()
    satellite = fields.IntField()
    dop = fields.FloatField()
    delay = fields.IntField()

    class Meta:
        table = "gga"
