import logging
from sqlalchemy import select, delete
from app.models.model import Company, User
from app.schemas.company import CompanyCreateRequest, CompanySchema
from app.services.user import UserService
from app.utils.exceptions import CompanyAlreadyExistsException, NotFoundException
from app.utils.pagination import Pagination
from app.schemas.pagination import PageParams, PagedResponseSchema
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class CompanyService:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)


    async def get_company_by_id(self, company_id: int)-> Company:
                try:
                    stmt = select(Company).filter_by(id=company_id)
                    result = await self.session.execute(stmt)
                    company = result.scalar_one()
                    print('company',company)
                    return company
                except SQLAlchemyError as e:
                    self.logger.error(f"get company by id: {str(e)}")
                    return None


    async def check_company_name(self, name):
        stmt = select(Company).where(Company.name == name)
        result = await self.session.execute(stmt)
        exist = result.scalars().all()
        if exist:
            raise CompanyAlreadyExistsException(name)
        return False


    async def add_company(self, company: CompanyCreateRequest, user) -> Company:
            data = company.dict()
            user_service = UserService(self.session)
            current_user = await user_service.get_user_by_email(user.email)
            data.update({"owner_id": current_user.id})
            await self.check_company_name(data["name"])
            company = Company(**data)
            self.session.add(company)
            await self.session.commit()
            await self.session.refresh(company)
            return company


    async def get_all_companies(self, page_params: PageParams) -> PagedResponseSchema:
        pagination = Pagination(Company, self.session, page_params)
        return await pagination.get_pagination()


    async def partially_company_update(self, user, company, id):
        data = company.dict(exclude={'updated_at'})
        user_service = UserService(self.session)
        user = await user_service.get_user_by_email(user.email)
        current_company= await self.get_company_by_id(id)
        if current_company.owner_id != user.id:
            raise NotFoundException()
        current_company.name = data['name']
        current_company.description = data['description']
        current_company.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(current_company)
        return current_company


    async def delete_company(self, id: int, user):
            user_service = UserService(self.session)
            user = await user_service.get_user_by_email(user.email)
            current_company = await self.get_company_by_id(id)
            if current_company.owner_id != user.id:
                raise NotFoundException()
            stmt = delete(Company).filter_by(id=id)
            await self.session.execute(stmt)
            await self.session.commit()
            return True


    async def change_company_visibility(self, user, update, id):
        data = update.dict()
        user_service = UserService(self.session)
        user = await user_service.get_user_by_email(user.email)
        current_company = await self.get_company_by_id(id)
        if current_company.owner_id != user.id:
            raise NotFoundException()
        current_company.is_visible = data['is_visible']
        current_company.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(current_company)
        return current_company


    async def users_companies(self, user, page_params):
        user_service = UserService(self.session)
        user = await user_service.get_user_by_email(user.email)
        result = await self.session.execute(
            select(Company).join(User, User.id == Company.owner_id).where(User.id == user.id)
        )
        companies = result.scalars().all()
        pagination = Pagination(User, self.session, page_params,companies)
        return await pagination.get_pagination()

