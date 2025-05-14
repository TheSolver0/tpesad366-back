from rest_framework import routers
from .views import AuthViewSet,UserViewSet, ProduitViewSet,UserTPEViewSet, FournisseurViewSet, ClientViewSet, CategorieViewSet, MouvementViewSet, CommandeClientViewSet,CommandeFournisseurViewSet

router = routers.DefaultRouter()

router.register('produits', ProduitViewSet)
router.register('users', UserTPEViewSet,basename='user')
router.register('gerants', UserViewSet,basename='gerant')
router.register('fournisseurs', FournisseurViewSet,basename='fournisseur')
router.register('clients', ClientViewSet,basename='client')
router.register('mouvements', MouvementViewSet)
router.register('categories', CategorieViewSet)
router.register('commandesClient',CommandeClientViewSet )
router.register('commandesFournisseur',CommandeFournisseurViewSet )
router.register('auth',AuthViewSet, basename='auth' )

