from rest_framework import routers
from .views import BookViewSet, AuthorViewSet, ProduitViewSet, FournisseurViewSet, ClientViewSet, CategorieViewSet, MouvementViewSet

router = routers.DefaultRouter()
router.register('books', BookViewSet)
router.register('authors', AuthorViewSet)

#------------------------------------------------------------------------------------------------------------------------------------

router.register('produits', ProduitViewSet)
router.register('fournisseurs', FournisseurViewSet)
router.register('clients', ClientViewSet)
router.register('mouvements', MouvementViewSet)
router.register('categories', CategorieViewSet)