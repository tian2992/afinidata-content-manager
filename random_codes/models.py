from django.db import models
import random
import string


class Code(models.Model):
    code = models.CharField(max_length=255, null=True, unique=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_random_code()
        return super(Code, self).save(*args, **kwargs)

    def generate_random_code(self):
        random_code = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(7)])
        random_code = random_code.lower()
        print(random_code)
        if Code.objects.filter(code=random_code).count() > 0:
            return self.generate_random_code()
        else:
            return random_code

    def __str__(self):
        return self.code
