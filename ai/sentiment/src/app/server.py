from fastapi import FastAPI
from ai.sentiment.src.app.containers.app import AppContainer
from ai.sentiment.src.app.endpoints import classify


def create_app() -> FastAPI:
    # Create the container instance
    container = AppContainer()

    # This wires the 'Provide' markers in your routes to this container instance
    container.wire(modules=[classify])
    # Explicitly trigger the singleton creation
    container.sentiment_service()

    app = FastAPI()
    app.include_router(classify.sentiment_router, prefix="/sentiment")

    return app

# This 'app' is what uvicorn will eventually look for
app = create_app()