from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

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
    ('PREPAREE', 'Preparée'),
    ('EXPEDIEE', 'Expediée'),
    ('LIVREE', 'Livrée'),
    ('ANNULEE', 'Annulée'),
]
def clean(self):
    if not self.userC and not self.userF:
        raise ValidationError("Une commande doit être adressée soit à un client, soit à un fournisseur.")

class Author(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom


class Book(models.Model):
    title = models.CharField(max_length=32, unique=True)
    quantity = models.IntegerField(default=1)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
    role= models.CharField(max_length=30, choices=ROLES_CHOICES, default='GERANT')
    produits = models.ManyToManyField(Produit, related_name='fournisseurs', blank=True)
    delai_livraison = models.DurationField(default=timedelta(days=3))
    def __str__(self):
        return self.nom



class Mouvement(TimeStampedModel):
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    qte = models.IntegerField()
    user = models.ForeignKey(UserTPE, on_delete=models.CASCADE, null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    produits =  models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True, blank=True)

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

class CommandeClient(BaseCommande):
    client = models.ForeignKey(UserTPE, on_delete=models.CASCADE,null=True, limit_choices_to={'role': 'CLIENT'})

    def __str__(self):
        return f"Commande client #{self.id} | {self.qte} x {self.produits.nom} | {self.client.nom}"
class CommandeFournisseur(BaseCommande):
    fournisseur = models.ForeignKey(UserTPE, on_delete=models.CASCADE,null=True, limit_choices_to={'role': 'FOURNISSEUR'})

    def __str__(self):
        return f"Commande fournisseur #{self.id} | {self.qte} x {self.produits.nom} | {self.fournisseur.nom}"

