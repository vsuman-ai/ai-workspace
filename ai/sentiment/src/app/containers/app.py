from dependency_injector import containers, providers
from ai.sentiment.src.app.services.sentiment_service import SentimentService
from ai.sentiment.src.app.services.configurations import SentimentClassificationAppConfiguration

class AppContainer(containers.DeclarativeContainer):
    # 1. Provide the Configuration Class as a Singleton
    # This will trigger your get_env logic once.
    app_config = providers.Singleton(SentimentClassificationAppConfiguration)

    # 2. Provide the Classifier
    # We use the factory/singleton and pull values from the app_config
    sentiment_service = providers.Singleton(
        SentimentService,
        triton_url= app_config.provided.get_triton_inference_url.call(),

    )