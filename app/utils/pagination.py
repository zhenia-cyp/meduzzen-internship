from typing import Optional, List, TypeVar, Generic
from app.schemas.pagination import PageParams, PagedResponseSchema
from sqlalchemy import select

T = TypeVar('T')

class Pagination:
    def __init__(self, model, session, page_params: PageParams, items: Optional[List[T]] = None):
        self.model = model
        self.session = session
        self.page_params = page_params
        self.items = items
        self.page = page_params.page - 1
        self.offset = self.page * page_params.size
        self.limit = page_params.size


    async def get_pagination(self ) -> PagedResponseSchema:
        if self.items is not None:
            total = len(self.items)
            paginated_items = self.items[self.offset:self.offset + self.limit]
            return PagedResponseSchema(
                total=total,
                page=self.page_params.page,
                size=self.page_params.size,
                result=paginated_items
            )

        stmt = select(self.model).offset(self.offset).limit(self.limit)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        total = len(items)
        return PagedResponseSchema(
            total=total,
            page=self.page_params.page,
            size=self.page_params.size,
            result=items
        )