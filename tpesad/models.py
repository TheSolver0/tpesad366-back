from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

TYPE_CHOICES = [
    ('ENTREE', 'Entrée'),
    ('SORTIE', 'Sortie'),
]
ROLES_CHOICES = [
    ('CLIENT', 'Client'),
    ('FOURNISSEUR', 'Fournisseur'),
    ('GERANT', 'Gérant'),
    ('ADMIN', 'Admin'),
]
STATUT_CHOICES = [
    ('EN_ATTENTE', 'En attente'),
    ('PREPAREE', 'Préparée'),
    ('EXPEDIEE', 'Expédiée'),
    ('LIVREE', 'Livrée'),
    ('ANNULEE', 'Annulée'),
]

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L’adresse email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Pour accès admin
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom']

    objects = UserManager()

    def __str__(self):
        return self.email


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class Categorie(TimeStampedModel):
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return self.libelle


class Produit(TimeStampedModel):
    nom = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    categ = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    qte = models.IntegerField()
    pu = models.FloatField()
    seuil = models.IntegerField()

    def __str__(self):
        return self.nom


class UserTPE(TimeStampedModel):
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    role = models.CharField(max_length=30, choices=ROLES_CHOICES, default='GERANT')
    produits = models.ManyToManyField(Produit, related_name='fournisseurs', blank=True)
    delai_livraison = models.DurationField(default=timedelta(days=3))

    def __str__(self):
        return self.nom


class Mouvement(TimeStampedModel):
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    qte = models.IntegerField()
    user = models.ForeignKey(UserTPE, on_delete=models.CASCADE, null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    produits = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.qte}"


class BaseCommande(TimeStampedModel):
    produits = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qte = models.IntegerField()
    statut = models.CharField(max_length=30, choices=STATUT_CHOICES, default='EN_ATTENTE')
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.produits and self.qte:
            self.montant = self.produits.pu * self.qte
        super().save(*args, **kwargs)

    def clean(self):
        if not self.produits or not self.qte:
            raise ValidationError("La commande doit contenir un produit et une quantité valide.")


class CommandeClient(BaseCommande):
    client = models.ForeignKey(UserTPE, on_delete=models.CASCADE, null=True, limit_choices_to={'role': 'CLIENT'})

    def __str__(self):
        return f"Commande client #{self.id} | {self.qte} x {self.produits.nom} | {self.client.nom}"

    def clean(self):
        super().clean()
        if not self.client:
            raise ValidationError("La commande doit être adressée à un client.")


class CommandeFournisseur(BaseCommande):
    fournisseur = models.ForeignKey(UserTPE, on_delete=models.CASCADE, null=True, limit_choices_to={'role': 'FOURNISSEUR'})

    def __str__(self):
        return f"Commande fournisseur #{self.id} | {self.qte} x {self.produits.nom} | {self.fournisseur.nom}"

    def clean(self):
        super().clean()
        if not self.fournisseur:
            raise ValidationError("La commande doit être adressée à un fournisseur.")
