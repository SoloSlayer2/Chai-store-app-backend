from fastapi import FastAPI
from app.middlewares.auth_middlewares import jwt_verify
from app.routes.User_routes import router as user_auth_routes

app = FastAPI()

# 👇 Register custom JWT middleware globally
app.middleware("http")(jwt_verify)

# 👇 Include auth routes
app.include_router(user_auth_routes)
