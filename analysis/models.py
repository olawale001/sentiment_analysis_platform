from django.db import models

class SentimentAnalysis(models.Model):
    text = models.TextField()
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    sentiment = models.CharField(max_length=20)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50] if self.text else f"File {self.file.name}"
