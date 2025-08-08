from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.inventory_service import inventory_service
from datetime import datetime

movement_bp = Blueprint('movements', __name__)

@movement_bp.route('/')
def list_movements():
    """Liste des mouvements de stock"""
    produit_id = request.args.get('produit')
    type_filtre = request.args.get('type', '')
    page = int(request.args.get('page', 1))
    par_page = 50
    
    mouvements = inventory_service.obtenir_mouvements(produit_id)
    
    # Filtrer par type si spécifié
    if type_filtre:
        mouvements = [m for m in mouvements if m.type_mouvement == type_filtre]
    
    # Pagination
    total_mouvements = len(mouvements)
    debut = (page - 1) * par_page
    fin = debut + par_page
    mouvements_page = mouvements[debut:fin]
    
    # Enrichir avec les informations produit
    mouvements_avec_produit = []
    for mouvement in mouvements_page:
        produit = inventory_service.obtenir_produit(mouvement.produit_id)
        mouvement_dict = mouvement.to_dict()
        mouvement_dict['produit'] = produit.to_dict() if produit else None
        mouvements_avec_produit.append(mouvement_dict)
    
    pages_totales = (total_mouvements + par_page - 1) // par_page
    produits = inventory_service.obtenir_tous_produits()
    
    return render_template('movements/list.html',
                         mouvements=mouvements_avec_produit,
                         produits=produits,
                         produit_selectionne=produit_id,
                         type_selectionne=type_filtre,
                         page_courante=page,
                         pages_totales=pages_totales,
                         total_mouvements=total_mouvements)

@movement_bp.route('/ajouter', methods=['GET', 'POST'])
def add_movement():
    """Ajouter un mouvement de stock"""
    if request.method == 'POST':
        try:
            produit_id = request.form.get('produit_id')
            type_mouvement = request.form.get('type_mouvement')
            quantite = int(request.form.get('quantite', 0))
            motif = request.form.get('motif', '').strip()
            prix_unitaire = request.form.get('prix_unitaire')
            
            # Validation
            if not produit_id:
                flash('Veuillez sélectionner un produit.', 'danger')
                return render_template('movements/add.html', produits=inventory_service.obtenir_tous_produits())
            
            produit = inventory_service.obtenir_produit(produit_id)
            if not produit:
                flash('Produit introuvable.', 'danger')
                return render_template('movements/add.html', produits=inventory_service.obtenir_tous_produits())
            
            if quantite <= 0:
                flash('La quantité doit être positive.', 'danger')
                return render_template('movements/add.html', produits=inventory_service.obtenir_tous_produits())
            
            # Prix unitaire par défaut selon le type de mouvement
            if not prix_unitaire:
                if type_mouvement == 'ENTREE':
                    prix_unitaire = produit.prix_achat
                else:
                    prix_unitaire = produit.prix_vente
            else:
                prix_unitaire = float(prix_unitaire)
            
            # Effectuer le mouvement selon le type
            if type_mouvement == 'ENTREE':
                mouvement = inventory_service.effectuer_entree_stock(
                    produit_id, quantite, motif or "Approvisionnement", prix_unitaire
                )
                flash(f'Entrée de stock effectuée: {quantite} unités de "{produit.nom}".', 'success')
            elif type_mouvement == 'SORTIE':
                mouvement = inventory_service.effectuer_sortie_stock(
                    produit_id, quantite, motif or "Vente", prix_unitaire
                )
                flash(f'Sortie de stock effectuée: {quantite} unités de "{produit.nom}".', 'success')
            else:
                flash('Type de mouvement invalide.', 'danger')
                return render_template('movements/add.html', produits=inventory_service.obtenir_tous_produits())
            
            return redirect(url_for('movements.list_movements'))
            
        except ValueError as e:
            flash(f'Erreur: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Erreur inattendue: {str(e)}', 'danger')
    
    produits = inventory_service.obtenir_tous_produits()
    # Trier par nom pour faciliter la sélection
    produits.sort(key=lambda x: x.nom.lower())
    
    return render_template('movements/add.html', produits=produits)

@movement_bp.route('/ajuster', methods=['GET', 'POST'])
def adjust_stock():
    """Ajuster le stock d'un produit"""
    if request.method == 'POST':
        try:
            produit_id = request.form.get('produit_id')
            nouvelle_quantite = int(request.form.get('nouvelle_quantite', 0))
            motif = request.form.get('motif', 'Ajustement d\'inventaire').strip()
            
            # Validation
            if not produit_id:
                flash('Veuillez sélectionner un produit.', 'danger')
                return render_template('movements/adjust.html', produits=inventory_service.obtenir_tous_produits())
            
            produit = inventory_service.obtenir_produit(produit_id)
            if not produit:
                flash('Produit introuvable.', 'danger')
                return render_template('movements/adjust.html', produits=inventory_service.obtenir_tous_produits())
            
            if nouvelle_quantite < 0:
                flash('La quantité ne peut pas être négative.', 'danger')
                return render_template('movements/adjust.html', produits=inventory_service.obtenir_tous_produits())
            
            ancienne_quantite = produit.quantite
            inventory_service.ajuster_stock(produit_id, nouvelle_quantite, motif)
            
            flash(f'Stock ajusté pour "{produit.nom}": {ancienne_quantite} → {nouvelle_quantite} unités.', 'success')
            return redirect(url_for('movements.list_movements'))
            
        except Exception as e:
            flash(f'Erreur: {str(e)}', 'danger')
    
    produits = inventory_service.obtenir_tous_produits()
    produits.sort(key=lambda x: x.nom.lower())
    
    return render_template('movements/adjust.html', produits=produits)
