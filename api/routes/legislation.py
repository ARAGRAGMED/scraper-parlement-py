#!/usr/bin/env python3
"""
Legislation routes for the Moroccan Parliament API
"""

from fastapi import APIRouter
from services.data_service import DataService

router = APIRouter()

@router.get("/legislation")
async def get_all_legislation():
    """Get all legislation from local database"""
    return DataService.read_legislation_data()

@router.get("/legislation/{stage}")
async def get_legislation_by_stage(stage: str):
    """Get legislation from local database by stage (1 or 2)"""
    return DataService.filter_legislation_by_stage(stage)

@router.get("/legislation/commission/{commission_id}")
async def get_legislation_by_commission(commission_id: str):
    """Get legislation from local database by commission ID"""
    return DataService.filter_legislation_by_commission(commission_id)

@router.get("/legislation/numero/{numero}")
async def get_legislation_by_numero(numero: str):
    """Get legislation from local database by law number"""
    return DataService.find_legislation_by_number(numero)
