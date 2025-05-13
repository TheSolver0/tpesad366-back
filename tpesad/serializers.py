from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Produit,Categorie,Mouvement,CommandeClient, CommandeFournisseur,UserTPE, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nom']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Identifiants invalides")
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'nom', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            nom=validated_data['nom'],
            password=validated_data['password']
        )
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
    user_details = UserTPESerializer(source='user', read_only=True)
    produit_details = ProduitSerializer(source='produits', read_only=True)

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
    fournisseur_details = UserTPESerializer(source='fournisseur', read_only=True)
    produits_details = ProduitSerializer(source='produits', read_only=True)

    class Meta(CommandeBaseSerializer.Meta):
        model = CommandeFournisseur
        fields = CommandeBaseSerializer.Meta.fields + ['fournisseur','created_at','updated_at', 'produit_nom', 'fournisseur_details', 'produit_pu', 'produits_details']

