from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charityproject_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate)
from app.core.user import current_superuser
from app.models import CharityProject
from app.services.project_service import ProjectService


router = APIRouter()


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)])
async def create_new_charityproject(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """Создание проекта. Только для суперюзеров."""

    return await ProjectService(session).create(obj_in=project)


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True,)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
) -> list[CharityProject]:
    """Получение списка проектов."""

    return await charityproject_crud.get_multi(session)


@router.patch('/{project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)])
async def update(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """Обновление данных о проекте. Только для суперюзеров."""

    return await ProjectService(session).update(
        project_id, obj_in)


@router.delete('/{project_id}',
               response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)])
async def remove(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """Удаление проекта. Только для суперюзеров."""

    return await ProjectService(session).remove(project_id)
