from .user import router as user_router
from .authentication import router as authentication_router
from .source import router as source_router
from .warehouse import router as warehouse_router
from .inland_transport import router as inalnd_transport_router
from .shipping_line import router as shipping_line_router
from .maritime_transport import router as maritime_transport_router
from .copart_testing import router as copart_router
routers = [
    user_router, 
    authentication_router, 
    source_router, 
    warehouse_router, 
    inalnd_transport_router, 
    shipping_line_router, 
    maritime_transport_router,
    copart_router,
]


