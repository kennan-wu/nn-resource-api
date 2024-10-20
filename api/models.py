from django.db import models
import uuid

class NeuralNetwork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    input_shape = models.JSONField()
    layers = models.JSONField()
    created_on = models.DateTimeField("date created", auto_now_add=True)
    last_updated = models.DateTimeField("date last updated", auto_now=True)

    def __str__(self) -> str:
        return self.name
