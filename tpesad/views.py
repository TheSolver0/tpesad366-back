from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book, Author, Produit,Fournisseur,Client,Categorie,Mouvement,Commande
from .serializers import BookSerializer, AuthorSerializer, ProduitSerializer, FournisseurSerializer, ClientSerializer, CategorieSerializer, MouvementSerializer, CommandeSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = (IsAuthenticated, )

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # permission_classes = (IsAuthenticated, )

#-------------------------------------------------------------------------------------------------------------------------------

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class MouvementViewSet(viewsets.ModelViewSet):
    queryset = Mouvement.objects.all()
    serializer_class = MouvementSerializer
    
class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    