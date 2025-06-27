from functools import wraps

def asyncHandler(func):
    @wraps(func)
    async def wrapper(*args,**kwargs):
        try:
            return await func(*args,**kwargs)
        except Exception as e:
            raise e
    return wrapper