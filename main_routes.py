from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.inventory_service import inventory_service
from services.statistics_service import statistics_service

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Page d'accueil avec tableau de bord"""
    stats = statistics_service.calculer_statistiques_generales()
    produits_recents = inventory_service.rechercher_produits(tri="date_creation")[:5]
    mouvements_recents = inventory_service.obtenir_mouvements(limite=5)
    alertes = statistics_service.obtenir_alertes_stock()[:5]
    
    # Enrichir les mouvements avec les informations produit
    mouvements_avec_produit = []
    for mouvement in mouvements_recents:
        produit = inventory_service.obtenir_produit(mouvement.produit_id)
        mouvement_dict = mouvement.to_dict()
        mouvement_dict['produit'] = produit.to_dict() if produit else None
        mouvements_avec_produit.append(mouvement_dict)
    
    return render_template('index.html', 
                         stats=stats,
                         produits_recents=produits_recents,
                         mouvements_recents=mouvements_avec_produit,
                         alertes=alertes)

@main_bp.route('/alertes')
def alertes_stock():
    """Page des alertes de stock faible"""
    alertes = statistics_service.obtenir_alertes_stock()
    return render_template('alerts/low_stock.html', alertes=alertes)

@main_bp.route('/export')
def exporter_donnees():
    """Export des données d'inventaire"""
    from flask import jsonify
    donnees = inventory_service.exporter_donnees()
    return jsonify(donnees)
