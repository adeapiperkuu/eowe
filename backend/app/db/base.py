# Model registry: import every model module here so Alembic autogenerate
# sees the full metadata (DEVELOPMENT_GUIDE §3).
from app.db.base_class import Base  # noqa: F401
from app.modules.auth.models import RefreshToken, Role, User  # noqa: F401
from app.modules.events.models import Event  # noqa: F401
from app.modules.participants.models import Participant  # noqa: F401
from app.modules.partners.models import Partner  # noqa: F401
from app.modules.shop.models import Product  # noqa: F401
from app.modules.tenants.models import Tenant  # noqa: F401
