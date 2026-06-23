from fastapi import APIRouter

router = APIRouter()

@router.post("/create-user")
async def create_user():

    return {
        "message": "User created successfully"
    }