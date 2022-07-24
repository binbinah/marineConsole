from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from backend.app.cma.api import router as cma_router
import uvicorn

api = FastAPI(docs_url=None)

app = FastAPI()

app.mount("/api", api)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="dist")


@api.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title=api.title + " - Swagger UI",
        oauth2_redirect_url=api.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@api.get(api.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


# swagger 文档配置
def custom_openapi():
    if api.openapi_schema:
        return api.openapi_schema
    openapi_schema = get_openapi(
        title="自动化服务控制器 API",
        version="1.0.0",
        description="自动化服务控制器 API",
        routes=api.routes,
        servers=[{"url": "/api"}],
    )
    api.openapi_schema = openapi_schema
    return api.openapi_schema


api.openapi = custom_openapi


api.include_router(cma_router, prefix="/cma/v1", tags=["CMA"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
