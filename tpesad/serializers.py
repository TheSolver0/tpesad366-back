from rest_framework import serializers
from .models import Book,Author,Produit,Fournisseur,Client,Categorie,Mouvement

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

#----------------------------------------------------------------------------------------------------------------------------------------

class ProduitSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categ.libelle', read_only=True)
    class Meta:
        model = Produit
        fields = '__all__'

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class MouvementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mouvement
        fields = '__all__'