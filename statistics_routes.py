from flask import Blueprint, render_template, request, jsonify
from services.statistics_service import statistics_service

statistics_bp = Blueprint('statistics', __name__)

@statistics_bp.route('/')
def dashboard():
    """Tableau de bord des statistiques"""
    stats_generales = statistics_service.calculer_statistiques_generales()
    produits_plus_vendus = statistics_service.obtenir_produits_plus_vendus(10)
    produits_plus_stockes = statistics_service.obtenir_produits_plus_stockes(10)
    repartition_categories = statistics_service.obtenir_repartition_par_categorie()
    evolution_stock = statistics_service.obtenir_evolution_stock(30)
    alertes = statistics_service.obtenir_alertes_stock()
    
    return render_template('statistics/dashboard.html',
                         stats_generales=stats_generales,
                         produits_plus_vendus=produits_plus_vendus,
                         produits_plus_stockes=produits_plus_stockes,
                         repartition_categories=repartition_categories,
                         evolution_stock=evolution_stock,
                         alertes=alertes)

@statistics_bp.route('/api/evolution-stock')
def api_evolution_stock():
    """API pour l'évolution du stock (pour les graphiques)"""
    jours = int(request.args.get('jours', 30))
    evolution = statistics_service.obtenir_evolution_stock(jours)
    return jsonify(evolution)

@statistics_bp.route('/api/repartition-categories')
def api_repartition_categories():
    """API pour la répartition par catégories (pour les graphiques)"""
    repartition = statistics_service.obtenir_repartition_par_categorie()
    return jsonify(repartition)
