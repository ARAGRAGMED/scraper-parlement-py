#!/usr/bin/env python3
"""
Data service for handling data file operations
"""

import json
import os
from datetime import datetime
from utils.helpers import get_data_file_path

class DataService:
    """Service for handling data file operations"""
    
    @staticmethod
    def get_data_file_path():
        """Get the current year data file path dynamically"""
        return get_data_file_path()
    
    @staticmethod
    def read_legislation_data():
        """Read legislation data from the appropriate data file"""
        try:
            data_file, legislative_year = get_data_file_path()
            
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        "total_items": data.get("total_items", 0),
                        "current_year": data.get("current_year", legislative_year),
                        "scraped_at": data.get("scraped_at"),
                        "data": data.get("data", []),
                        "status": "success",
                        "message": f"Retrieved {data.get('total_items', 0)} legislation items"
                    }
            else:
                return {
                    "total_items": 0,
                    "current_year": legislative_year,
                    "scraped_at": None,
                    "data": [],
                    "message": f"No legislation data available for {legislative_year}. Use /api/legislation/refresh to fetch data from source.",
                    "status": "empty"
                }
        except Exception as e:
            return {
                "error": "Failed to retrieve legislation data",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    @staticmethod
    def filter_legislation_by_stage(stage: str):
        """Filter legislation data by stage"""
        try:
            if stage not in ["1", "2"]:
                return {
                    "error": "Invalid stage parameter",
                    "message": "Stage must be '1' or '2'",
                    "valid_stages": ["1", "2"],
                    "timestamp": datetime.now().isoformat()
                }
            
            data_file, legislative_year = get_data_file_path()
            stage_name = "Lecture 1" if stage == "1" else "Lecture 2"
            
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    stage_data = [item for item in data.get("data", []) if item.get("stage") == stage_name]
                    
                    return {
                        "stage": stage_name,
                        "stage_number": stage,
                        "total_items": len(stage_data),
                        "data": stage_data,
                        "message": f"Retrieved {len(stage_data)} legislation items for stage {stage}",
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return {
                    "stage": stage_name,
                    "stage_number": stage,
                    "total_items": 0,
                    "data": [],
                    "message": f"No legislation data available for stage {stage}",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "error": "Failed to retrieve legislation by stage",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    @staticmethod
    def filter_legislation_by_commission(commission_id: str):
        """Filter legislation data by commission ID"""
        try:
            # Map commission IDs to names
            commission_names = {
                "62": "Commission des affaires étrangères, de la défense nationale, des affaires islamiques, des affaires de la migration et des MRE",
                "63": "Commission des Pétitions",
                "64": "Commission de l'intérieur, des collectivités territoriales, de l'habitat, de la politique de la ville et des affaires administratives",
                "65": "Commission de justice, de législation, des droits de l'homme et des libertés",
                "66": "Commission des finances et du développement économique",
                "67": "Commission des secteurs sociaux",
                "68": "Commission des secteurs productifs",
                "69": "Commission des infrastructures, de l'énergie, des mines, de l'environnement et du développement durable",
                "70": "Commission de l'enseignement, de la culture et de la communication",
                "71": "Commission du contrôle des finances publiques et de la gouvernance",
                "72": "Groupe de travail thématique chargé de l'évaluation du Plan National de la Réforme de l'Administration",
                "73": "Groupe de travail thématique chargé de l'évaluation de la politique hydrique",
                "74": "Groupe de travail thématique chargé de l'évaluation du Plan Maroc Vert",
                "75": "Groupe de travail thématique temporaire chargé de l'évaluation des conditions de mise en application de la loi N°103.13 relative à la lutte contre les violences faites aux femmes",
                "94": "Groupe de travail thématique temporaire sur la transition énergétique",
                "95": "Groupe de travail thématique temporaire sur l'intelligence artificielle",
                "96": "Groupe de travail thématique temporaire sur l'égalité et la parité",
                "97": "Groupe de travail thématique chargé de l'évaluation des programmes d'alphabétisation",
                "98": "Groupe de travail thématique chargé de l'évaluation de la stratégie nationale du sport 2008-2020",
                "99": "Groupe de travail thématique temporaire sur les Affaires Africaines",
                "100": "Groupe de travail thématique temporaire sur les mesures de contrôle des prix des produits de base sur le marché national"
            }
            
            if commission_id not in commission_names:
                return {
                    "error": "Commission not found",
                    "message": f"Commission ID {commission_id} does not exist",
                    "valid_commission_ids": list(commission_names.keys()),
                    "timestamp": datetime.now().isoformat()
                }
            
            data_file, legislative_year = get_data_file_path()
            
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    commission_data = [item for item in data.get("data", []) if item.get("commission_id") == commission_id]
                    
                    return {
                        "commission_id": commission_id,
                        "commission_name": commission_names[commission_id],
                        "total_items": len(commission_data),
                        "data": commission_data,
                        "message": f"Retrieved {len(commission_data)} legislation items for commission {commission_id}",
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return {
                    "commission_id": commission_id,
                    "commission_name": commission_names[commission_id],
                    "total_items": 0,
                    "data": [],
                    "message": f"No legislation data available for commission {commission_id}",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "error": "Failed to retrieve legislation by commission",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    @staticmethod
    def find_legislation_by_number(numero: str):
        """Find legislation by law number"""
        try:
            data_file, legislative_year = get_data_file_path()
            
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    legislation_item = next((item for item in data.get("data", []) if item.get("law_number") == numero), None)
                    
                    if legislation_item:
                        return {
                            "law_number": numero,
                            "found": True,
                            "data": legislation_item,
                            "message": f"Retrieved legislation with number {numero}",
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        return {
                            "law_number": numero,
                            "found": False,
                            "message": f"No legislation found with number {numero}",
                            "timestamp": datetime.now().isoformat()
                        }
            else:
                return {
                    "law_number": numero,
                    "found": False,
                    "message": f"No legislation data available",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "error": "Failed to retrieve legislation by number",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
