import logging

from fastapi import FastAPI

log = logging.getLogger("werkzeug")
log.setLevel(logging.WARNING)


class CustomFastAPIApp(FastAPI):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._configure_blueprints()

    def _configure_blueprints(self):
        from src.views import routers

        for router in routers:
            self.include_router(router)
