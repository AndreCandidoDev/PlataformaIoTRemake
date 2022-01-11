from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=11)

    # apenas para usuario gratuito, para outros planos são irrelevantes
    device_limit_creation = models.IntegerField(null=True, blank=True, default=20)
    devices_created = models.IntegerField(null=True, blank=True, default=0)
    # add another fields here if required

    # Haverá limite para criação de redes em usuarios pago
    # todo: planejar cobranças para isso
    network_limit_creation = models.IntegerField(null=True, blank=True, default=0)
    networks_created = models.IntegerField(null=True, blank=True, default=0)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)
    endereco_completo = models.CharField(max_length=255)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['id']

    def __str__(self):
        return str(self.user)


class Plano(models.Model):
    tipos_planos = (
        ('Pessoal', 'Pessoal'),
        ('Empresarial', 'Empresarial'),
        # ('Pago_personalizado', 'Pago_personalizado')  # será implementado depois
    )

    periodos = (
        ('Trimestral', '3 meses'),
        ('Semestral', '6 meses'),
        ('anual', '1 ano')
    )

    usuario = models.ForeignKey(Account, on_delete=models.CASCADE)
    perfil = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    plano = models.CharField(max_length=255, choices=tipos_planos, default='Pessoal')
    periodo = models.CharField(max_length=255, default='Trimestral', choices=periodos)
    limite_redes_iot = models.IntegerField(default=3)
    limite_dispositivos_iot = models.IntegerField(default=30)
    ativo = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['id']

    def __str__(self):
        return f'{self.usuario} plano {self.plano}'

# Plano --> define o tipo de plano e seus limites (será passado pela view)
