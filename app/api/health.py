from fastapi import APIRouter  
  
router = APIRouter()  
  
@router.get("/health", tags=["Health"])  
async def health_check():  
    """  
    Health Check Endpoint  
  
    This endpoint returns the health status of the service.  
    It can be used to verify that the service is running correctly.  
  
    Returns:  
        dict: A dictionary containing the health status with a key 'status' and value 'healthy'.  
    """  
    return {"status": "healthy"}  
