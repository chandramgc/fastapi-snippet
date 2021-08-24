from fastapi import APIRouter

# from app.api.routes import authentication, comments, profiles, tags, users
# from app.api.routes.articles import api as articles

from src.api.routes.customers import api as customers
from src.api.routes.restaurants import api as restaurants
from src.core.config import API_VERSION

router = APIRouter()
router.include_router(customers.router, tags=["Customers"], prefix="/"+API_VERSION)
router.include_router(restaurants.router, tags=["Restaurants"], prefix="/"+API_VERSION)

"""
router.include_router(authentication.router, tags=["authentication"], prefix="/users")
router.include_router(users.router, tags=["users"], prefix="/user")
router.include_router(profiles.router, tags=["profiles"], prefix="/profiles")
router.include_router(articles.router, tags=["articles"])
router.include_router(
    comments.router,
    tags=["comments"],
    prefix="/articles/{slug}/comments",
)
router.include_router(tags.router, tags=["tags"], prefix="/tags")
"""