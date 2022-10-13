from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service import services, uploads

app = FastAPI(itle="API Tool", description="APIs to read a file and provide data.")

# Allowed Origins
origins = ["*"]

# Add Middleware
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# File Upload Service
app.include_router(uploads.router, prefix="/uploads", tags=["File Upload"],
                          responses={404: {"Description": "Not Found!"}})

# Services
app.include_router(services.router, prefix="/products", tags=["Services"],
                   responses={404: {"Description": "Not Found!"}})
                   