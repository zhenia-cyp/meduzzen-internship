from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.schemas.company import CompanyCreateRequest, CompanySchema, CompanyUpdateRequest, CompanyDetails, StatusCompany
from app.schemas.pagination import PagedResponseSchema, PageParams
from app.schemas.schema import MyResponse
from app.services.authentication import AuthService
from app.services.company import CompanyService
from fastapi.security import HTTPBearer
from app.utils.exceptions import NotFoundException

router = APIRouter()
token_auth_scheme = HTTPBearer()


@router.post("/add/company/", response_model=CompanyCreateRequest)
async def add_company(company: CompanyCreateRequest, token: str = Depends(token_auth_scheme), session: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    company_service = CompanyService(session)
    new_company = await company_service.add_company(company, user)
    return new_company


@router.get("/companies/", response_model=PagedResponseSchema[CompanySchema])
async def all_users(session: AsyncSession = Depends(get_async_session), page_params: PageParams = Depends(PageParams)):
    company_service = CompanyService(session)
    companies = await company_service.get_all_companies(page_params)
    return companies


@router.patch("/update/company/", response_model=CompanyUpdateRequest)
async def partially_user_update(company_id: int,company: CompanyUpdateRequest, token: str = Depends(token_auth_scheme), session: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    company_service = CompanyService(session)
    update = await company_service.partially_company_update(user, company, company_id)
    return update


@router.delete("/delete/company/{company_id}/", response_model=MyResponse[int])
async def delete_user(company_id: int, session: AsyncSession = Depends(get_async_session), token: str = Depends(token_auth_scheme)):
     auth_service = AuthService(session)
     user = await auth_service.get_user_by_token(token, session)
     company_service = CompanyService(session)
     result = await company_service.delete_company(company_id, user)
     return MyResponse(status_code="200",message="Delete user",result=result)



@router.get("/get/company/{company_id}/",response_model=CompanyDetails)
async def get_by_id(company_id: int, session: AsyncSession = Depends(get_async_session)):
    company_service = CompanyService(session)
    result = await company_service.get_company_by_id(company_id)
    if result is None:
        raise NotFoundException()
    return result


@router.patch("/change/status/{company_id}/", response_model=StatusCompany)
async def partially_user_update(company_id: int,update: StatusCompany, token: str = Depends(token_auth_scheme), session: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    company_service = CompanyService(session)
    update = await company_service.change_company_visibility(user, update, company_id)
    return update


@router.get("/companies/by/user/", response_model=PagedResponseSchema[CompanySchema])
async def all_users(session: AsyncSession = Depends(get_async_session),  token: str = Depends(token_auth_scheme), page_params: PageParams = Depends(PageParams)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    company_service = CompanyService(session)
    companies = await company_service.users_companies(user, page_params)
    return companies