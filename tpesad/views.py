# from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework.permissions import IsAuthenticated
from .models import  Produit,UserTPE,Categorie,Mouvement,CommandeClient,CommandeFournisseur
from .serializers import LoginSerializer,RegisterSerializer, UserSerializer, ProduitSerializer,UserTPESerializer,CategorieSerializer, MouvementSerializer, CommandeFournisseurSerializer, CommandeClientSerializer


class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Utilisateur créé avec succès'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({'error': 'Token de rafraîchissement manquant'}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class ProduitViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class UserTPEViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = UserTPE.objects.all()
    serializer_class = UserTPESerializer
class ClientViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = UserTPE.objects.filter(role='CLIENT')
    serializer_class = UserTPESerializer

class FournisseurViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = UserTPE.objects.filter(role='FOURNISSEUR')
    serializer_class = UserTPESerializer

class CategorieViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class MouvementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Mouvement.objects.all()
    serializer_class = MouvementSerializer
    
class CommandeClientViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = CommandeClient.objects.all()
    serializer_class = CommandeClientSerializer

class CommandeFournisseurViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = CommandeFournisseur.objects.all()
    serializer_class = CommandeFournisseurSerializer
    