from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from TelegramExpolorer.api.search_routes import router as search_router


def make_app() -> FastAPI:
    app = FastAPI(
        title="Telegram Explorer API",
        description="API для поиска контента в Telegram",
        version="1.0.0",
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # В production укажите конкретные домены
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Включение роутера
    app.include_router(
        search_router,
        prefix="/v1",
        tags=["search"],
    )

    # Добавляем health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


app = make_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Автоперезагрузка при изменении кода
        log_level="info",
    )
