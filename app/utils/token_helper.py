import jwt
import logging
import os
import inspect
from fastapi import Request, HTTPException
from functools import wraps
from datetime import datetime, timedelta, timezone
from functools import wraps
from starlette import status
from fastapi import Request
# from jose.exceptions import JWTError, ExpiredSignatureError
from fastapi import HTTPException, status, Depends
from typing import Optional

SECRET_KEY = "aV3ry$tr0ngRand0mStr1ngWithSymb0ls!1234567890" #os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

logger = logging.info(__name__)

def verify_token(allowed_roles: list):
    print('level 1')
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            print('level 2')
            auth_header = request.headers.get('Authorization')
            print(auth_header)
            if not auth_header or not auth_header.startswith('Bearer '):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing or invalid Authorization header"
                )
            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_role = payload.get("role")
                print(user_role)
                print(payload.get("user_id"))
                user_id = payload.get("user_id")

                if not user_role:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Role not found in token"
                    )

                if allowed_roles and user_role not in allowed_roles:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Access denied for role: {user_role}"
                    )
                request.state.user_id = user_id
                # kwargs['user'] = payload  # Pass user info to route handler
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token has expired")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")
            except Exception as e:
                raise e

            if inspect.iscoroutinefunction(func):
                return await func(request, *args, **kwargs)
            else:
                return func(request, *args, **kwargs)
        return wrapper
    return decorator

def verify_user_jwt(token: str = Depends()):
    return verify_token(token, role="user")

def verify_admin_jwt(token: str = Depends()):
    return verify_token(token, role="admin")
