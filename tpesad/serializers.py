from rest_framework import serializers
from .models import Book,Author,Produit,Categorie,Mouvement,CommandeClient, CommandeFournisseur,UserTPE
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

class UserTPESerializer(serializers.ModelSerializer):
    produits_details = ProduitSerializer(source='produits', many=True, read_only=True)
    class Meta:
        model = UserTPE
        fields = '__all__'


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class MouvementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mouvement
        fields = '__all__'



class CommandeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'produits', 'qte', 'statut', 'montant']
        read_only_fields = ['montant']
class CommandeClientSerializer(CommandeBaseSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=UserTPE.objects.filter(role='CLIENT'))
    produit_nom = serializers.CharField(source='produits.nom', read_only=True)
    produit_pu = serializers.CharField(source='produits.pu', read_only=True)
    client_nom = serializers.CharField(source='client.nom', read_only=True)
    produits_details = ProduitSerializer(source='produits', read_only=True)

    class Meta(CommandeBaseSerializer.Meta):
        model = CommandeClient
        fields = CommandeBaseSerializer.Meta.fields + ['client', 'produit_nom', 'client_nom', 'produit_pu', 'produits_details']

class CommandeFournisseurSerializer(CommandeBaseSerializer):
    fournisseur = serializers.PrimaryKeyRelatedField(queryset=UserTPE.objects.filter(role='FOURNISSEUR'))
    produit_nom = serializers.CharField(source='produits.nom', read_only=True)
    produit_pu = serializers.CharField(source='produits.pu', read_only=True)
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True)
    produits_details = ProduitSerializer(source='produits', read_only=True)

    class Meta(CommandeBaseSerializer.Meta):
        model = CommandeFournisseur
        fields = CommandeBaseSerializer.Meta.fields + ['fournisseur', 'produit_nom', 'fournisseur_nom', 'produit_pu', 'produits_details']

