from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Body, Depends, Query, status, HTTPException
from fastapi_pagination import LimitOffsetPage, LimitOffsetParams
from pydantic import UUID4
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaListOut, AtletaOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
        '/',
        summary='Criar um novo atleta',
        status_code=status.HTTP_201_CREATED,
        response_model=AtletaOut,
        )
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...),
    ) -> AtletaOut:
    
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    # procura a categoria
    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_nome))
        ).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'A categoria {categoria_nome} não foi encontrada')

    # procura centro de treinamento
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
        ).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado')
    
    atleta_out = AtletaOut(id=uuid4(),created_at=datetime.now(timezone.utc), **atleta_in.model_dump())
    atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
    atleta_model.categoria_id = categoria.pk_id
    atleta_model.centro_treinamento_id = centro_treinamento.pk_id
    
    try:
        db_session.add(atleta_model)
        await db_session.commit()
    
    except IntegrityError as e:
        # Rollback the transaction
        await db_session.rollback()
        
        if 'cpf' in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro de integridade dos dados."
        )

    return atleta_out
        

# Get all (atletas)
@router.get(
        '/',
        summary='Consultar todos os atletas',
        status_code=status.HTTP_200_OK,
        response_model=LimitOffsetPage[AtletaListOut],
        )
async def query(
    db_session: DatabaseDependency,
    params: LimitOffsetParams = Depends(),
    nome: Optional[str] = Query(None, description="Filtrar por nome do atleta"),
    cpf: Optional[str] = Query(None, description="Filtrar por CPF do atleta")
    ) -> LimitOffsetPage[AtletaListOut]:
    
    # Base query
    query = select(AtletaModel)

    # Apply filters if query parameters are provided
    if nome:
        query = query.filter(AtletaModel.nome == nome)
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)

    # Apply pagination
    result = await db_session.execute(
        query.offset(params.offset).limit(params.limit)  # Use limit and offset
    )
    atletas = result.scalars().all()
    
    # Total count (for pagination metadata)
    total_count = await db_session.scalar(select(func.count()).select_from(AtletaModel))

    # return atletas
    return LimitOffsetPage.create(
        items=atletas,
        total=total_count,
        params=params
    )

# Get by id
@router.get(
        '/{id}',
        summary='Consultar um atleta pelo id',
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut,
        )

async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado pelo id: {id}')

    return atleta

# Patch
@router.patch(
        '/{id}',
        summary='Editar um atleta pelo id',
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut,
        )
async def get(
    id: UUID4,
    db_session: DatabaseDependency,
    atleta_up: AtletaUpdate = Body(...),
    ) -> AtletaOut:
    
    atleta = (await db_session.execute(
        select(AtletaModel).filter_by(id=id))
        ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado pelo id: {id}')
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta

# Delete
@router.delete(
        '/{id}',
        summary='Deletar um atleta pelo id',
        status_code=status.HTTP_204_NO_CONTENT
        )

async def get(
        id: UUID4,
        db_session: DatabaseDependency
        ) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado pelo id: {id}')
    

    await db_session.delete(atleta)
    await db_session.commit()