#!/usr/bin/env python3
"""
Data service for the Moroccan Parliament API
Handles reading and filtering legislation data from local JSON files
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

# Import utilities with absolute imports for Vercel compatibility
try:
    from api.utils.helpers import get_data_file_path
except ImportError:
    # Fallback for local development
    from utils.helpers import get_data_file_path

class DataService:
    """Service class for handling legislation data operations"""
    
    @staticmethod
    def read_legislation_data() -> Dict[str, Any]:
        """Read all legislation data from local database"""
        try:
            data_file_path = get_data_file_path()
            
            if not os.path.exists(data_file_path):
                return {
                    "total_items": 0,
                    "current_year": datetime.now().year,
                    "data": [],
                    "status": "no_data",
                    "message": "No legislation data found"
                }
            
            with open(data_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract basic info
            total_items = len(data.get('data', []))
            current_year = data.get('current_year', datetime.now().year)
            scraped_at = data.get('scraped_at', datetime.now().isoformat())
            
            return {
                "total_items": total_items,
                "current_year": current_year,
                "scraped_at": scraped_at,
                "data": data.get('data', []),
                "status": "success" if total_items > 0 else "empty",
                "message": f"Successfully loaded {total_items} legislation items"
            }
            
        except Exception as e:
            return {
                "total_items": 0,
                "current_year": datetime.now().year,
                "data": [],
                "status": "error",
                "message": f"Error reading legislation data: {str(e)}"
            }
    
    @staticmethod
    def filter_legislation_by_stage(stage: str) -> Dict[str, Any]:
        """Filter legislation by stage (1 = Lecture 1, 2 = Lecture 2)"""
        try:
            all_data = DataService.read_legislation_data()
            
            if all_data['status'] != 'success':
                return all_data
            
            # Filter by stage
            stage_name = "Lecture 1" if stage == "1" else "Lecture 2"
            filtered_data = [
                item for item in all_data['data'] 
                if item.get('stage') == stage_name
            ]
            
            return {
                "stage": stage,
                "stage_name": stage_name,
                "total_items": len(filtered_data),
                "data": filtered_data,
                "status": "success" if filtered_data else "empty"
            }
            
        except Exception as e:
            return {
                "stage": stage,
                "total_items": 0,
                "data": [],
                "status": "error",
                "message": f"Error filtering by stage: {str(e)}"
            }
    
    @staticmethod
    def filter_legislation_by_commission(commission_id: str) -> Dict[str, Any]:
        """Filter legislation by commission ID"""
        try:
            all_data = DataService.read_legislation_data()
            
            if all_data['status'] != 'success':
                return all_data
            
            # Filter by commission ID
            filtered_data = [
                item for item in all_data['data'] 
                if item.get('commission_id') == commission_id
            ]
            
            commission_name = filtered_data[0].get('commission', 'Unknown') if filtered_data else 'Unknown'
            
            return {
                "commission_id": commission_id,
                "commission_name": commission_name,
                "total_items": len(filtered_data),
                "data": filtered_data,
                "status": "success" if filtered_data else "empty"
            }
            
        except Exception as e:
            return {
                "commission_id": commission_id,
                "total_items": 0,
                "data": [],
                "status": "error",
                "message": f"Error filtering by commission: {str(e)}"
            }
    
    @staticmethod
    def find_legislation_by_number(numero: str) -> Dict[str, Any]:
        """Find specific legislation by law number"""
        try:
            all_data = DataService.read_legislation_data()
            
            if all_data['status'] != 'success':
                return all_data
            
            # Find by law number
            found_item = None
            for item in all_data['data']:
                if item.get('law_number') == numero:
                    found_item = item
                    break
            
            if found_item:
                return {
                    "numero": numero,
                    "data": found_item,
                    "status": "success"
                }
            else:
                return {
                    "numero": numero,
                    "data": None,
                    "status": "not_found",
                    "message": f"Legislation with number {numero} not found"
                }
                
        except Exception as e:
            return {
                "numero": numero,
                "data": None,
                "status": "error",
                "message": f"Error finding legislation: {str(e)}"
            }
    
    @staticmethod
    def get_all_commissions() -> List[Dict[str, str]]:
        """Get all available commissions"""
        try:
            # Hardcoded commission list for now
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
            
            return commissions
            
        except Exception as e:
            return []
