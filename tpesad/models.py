from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

TYPE_CHOICES = [
    ('ENTREE', 'Entrée'),
    ('SORTIE', 'Sortie'),
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


class Fournisseur(TimeStampedModel):
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom


class Client(TimeStampedModel):
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom


class Mouvement(TimeStampedModel):
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    qte = models.IntegerField()
    userF = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
    userC = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    produits =  models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        if self.userC and self.userF:
            raise ValidationError("Une commande ne peut pas être destinée à la fois à un client et à un fournisseur.")
        if not self.userC and not self.userF:
            raise ValidationError("Une commande doit être destinée soit à un client, soit à un fournisseur.")

    def save(self, *args, **kwargs):
        self.full_clean()  
      
        super().save(*args, **kwargs)
    @property
    def type_commande(self):
        if self.userC:
            return "client"
        elif self.userF:
            return "fournisseur"
        return "inconnu"

    def __str__(self):
        return f"{self.type} - {self.qte}"

class Commande(TimeStampedModel):
    produits =  models.ForeignKey(Produit, on_delete=models.CASCADE)
    qte = models.IntegerField()
    userF = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
    userC = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    statut = models.CharField(max_length=30, choices=STATUT_CHOICES, default='EN_ATTENTE' )
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def clean(self):
        if self.userC and self.userF:
            raise ValidationError("Une commande ne peut pas être destinée à la fois à un client et à un fournisseur.")
        if not self.userC and not self.userF:
            raise ValidationError("Une commande doit être destinée soit à un client, soit à un fournisseur.")

    def save(self, *args, **kwargs):
        self.full_clean()  
        if self.produits and self.qte:
            self.montant = self.produits.pu * self.qte
        super().save(*args, **kwargs)
    @property
    def type_commande(self):
        if self.userC:
            return "client"
        elif self.userF:
            return "fournisseur"
        return "inconnu"

    def __str__(self):
        cible = self.userC or self.userF
        type_cible = "Client" if self.userC else "Fournisseur"
        return f"Commande #{self.id} | {self.qte} x {self.produits.nom} | {type_cible}: {cible.nom if cible else 'Inconnu'} | Statut: {self.statut}"
    