import uvicorn, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.routers import user
from routes.auth import auth
from routes.vmcreator import vmcreator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user)
app.include_router(auth)
app.include_router(vmcreator)

# Mount static files directory
app.mount("/", StaticFiles(directory="StaticFiles/build", html=True), name="static")

if __name__ == "__main__":
    ssl_keyfile = os.path.join(os.getcwd(), "Portals.key")
    ssl_certfile = os.path.join(os.getcwd(), "Portals.crt")
    # uvicorn.run("index:app", host="0.0.0.0", port=443, ssl_keyfile=ssl_keyfile, ssl_certfile=ssl_certfile, reload=True)
    uvicorn.run("index:app", host="0.0.0.0", port=80, reload=True)