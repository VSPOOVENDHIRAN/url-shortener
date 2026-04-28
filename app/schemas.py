from pydantic import BaseModel
from typing import Optional  

class URLCreate(BaseModel):  
    url: str  
    custom_code: Optional[str] = None
    expiry_minutes: Optional[int] = None