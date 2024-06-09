from django.db import models


class ProductModel(models.Model):
    name = models.CharField(max_length=128, default="Unknown product")
    inner_name = models.CharField(max_length=32, default=None)
    status = models.IntegerField(default=0)

    def __str__(self):
        str_status: str = "Unknown"
        if self.status == 1:
            str_status = "Safe"
        elif self.status == 2:
            str_status = "Detected"

        return f"[{self.name}] {self.inner_name} -> Status: {str_status}"
