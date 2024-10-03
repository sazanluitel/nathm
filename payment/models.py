from django.db import models
 
class PaymentHistory(models.Model):
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.amount} - {self.status}"

