from .routes import health


def add_app_routes(app):
    app.include_router(health.router, prefix="/health", tags=["Health"])
