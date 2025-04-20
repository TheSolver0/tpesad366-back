from rest_framework import serializers
from .models import Book,Author,Produit,Fournisseur,Client,Categorie,Mouvement,Commande

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

class CommandeSerializer(serializers.ModelSerializer):
    produits = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all())
    produits_details = ProduitSerializer(source='produits', read_only=True)

    userF = serializers.PrimaryKeyRelatedField(queryset=Fournisseur.objects.all(), required=False, allow_null=True)
    userF_details = FournisseurSerializer(source='userF', read_only=True)

    userC = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), required=False, allow_null=True)
    userC_details = ClientSerializer(source='userC', read_only=True)

    type_commande = serializers.SerializerMethodField()

    class Meta:
        model = Commande
        fields = [
            'id',
            'produits', 'produits_details',
            'qte',
            'userF', 'userF_details',
            'userC', 'userC_details',
            'statut',
            'type_commande',
            'montant',
        ]
        read_only_fields = ['montant']

    def get_type_commande(self, obj):
        return obj.type_commande
