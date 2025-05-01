from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book, Author, Produit,UserTPE,Categorie,Mouvement,CommandeClient,CommandeFournisseur
from .serializers import BookSerializer, AuthorSerializer, ProduitSerializer,UserTPESerializer,CategorieSerializer, MouvementSerializer, CommandeFournisseurSerializer, CommandeClientSerializer

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

class UserTPEViewSet(viewsets.ModelViewSet):
    queryset = UserTPE.objects.all()
    serializer_class = UserTPESerializer
class ClientViewSet(viewsets.ModelViewSet):
    queryset = UserTPE.objects.filter(role='CLIENT')
    serializer_class = UserTPESerializer

class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = UserTPE.objects.filter(role='FOURNISSEUR')
    serializer_class = UserTPESerializer

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class MouvementViewSet(viewsets.ModelViewSet):
    queryset = Mouvement.objects.all()
    serializer_class = MouvementSerializer
    
class CommandeClientViewSet(viewsets.ModelViewSet):
    queryset = CommandeClient.objects.all()
    serializer_class = CommandeClientSerializer

class CommandeFournisseurViewSet(viewsets.ModelViewSet):
    queryset = CommandeFournisseur.objects.all()
    serializer_class = CommandeFournisseurSerializer
    