from django.db import models

# Create your models here.
class Calculator(models.Model):

    def compute(self, annual_income, filing_status, adjustments):
        return "computed"