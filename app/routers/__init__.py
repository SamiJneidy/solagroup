from .user import router as user_router
from .authentication import router as authentication_router
from .source import router as source_router
from .warehouse import router as warehouse_router
from .inland_transport import router as inalnd_transport_router
from .shipping_line import router as shipping_line_router
from .maritime_transport import router as maritime_transport_router
from .copart_testing import router as copart_router
from .auction_fee import router as auction_fee_router
from .additional_settings import router as additional_settings_router
from .estimate_cost import router as estimate_cost_router
from .destination import router as destinations_router
routers = [
    user_router, 
    authentication_router, 
    source_router, 
    warehouse_router, 
    inalnd_transport_router, 
    shipping_line_router, 
    maritime_transport_router,
    auction_fee_router,
    additional_settings_router,
    estimate_cost_router,
    destinations_router,
    # copart_router,
]


