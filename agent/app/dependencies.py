from fastapi import Request

from app.services.database import DatabaseService
from app.services.chroma import ChromaService
from app.config import Settings


def get_agent(request: Request):
    return request.app.state.agent


def get_db(request: Request) -> DatabaseService:
    return request.app.state.db


def get_chroma(request: Request) -> ChromaService:
    return request.app.state.chroma


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_schema_reflector(request: Request):
    return request.app.state.schema_reflector
