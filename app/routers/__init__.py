from .user import router as user_router
from .authentication import router as authentication_router
from .source import router as source_router
from .destination import router as destination_router
from .inland_transport import router as inalnd_transport_router

routers = [user_router, authentication_router, source_router, destination_router, inalnd_transport_router]


