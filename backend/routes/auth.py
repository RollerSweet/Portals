import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials, HTTPBasicCredentials
# from Utilities.Addresses import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, vCenter_IP, vCenter_username, \
#     vCenter_passwd
# from Utilities.Utility import check_folder_existence, check_session_existence, is_user_in_group

security = HTTPBearer()
auth = APIRouter()




def create_access_token(username: str) -> str:
    # Get the expiry time
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Create the token
    access_token = jwt.encode({"sub": username, "exp": expiry}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # Return the token
    return access_token


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # Verify the token and get the payload
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        # Get the username from the payload and returns it
        username = payload.get("sub")
        return username
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except (jwt.exceptions.InvalidTokenError, Exception):
        raise HTTPException(status_code=401, detail="Invalid access token")


@auth.get("/protected")
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        return {"message": f"Hello, {username}!"}
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except (jwt.exceptions.InvalidTokenError, Exception):
        raise HTTPException(status_code=401, detail="Invalid access token")


@auth.get("/validate_token")
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username:
            return True
        else:
            return False
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except (jwt.exceptions.InvalidTokenError, Exception):
        raise HTTPException(status_code=401, detail="Invalid access token")


@auth.post("/api/login")
async def login(credentials: HTTPBasicCredentials):
    username = credentials.username
    password = credentials.password
    # Check if the user is in the specific OU
    valid_user = is_user_in_group(username, password)
    if not valid_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(username)  # If user is valid, create and return access token
    return {"access_token": access_token}


# @auth.post('/upload')
# async def upload_file(current_user: str = Depends(get_current_user)):
