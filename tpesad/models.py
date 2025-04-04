from django.db import models
TYPE_CHOICES = [
    ('ENTREE', 'Entrée'),
    ('SORTIE', 'Sortie'),
]
class Author(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom


class Book(models.Model):
    title = models.CharField(max_length=32, unique=True)
    quantity = models.IntegerField(default=1)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Categorie(models.Model):
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return self.libelle


class Produit(models.Model):
    nom = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    categ = models.ForeignKey(Categorie, on_delete=models.DO_NOTHING)
    qte = models.IntegerField()
    pu = models.FloatField()
    seuil = models.IntegerField()

    def __str__(self):
        return self.nom


class Fournisseur(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom


class Client(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom


class Mouvement(models.Model):
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    qte = models.IntegerField()
    userF = models.ForeignKey(Fournisseur, on_delete=models.DO_NOTHING)
    userC = models.ForeignKey(Client, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.type} - {self.qte}"
