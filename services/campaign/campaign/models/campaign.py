from django.db import models


class Campaign(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    title = models.CharField(
        max_length=100,
    )
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    goal_amount = models.IntegerField()
    current_amount = models.IntegerField(
        null=True,
        blank=True,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    creator_id = models.BigIntegerField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title}: {self.start_date} to {self.end_date}. Goal: {self.goal_amount} ~> Current: {self.current_amount}'
