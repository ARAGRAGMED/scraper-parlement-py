#!/usr/bin/env python3
"""
Commission routes for the Moroccan Parliament API
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/commissions")
async def get_all_commissions():
    """Get all available commissions from the Moroccan Parliament"""
    try:
        commissions = [
            {"id": "62", "name": "Commission des affaires étrangères, de la défense nationale, des affaires islamiques, des affaires de la migration et des MRE"},
            {"id": "63", "name": "Commission des Pétitions"},
            {"id": "64", "name": "Commission de l'intérieur, des collectivités territoriales, de l'habitat, de la politique de la ville et des affaires administratives"},
            {"id": "65", "name": "Commission de justice, de législation, des droits de l'homme et des libertés"},
            {"id": "66", "name": "Commission des finances et du développement économique"},
            {"id": "67", "name": "Commission des secteurs sociaux"},
            {"id": "68", "name": "Commission des secteurs productifs"},
            {"id": "69", "name": "Commission des infrastructures, de l'énergie, des mines, de l'environnement et du développement durable"},
            {"id": "70", "name": "Commission de l'enseignement, de la culture et de la communication"},
            {"id": "71", "name": "Commission du contrôle des finances publiques et de la gouvernance"},
            {"id": "72", "name": "Groupe de travail thématique chargé de l'évaluation du Plan National de la Réforme de l'Administration"},
            {"id": "73", "name": "Groupe de travail thématique chargé de l'évaluation de la politique hydrique"},
            {"id": "74", "name": "Groupe de travail thématique chargé de l'évaluation du Plan Maroc Vert"},
            {"id": "75", "name": "Groupe de travail thématique temporaire chargé de l'évaluation des conditions de mise en application de la loi N°103.13 relative à la lutte contre les violences faites aux femmes"},
            {"id": "94", "name": "Groupe de travail thématique temporaire sur la transition énergétique"},
            {"id": "95", "name": "Groupe de travail thématique temporaire sur l'intelligence artificielle"},
            {"id": "96", "name": "Groupe de travail thématique temporaire sur l'égalité et la parité"},
            {"id": "97", "name": "Groupe de travail thématique chargé de l'évaluation des programmes d'alphabétisation"},
            {"id": "98", "name": "Groupe de travail thématique chargé de l'évaluation de la stratégie nationale du sport 2008-2020"},
            {"id": "99", "name": "Groupe de travail thématique temporaire sur les Affaires Africaines"},
            {"id": "100", "name": "Groupe de travail thématique temporaire sur les mesures de contrôle des prix des produits de base sur le marché national"}
        ]
        
        return {
            "total_commissions": len(commissions),
            "commissions": commissions,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": "Failed to retrieve commissions data",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }
