from django.db import models

# Create your models here.
class Payments(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.TextField(null=True, blank=True)
    payment_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student} - {self.amount}"
    
class PaymentHistory(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    payment = models.ForeignKey('payments.Payments', on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.payment}"
    
