from fastapi import FastAPI
from app.middlewares.auth_middlewares import jwt_verify
from app.routes.User_routes import user_router as user_auth_routes
from app.routes.Chai_routes import chai_router as chai_routes

app = FastAPI()

# 👇 Register custom JWT middleware globally
app.middleware("http")(jwt_verify)

# 👇 Include auth routes
app.include_router(user_auth_routes)
app.include_router(chai_routes)
