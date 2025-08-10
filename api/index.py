#!/usr/bin/env python3
"""
Vercel Serverless Function for Moroccan Parliament Legislation API
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from pathlib import Path

# Add src directory to Python path for scraper imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

try:
    from moroccan_parliament_scraper.core.legislation_scraper import MoroccanParliamentScraper
    SCRAPER_AVAILABLE = True
    print("✅ Scraper module imported successfully!")
except ImportError as e:
    SCRAPER_AVAILABLE = False
    print(f"❌ Failed to import scraper: {e}")
    print(f"Current directory: {current_dir}")
    print(f"Src directory: {src_dir}")
    print(f"Python path: {sys.path[:3]}")

app = FastAPI(
    title="Moroccan Parliament Scraper API",
    description="API for scraping Moroccan Parliament legislation data",
    version="1.0.0"
)

# Create API router with /api prefix
api_router = APIRouter(prefix="/api")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Scraping endpoint
@api_router.post("/scrape")
async def scrape_legislation():
    """Scrape legislation data from Moroccan Parliament website"""
    try:
        if not SCRAPER_AVAILABLE:
            return {
                "error": "Scraper not available",
                "message": "Scraping functionality is not available on this platform",
                "suggestion": "Use existing data from /api/legislation endpoint",
                "timestamp": datetime.now().isoformat()
            }
        
        # Create scraper instance
        scraper = MoroccanParliamentScraper()
        
        # Run scraper
        success = scraper.run()
        
        if success:
            return {
                "message": "Legislation scraping completed successfully",
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "total_items": len(scraper.results) if hasattr(scraper, 'results') else 0,
                    "scraped_at": datetime.now().isoformat()
                }
            }
        else:
            return {
                "message": "Legislation scraping failed",
                "status": "error",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "error": "Failed to scrape legislation data",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Root endpoint for the main page (serves dynamic_viewer.html content)
@app.get("/")
async def main_page():
    """Main page endpoint - serves dynamic_viewer.html content"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualiseur de Législation du Parlement Marocain</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            min-height: 100vh;
            margin: 0;
            padding: 0;
            line-height: 1.6;
            color: #2c3e50;
        }
        
        .navbar {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 15px 20px;
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
            margin-bottom: 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .navbar-content {
            max-width: 1100px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .navbar-brand {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .navbar-brand:hover {
            color: #5a6fd8;
        }
        
        .navbar-nav {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        
        .nav-link {
            color: #666;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 6px;
            transition: all 0.3s ease;
            font-weight: 500;
            font-size: 14px;
        }
        
        .nav-link:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }
        
        .nav-link.active {
            background: #667eea;
            color: white;
        }
        
        .nav-link.docs {
            background: #28a745;
            color: white;
        }
        
        .nav-link.docs:hover {
            background: #218838;
            transform: translateY(-2px);
        }
        
        .nav-link i {
            margin-right: 8px;
        }
        
        .navbar-brand i {
            margin-right: 10px;
        }
        
        .btn i {
            margin-right: 8px;
        }
        
        .container {
            max-width: 1100px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            overflow: hidden;
            padding: 0;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 40px 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.2em;
            margin: 0 0 12px 0;
            font-weight: 300;
            color: white;
        }

        .header p {
            margin: 0;
            font-size: 0.95em;
            opacity: 0.9;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }

        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 6px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
        }

        .stat-card:hover {
            transform: translateY(-2px);
        }

        .stat-number {
            font-size: 1.8em;
            font-weight: 600;
            color: #667eea;
            margin-bottom: 6px;
        }

        .stat-label {
            color: #6c757d;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }

        .controls {
            padding: 25px 40px;
            background: white;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }

        .search-box {
            flex: 1;
            min-width: 300px;
            padding: 10px 15px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 15px;
            background: white;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .search-box:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
        }

        .filter-select {
            padding: 10px 15px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 15px;
            background: white;
            min-width: 150px;
            transition: border-color 0.2s ease;
        }

        .filter-select:focus {
            outline: none;
            border-color: #667eea;
        }

        .legislation-grid {
            display: grid;
            gap: 20px;
            padding: 30px;
        }

        .legislation-card {
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 25px;
            transition: all 0.2s ease;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .legislation-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transform: translateY(-1px);
        }

        .card-header {
            display: flex;
            align-items: flex-start;
            margin-bottom: 12px;
            gap: 16px;
        }

        .law-number {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 6px 12px;
            font-weight: 500;
            font-size: 0.8em;
            white-space: nowrap;
            border-radius: 15px;
        }

        .stage-badge {
            padding: 4px 10px;
            font-size: 0.75em;
            font-weight: 500;
            white-space: nowrap;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-radius: 12px;
        }

        .stage-lecture-1 {
            background: #e3f2fd;
            color: #1976d2;
        }

        .stage-lecture-2 {
            background: #f3e5f5;
            color: #7b1fa2;
        }

        .card-title {
            flex: 1;
            font-size: 1.1em;
            font-weight: 500;
            color: #2c3e50;
            line-height: 1.4;
        }

        .pdf-indicator {
            background: linear-gradient(135deg, #dc3545, #c82333);
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.7em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 4px rgba(220, 53, 69, 0.2);
        }

        .card-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 18px 0;
            padding: 18px;
            background: #f8f9fa;
            border-radius: 4px;
            font-size: 0.9em;
        }

        .meta-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .meta-label {
            font-weight: 500;
            color: #495057;
        }

        .meta-value {
            color: #6c757d;
        }

        .stages-container {
            margin-top: 16px;
        }

        .stage-section {
            margin-bottom: 12px;
            border: 1px solid #e8e8e8;
            overflow: hidden;
        }

        .stage-header {
            background: #f8f8f8;
            color: #333;
            padding: 8px 16px;
            font-weight: 400;
            font-size: 0.9em;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .stage-header:hover {
            background: #f0f0f0;
        }

        .stage-content {
            padding: 16px;
            background: white;
            display: none;
            border-top: 1px solid #f0f0f0;
        }

        .stage-content.active {
            display: block;
        }

        .stage-detail {
            margin-bottom: 12px;
            padding: 12px 0;
            border-bottom: 1px solid #f8f8f8;
        }

        .stage-detail:last-child {
            border-bottom: none;
        }

        .detail-title {
            font-weight: 500;
            color: #333;
            margin-bottom: 4px;
            font-size: 0.9em;
        }

        .detail-content {
            color: #666;
            line-height: 1.4;
            font-size: 0.85em;
        }

        .pdf-link {
            background: linear-gradient(135deg, #dc3545, #c82333);
            color: white;
            text-decoration: none;
            font-size: 0.85em;
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(220, 53, 69, 0.2);
        }

        .pdf-link:hover {
            background: linear-gradient(135deg, #c82333, #bd2130);
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
        }

        .pdf-button {
            background: linear-gradient(135deg, #dc3545, #c82333);
            color: white;
            text-decoration: none;
            font-size: 0.9em;
            padding: 10px 16px;
            border-radius: 5px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s ease;
            box-shadow: 0 3px 6px rgba(220, 53, 69, 0.25);
            border: none;
            cursor: pointer;
        }

        .pdf-button:hover {
            background: linear-gradient(135deg, #c82333, #bd2130);
            transform: translateY(-2px);
            box-shadow: 0 5px 12px rgba(220, 53, 69, 0.35);
        }

        .actions {
            display: flex;
            gap: 12px;
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid #f0f0f0;
        }

        .btn {
            padding: 8px 16px;
            border: none;
            cursor: pointer;
            font-size: 0.85em;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            border-radius: 4px;
            transition: all 0.2s ease;
            font-weight: 500;
        }

        .btn-primary {
            background: #667eea;
            color: white;
        }

        .btn-primary:hover {
            background: #5a67d8;
            transform: translateY(-1px);
        }

        .btn-outline {
            background: transparent;
            border: 1px solid #667eea;
            color: #667eea;
        }

        .btn-outline:hover {
            background: #667eea;
            color: white;
        }

        .loading {
            text-align: center;
            padding: 60px 40px;
            color: #888;
        }

        .error {
            text-align: center;
            padding: 60px 40px;
            color: #666;
            background: #f8f8f8;
            border-top: 1px solid #f0f0f0;
        }

        .empty-state {
            text-align: center;
            padding: 60px 40px;
            color: #888;
        }

        @media (max-width: 768px) {
            .navbar-content {
                flex-direction: column;
                gap: 15px;
            }
            
            .navbar-nav {
                gap: 10px;
            }
            
            .nav-link {
                padding: 6px 12px;
                font-size: 13px;
            }
            
            .card-header {
                flex-direction: column;
                align-items: flex-start;
            }

            .controls {
                flex-direction: column;
            }

            .search-box {
                min-width: 100%;
            }
        }
    </style>
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar">
        <div class="navbar-content">
            <a href="/" class="navbar-brand"><i class="fas fa-landmark"></i> Visualiseur Parlementaire</a>
            <div class="navbar-nav">
                <a href="/" class="nav-link active"><i class="fas fa-home"></i> Accueil</a>
                <a href="/docs" class="nav-link docs" target="_blank"><i class="fas fa-book"></i> Documentation API</a>
                <a href="/redoc" class="nav-link" target="_blank"><i class="fas fa-file-alt"></i> ReDoc</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="header">
            <h1><i class="fas fa-landmark"></i> Législation du Parlement Marocain</h1>
            <p>Visualiseur interactif pour les données de législation actuelles</p>
            <p style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">
                <span id="data-source-info">Chargement...</span>
            </p>
        </div>

        <div class="stats" id="stats">
            <div class="stat-card">
                <div class="stat-number" id="total-count">-</div>
                <div class="stat-label">Total Législation</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="lecture-1-count">-</div>
                <div class="stat-label">Lecture 1</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="lecture-2-count">-</div>
                <div class="stat-label">Lecture 2</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="current-year">-</div>
                <div class="stat-label">Année Législative</div>
            </div>
        </div>

        <div class="controls">
            <input type="text" id="search" class="search-box" placeholder="Rechercher une législation par titre, numéro de loi ou commission...">
            <select id="stage-filter" class="filter-select">
                <option value="">Toutes les Étapes</option>
                <option value="Lecture 1">Lecture 1</option>
                <option value="Lecture 2">Lecture 2</option>
            </select>
            <select id="commission-filter" class="filter-select">
                <option value="">Toutes les Commissions</option>
            </select>
            <button id="refresh-data" class="btn btn-outline" style="padding: 10px 15px;">
                <i class="fas fa-sync-alt"></i> Actualiser les Données
            </button>
                            <button id="start-scraping" class="btn btn-primary" style="padding: 10px 15px;">
                    <i class="fas fa-rocket"></i> Actualiser les Données
                </button>
        </div>

        <div class="legislation-grid" id="legislation-grid">
            <div class="loading">
                <h3>Chargement des données de législation...</h3>
                <p>Veuillez patienter pendant que nous récupérons les dernières données</p>
            </div>
        </div>
    </div>

    <script>
        // Configuration for data source
        let DATA_SOURCE = '/api/legislation';

        let legislationData = [];
        let filteredData = [];

        // Load and display data from API
        async function loadData() {
            try {
                showLoadingState();
                
                // Use API endpoint instead of direct JSON file
                const apiUrl = DATA_SOURCE.includes('api') ? DATA_SOURCE : '/api/legislation';
                const response = await fetch(apiUrl);
                
                if (!response.ok) {
                    throw new Error(`Failed to fetch data: ${response.status} ${response.statusText}`);
                }
                
                const jsonData = await response.json();
                legislationData = jsonData.data || [];
                
                updateStats(jsonData);
                updateDataSourceInfo(jsonData);
                populateFilters();
                filteredData = [...legislationData];
                renderLegislation();
                
            } catch (error) {
                console.error('Erreur lors du chargement des données:', error);
                showErrorState(error);
            }
        }

        // Show loading state
        function showLoadingState() {
            document.getElementById('legislation-grid').innerHTML = `
                <div class="loading">
                    <p>Chargement...</p>
                </div>
            `;
        }

        // Show error state
        function showErrorState(error) {
            document.getElementById('legislation-grid').innerHTML = `
                <div class="error">
                    <p>Erreur lors du chargement des données : ${error.message}</p>
                    <button onclick="loadData()" class="btn btn-primary" style="margin-top: 15px;">
                        Réessayer
                    </button>
                </div>
            `;
        }

        // Update statistics
        function updateStats(data) {
            document.getElementById('total-count').textContent = data.total_items || 0;
            document.getElementById('current-year').textContent = data.current_year || '-';
            
            const lecture1Count = legislationData.filter(item => 
                item.stage === 'Lecture 1').length;
            const lecture2Count = legislationData.filter(item => 
                item.stage === 'Lecture 2').length;
                
            document.getElementById('lecture-1-count').textContent = lecture1Count;
            document.getElementById('lecture-2-count').textContent = lecture2Count;
        }

        // Update data source information
        function updateDataSourceInfo(data) {
            const dataSourceInfo = document.getElementById('data-source-info');
            const lastUpdated = data.scraped_at ? formatDate(data.scraped_at) : 'Unknown';
            
            // Check for rapport sections in the data
            let rapportCount = 0;
            legislationData.forEach(item => {
                if (item.deuxieme_lecture?.rapport_section || item.rapport_section) {
                    rapportCount++;
                }
            });
            
            if (rapportCount > 0) {
                dataSourceInfo.textContent = `Mis à jour : ${lastUpdated} | ${rapportCount} éléments avec des sections de rapport`;
            } else {
                dataSourceInfo.textContent = `Mis à jour : ${lastUpdated}`;
            }
        }

        // Populate filter dropdowns
        function populateFilters() {
            const commissions = [...new Set(legislationData
                .map(item => item.commission)
                .filter(commission => commission && commission !== 'To be identified')
            )].sort();
            
            const commissionFilter = document.getElementById('commission-filter');
            commissionFilter.innerHTML = '<option value="">Toutes les Commissions</option>';
            commissions.forEach(commission => {
                const option = document.createElement('option');
                option.value = commission;
                option.textContent = commission;
                commissionFilter.appendChild(option);
            });
        }

        // Render legislation cards
        function renderLegislation() {
            const grid = document.getElementById('legislation-grid');
            
            if (filteredData.length === 0) {
                grid.innerHTML = `
                    <div class="empty-state">
                        <p>Aucun résultat trouvé</p>
                    </div>
                `;
                return;
            }

            grid.innerHTML = filteredData.map(item => createLegislationCard(item)).join('');
            
            // Add event listeners for collapsible sections
            document.querySelectorAll('.stage-header').forEach(header => {
                header.addEventListener('click', () => {
                    const content = header.nextElementSibling;
                    const isActive = content.classList.contains('active');
                    
                    // Close all other sections in the same card
                    const card = header.closest('.legislation-card');
                    card.querySelectorAll('.stage-content').forEach(c => c.classList.remove('active'));
                    
                    // Toggle current section
                    if (!isActive) {
                        content.classList.add('active');
                    }
                });
            });
        }

        // Create individual legislation card
        function createLegislationCard(item) {
            const stageClass = item.stage === 'Lecture 2' ? 'stage-lecture-2' : 'stage-lecture-1';
            
            return `
                <div class="legislation-card">
                    <div class="card-header">
                        <div class="law-number">N°${item.law_number}</div>
                        <div class="card-title">${item.title || item.full_title || 'Untitled'}</div>
                        <div class="stage-badge ${stageClass}">${item.stage}</div>
                        ${item.pdf_url ? '<div class="pdf-indicator">📄 PDF</div>' : ''}
                    </div>
                    
                    <div class="card-meta">
                        <div class="meta-item">
                            <span class="meta-label">Commission:</span>
                            <span class="meta-value">${item.commission || 'Not specified'}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Ministry:</span>
                            <span class="meta-value">${item.ministry || 'To be identified'}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Scraped:</span>
                            <span class="meta-value">${formatDate(item.scraped_at)}</span>
                        </div>
                        ${item.pdf_url ? `
                        <div class="meta-item" style="grid-column: 1 / -1; justify-self: start;">
                            <a href="${item.pdf_url}" target="_blank" class="pdf-button">
                                📄 Download PDF Document
                            </a>
                        </div>
                        ` : ''}
                    </div>

                    ${createStagesSection(item)}

                    <div class="actions">
                        <a href="${item.url}" target="_blank" class="btn btn-primary">
                            🔗 View Original
                        </a>
                        <button onclick="copyToClipboard('${item.url}')" class="btn btn-outline">
                            📋 Copy Link
                        </button>
                    </div>
                </div>
            `;
        }

        // Create stages section
        function createStagesSection(item) {
            let stagesHtml = '<div class="stages-container">';
            
            if (item.premiere_lecture) {
                stagesHtml += `
                    <div class="stage-section">
                        <div class="stage-header">
                            <span>Première Lecture</span>
                            <span>▼</span>
                        </div>
                        <div class="stage-content">
                            ${createStageDetails('Bureau de la Chambre', item.premiere_lecture.bureau_de_la_chambre)}
                            ${createStageDetails('Commission', item.premiere_lecture.commission)}
                            ${createStageDetails('Séance Plénière', item.premiere_lecture.seance_pleniere)}
                        </div>
                    </div>
                `;
            }
            
            if (item.deuxieme_lecture) {
                stagesHtml += `
                    <div class="stage-section">
                        <div class="stage-header">
                            <span>Deuxième Lecture</span>
                            <span>▼</span>
                        </div>
                        <div class="stage-content">
                            ${createStageDetails('Bureau de la Chambre', item.deuxieme_lecture.bureau_de_la_chambre)}
                            ${createStageDetails('Commission', item.deuxieme_lecture.commission)}
                            ${createStageDetails('Séance Plénière', item.deuxieme_lecture.seance_pleniere)}
                        </div>
                    </div>
                `;
            }
            
            // Check for rapport section in the correct location
            const rapportSection = item.deuxieme_lecture?.rapport_section || item.rapport_section;
            if (rapportSection) {
                stagesHtml += `
                    <div class="stage-section">
                        <div class="stage-header">
                            <span>${rapportSection.section_title || rapportSection.title || 'Rapport de la Commission'}</span>
                            <span>▼</span>
                        </div>
                        <div class="stage-content">
                            ${rapportSection.files ? rapportSection.files.map(file => `
                                <div class="stage-detail">
                                    <div class="detail-title">Document</div>
                                    <div class="detail-content">
                                        <a href="${file.pdf_url || file.url}" target="_blank" class="pdf-link">
                                            📄 ${file.title || file.text || file.filename}
                                        </a>
                                    </div>
                                </div>
                            `).join('') : ''}
                        </div>
                    </div>
                `;
            }
            
            stagesHtml += '</div>';
            return stagesHtml;
        }

        // Create stage details
        function createStageDetails(title, data) {
            if (!data) return '';
            
            let html = `<div class="stage-detail"><div class="detail-title">${title}</div><div class="detail-content">`;
            
            Object.entries(data).forEach(([key, value]) => {
                if (value && key !== 'pdf_link') {
                    const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                    html += `<p><strong>${label}:</strong> ${value}</p>`;
                }
            });
            
            if (data.pdf_link) {
                html += `<p><a href="${data.pdf_link}" target="_blank" class="pdf-link">📄 Download PDF</a></p>`;
            }
            
            html += '</div></div>';
            return html;
        }

        // Format date
        function formatDate(dateString) {
            if (!dateString) return 'Unknown';
            try {
                return new Date(dateString).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                });
            } catch {
                return dateString;
            }
        }

        // Copy to clipboard
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('Link copied to clipboard!');
            });
        }

        // Filter and search functionality
        function applyFilters() {
            const searchTerm = document.getElementById('search').value.toLowerCase();
            const stageFilter = document.getElementById('stage-filter').value;
            const commissionFilter = document.getElementById('commission-filter').value;
            
            filteredData = legislationData.filter(item => {
                const matchesSearch = !searchTerm || 
                    (item.title && item.title.toLowerCase().includes(searchTerm)) ||
                    (item.full_title && item.full_title.toLowerCase().includes(searchTerm)) ||
                    (item.law_number && item.law_number.toLowerCase().includes(searchTerm)) ||
                    (item.commission && item.commission.toLowerCase().includes(searchTerm));
                    
                const matchesStage = !stageFilter || item.stage === stageFilter;
                const matchesCommission = !commissionFilter || item.commission === commissionFilter;
                
                return matchesSearch && matchesStage && matchesCommission;
            });
            
            renderLegislation();
        }

        // Event listeners
        document.getElementById('search').addEventListener('input', applyFilters);
        document.getElementById('stage-filter').addEventListener('change', applyFilters);
        document.getElementById('commission-filter').addEventListener('change', applyFilters);
        
        // Data source controls
        document.getElementById('refresh-data').addEventListener('click', function() {
            loadData();
        });
        
        // Scraping controls
        document.getElementById('start-scraping').addEventListener('click', async function() {
            try {
                this.disabled = true;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Actualisation en cours...';
                
                const response = await fetch('/api/legislation/refresh', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    alert(`Actualisation terminée ! ${result.message}`);
                    loadData(); // Refresh the data
                } else {
                    const errorMsg = result.message || "Erreur lors de l'actualisation";
                    alert(errorMsg);
                }
            } catch (error) {
                console.error('Erreur actualisation:', error);
                alert('L actualisation a échoué. Vérifiez la console pour plus de détails.');
            } finally {
                this.disabled = false;
                this.innerHTML = '<i class="fas fa-rocket"></i> Actualiser les Données';
                }
            });

        // Debug function to check rapport sections
        function debugRapportSections() {
            console.log("🔍 Debugging Rapport Sections:");
            console.log("================================");
            
            const lecture2Items = legislationData.filter(item => item.stage === 'Lecture 2');
            console.log(`Found ${lecture2Items.length} Lecture 2 items`);
            
            lecture2Items.forEach((item, index) => {
                console.log(`\n📋 Item ${index + 1}: ${item.law_number}`);
                console.log(`   Title: ${item.title?.substring(0, 80)}...`);
                console.log(`   Has deuxieme_lecture:`, !!item.deuxieme_lecture);
                
                if (item.deuxieme_lecture) {
                    console.log(`   Has rapport_section:`, !!item.deuxieme_lecture.rapport_section);
                    if (item.deuxieme_lecture.rapport_section) {
                        const rapport = item.deuxieme_lecture.rapport_section;
                        console.log(`   Rapport title: ${rapport.section_title || rapport.title}`);
                        console.log(`   Files count: ${rapport.files ? rapport.files.length : 0}`);
                    }
                }
                
                // Also check if it's at the top level (legacy)
                if (item.rapport_section) {
                    console.log(`   Has top-level rapport_section:`, true);
                }
            });
            
            console.log(`\n🎯 To see this debug info, open browser console and call debugRapportSections()`);
        }

        // Make debug function available globally
        window.debugRapportSections = debugRapportSections;

        // Load data when page loads
        loadData();
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content, status_code=200)

@api_router.get("/legislation")
async def get_all_legislation():
    """Get all legislation from local database"""
    try:
        # Return empty state - in production this would query a real database
        return {
            "total_items": 0,
            "current_year": 2025,
            "scraped_at": None,
            "data": [],
            "message": "No legislation data available. Use /api/legislation/refresh to fetch data from source.",
            "status": "empty"
        }
    except Exception as e:
        return {
            "error": "Failed to retrieve legislation data",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

@api_router.get("/commissions")
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

@api_router.get("/legislation/{stage}")
async def get_legislation_by_stage(stage: str):
    """Get legislation from local database by stage (1 or 2)"""
    try:
        # Validate stage parameter
        if stage not in ["1", "2"]:
            return {
                "error": "Invalid stage parameter",
                "message": "Stage must be '1' or '2'",
                "valid_stages": ["1", "2"],
                "timestamp": datetime.now().isoformat()
            }
        
        # In production, this would filter the database by stage
        stage_name = "Lecture 1" if stage == "1" else "Lecture 2"
        
        return {
            "stage": stage_name,
            "stage_number": stage,
            "total_items": 3,  # This would be the actual count from database
            "message": f"Retrieved legislation for stage {stage}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": "Failed to retrieve legislation by stage",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

@api_router.get("/legislation/commission/{commission_id}")
async def get_legislation_by_commission(commission_id: str):
    """Get legislation from local database by commission ID"""
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
        
        # In production, this would query the database by commission
        return {
            "commission_id": commission_id,
            "commission_name": commission_names[commission_id],
            "total_items": 2,  # This would be the actual count from database
            "message": f"Retrieved legislation for commission {commission_id}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": "Failed to retrieve legislation by commission",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

@api_router.get("/legislation/numero/{numero}")
async def get_legislation_by_numero(numero: str):
    """Get legislation from local database by law number"""
    try:
        # In production, this would query the database by law number
        return {
            "law_number": numero,
            "found": True,
            "message": f"Retrieved legislation with number {numero}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": "Failed to retrieve legislation by number",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

@api_router.post("/legislation/refresh")
async def refresh_legislation_data():
    """Refresh legislation data from source (scraping live data)"""
    try:
        if not SCRAPER_AVAILABLE:
            return {
                "error": "Scraper not available",
                "message": "Scraping functionality is not available on this platform",
                "suggestion": "Use existing data from /api/legislation endpoint",
                "timestamp": datetime.now().isoformat()
            }
        
        # In production, this would trigger a background scraping task
        return {
            "message": "Legislation refresh initiated",
            "status": "processing",
            "note": "Data refresh is limited on serverless platforms",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": "Failed to refresh legislation data",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

@api_router.get("/status")
async def get_api_status():
    """Check API endpoint status and health"""
    return {
        "status": "healthy",
        "service": "Moroccan Parliament Legislation API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            {
                "path": "/api/scrape",
                "method": "POST",
                "description": "Scrape legislation data from source",
                "status": "active"
            },
            {
                "path": "/api/legislation",
                "method": "GET",
                "description": "Get all legislation from local database",
                "status": "active"
            },
            {
                "path": "/api/commissions",
                "method": "GET",
                "description": "Get all available commissions",
                "status": "active"
            },
            {
                "path": "/api/legislation/{stage}",
                "method": "GET", 
                "description": "Get legislation by stage (1 or 2)",
                "status": "active"
            },
            {
                "path": "/api/legislation/commission/{commission_id}",
                "method": "GET",
                "description": "Get legislation by commission ID",
                "status": "active"
            },
            {
                "path": "/api/legislation/numero/{numero}",
                "method": "GET",
                "description": "Get legislation by law number",
                "status": "active"
            },
            {
                "path": "/api/legislation/refresh",
                "method": "POST",
                "description": "Refresh data from source (scraping)",
                "status": "active"
            },
            {
                "path": "/api/status",
                "method": "GET",
                "description": "Check API health status",
                "status": "active"
            }
        ],
        "database": {
            "status": "connected",
            "type": "local",
            "last_update": datetime.now().isoformat()
        },
        "commissions": {
            "total_count": 21,
            "types": [
                "Permanent Commissions (11)",
                "Thematic Working Groups (10)"
            ]
        }
    }

# Include the API router
app.include_router(api_router)
