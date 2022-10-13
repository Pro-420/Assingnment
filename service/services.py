from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from database.service import Database
from datetime import date

router = APIRouter()
database = Database()

def pagination(result, page_num, page_size, link):
    start=(page_num-1)*page_size
    end=start+page_size
    response={
        "data": result[start:end],
        "total": len(result),
        "count": page_size,
        "pagination": {}
    }
    
    if end>=len(result):
        response["pagination"]["next"] = None
        if page_num>1:
            response["pagination"]["previous"] = link
        else:
            response["pagination"]["previous"] = None
    else:
        if page_num>1:
            response["pagination"]["previous"] = link
        else:
            response["pagination"]["previous"] = None
        response["pagination"]["next"] = link
    
    return response    

@router.post("/productlist")
def listprovider(request: Request, supplier_info: str, page_num: int=1, page_size: int=10):
    data: dict = {
        'supplier': supplier_info
    }
    result = database.data_finder(data)
    link: str =  f"/productlist?supplier_info={supplier_info.replace(' ', '%20')}&page_num={page_num-1}&page_size={page_size}"
    response=pagination(
            result=result, 
            page_nume=page_num, 
            page_size=page_size,
            link=link
        )
    if len(result) != 0:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)
    else:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="No data found")
    
@router.post("/productlist/{product_name}")
def listprovider(request: Request, product_name: str, supplier_info: str, page_num: int=1, page_size: int=10):
    data: dict = {
        'supplier': supplier_info,
        'name': product_name
    }
    result = database.data_finder(data)
    link: str =  f"/productlist/{product_name.replace(' ', '%20')}?supplier_info={supplier_info.replace(' ', '%20')}&page_num={page_num-1}&page_size={page_size}"
    response=pagination(
            result=result, 
            page_nume=page_num, 
            page_size=page_size,
            link=link
        )
    
    if len(result) != 0:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)
    else:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="No data found")

@router.post("/nonexpiryproductlist")
def listprovider(request: Request, product_name: str, supplier_info: str, page_num: int=1, page_size: int=10):
    start_date = str(date.today())
    data: dict = {
        'supplier': supplier_info,
        'name': product_name,
        'exp': {'$gte': start_date}
    }
    result = database.data_finder(data)
    link: str =  f"/productlist?product_name={product_name.replace(' ', '%20')}&supplier_info={supplier_info.replace(' ', '%20')}&page_num={page_num-1}&page_size={page_size}"
    response=pagination(
            result=result, 
            page_nume=page_num, 
            page_size=page_size,
            link=link
        )
    
    if len(result) != 0:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)
    else:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="No data found")
