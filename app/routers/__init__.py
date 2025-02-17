from .user import router as user_router
from .authentication import router as authentication_router
from .source import router as source_router
from .warehouse import router as warehouse_router
from .inland_transport import router as inalnd_transport_router

routers = [user_router, authentication_router, source_router, warehouse_router, inalnd_transport_router]


