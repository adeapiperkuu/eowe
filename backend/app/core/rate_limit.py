from slowapi import Limiter
from slowapi.util import get_remote_address

# Shared instance: main.py registers it on app.state + the exception handler,
# route modules import it to apply @limiter.limit(...) to specific routes.
limiter = Limiter(key_func=get_remote_address)
