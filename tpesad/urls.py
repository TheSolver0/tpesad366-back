from rest_framework import routers
from .views import BookViewSet, AuthorViewSet, ProduitViewSet,UserTPEViewSet, FournisseurViewSet, ClientViewSet, CategorieViewSet, MouvementViewSet, CommandeClientViewSet,CommandeFournisseurViewSet

router = routers.DefaultRouter()
router.register('books', BookViewSet)
router.register('authors', AuthorViewSet)

#------------------------------------------------------------------------------------------------------------------------------------

router.register('produits', ProduitViewSet)
router.register('users', UserTPEViewSet,basename='user')
router.register('fournisseurs', FournisseurViewSet,basename='fournisseur')
router.register('clients', ClientViewSet,basename='client')
router.register('mouvements', MouvementViewSet)
router.register('categories', CategorieViewSet)
router.register('commandesClient',CommandeClientViewSet )
router.register('commandesFournisseur',CommandeFournisseurViewSet )