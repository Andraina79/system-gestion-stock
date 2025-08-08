from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.inventory_service import inventory_service

product_bp = Blueprint('products', __name__)

@product_bp.route('/')
def list_products():
    """Liste des produits avec recherche et tri"""
    terme_recherche = request.args.get('recherche', '')
    categorie = request.args.get('categorie', '')
    tri = request.args.get('tri', 'nom')
    page = int(request.args.get('page', 1))
    par_page = 20
    
    produits = inventory_service.rechercher_produits(terme_recherche, categorie, tri)
    categories = inventory_service.obtenir_categories()
    
    # Pagination simple
    total_produits = len(produits)
    debut = (page - 1) * par_page
    fin = debut + par_page
    produits_page = produits[debut:fin]
    
    pages_totales = (total_produits + par_page - 1) // par_page
    
    return render_template('products/list.html',
                         produits=produits_page,
                         categories=categories,
                         terme_recherche=terme_recherche,
                         categorie_selectionnee=categorie,
                         tri_selectionne=tri,
                         page_courante=page,
                         pages_totales=pages_totales,
                         total_produits=total_produits)

@product_bp.route('/ajouter', methods=['GET', 'POST'])
def add_product():
    """Ajouter un nouveau produit"""
    if request.method == 'POST':
        try:
            nom = request.form.get('nom', '').strip()
            categorie = request.form.get('categorie', '').strip()
            quantite = int(request.form.get('quantite', 0))
            prix_achat = float(request.form.get('prix_achat', 0))
            prix_vente = float(request.form.get('prix_vente', 0))
            seuil_minimal = int(request.form.get('seuil_minimal', 5))
            code = request.form.get('code', '').strip()
            
            # Validation
            if not nom:
                flash('Le nom du produit est obligatoire.', 'danger')
                return render_template('products/add.html')
            
            if not categorie:
                flash('La catégorie est obligatoire.', 'danger')
                return render_template('products/add.html')
            
            if prix_achat < 0 or prix_vente < 0:
                flash('Les prix ne peuvent pas être négatifs.', 'danger')
                return render_template('products/add.html')
            
            if quantite < 0:
                flash('La quantité ne peut pas être négative.', 'danger')
                return render_template('products/add.html')
            
            # Ajouter le produit
            produit = inventory_service.ajouter_produit(
                nom, categorie, quantite, prix_achat, prix_vente, seuil_minimal, code
            )
            
            flash(f'Produit "{nom}" ajouté avec succès (Code: {produit.code}).', 'success')
            return redirect(url_for('products.list_products'))
            
        except ValueError as e:
            flash(f'Erreur: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Erreur inattendue: {str(e)}', 'danger')
    
    categories_existantes = inventory_service.obtenir_categories()
    return render_template('products/add.html', categories_existantes=categories_existantes)

@product_bp.route('/<product_id>/modifier', methods=['GET', 'POST'])
def edit_product(product_id):
    """Modifier un produit existant"""
    produit = inventory_service.obtenir_produit(product_id)
    if not produit:
        flash('Produit introuvable.', 'danger')
        return redirect(url_for('products.list_products'))
    
    if request.method == 'POST':
        try:
            nom = request.form.get('nom', '').strip()
            categorie = request.form.get('categorie', '').strip()
            prix_achat = float(request.form.get('prix_achat', 0))
            prix_vente = float(request.form.get('prix_vente', 0))
            seuil_minimal = int(request.form.get('seuil_minimal', 5))
            
            # Validation
            if not nom:
                flash('Le nom du produit est obligatoire.', 'danger')
                return render_template('products/edit.html', produit=produit)
            
            if not categorie:
                flash('La catégorie est obligatoire.', 'danger')
                return render_template('products/edit.html', produit=produit)
            
            if prix_achat < 0 or prix_vente < 0:
                flash('Les prix ne peuvent pas être négatifs.', 'danger')
                return render_template('products/edit.html', produit=produit)
            
            # Modifier le produit
            inventory_service.modifier_produit(
                product_id, nom=nom, categorie=categorie, 
                prix_achat=prix_achat, prix_vente=prix_vente, 
                seuil_minimal=seuil_minimal
            )
            
            flash(f'Produit "{nom}" modifié avec succès.', 'success')
            return redirect(url_for('products.list_products'))
            
        except Exception as e:
            flash(f'Erreur: {str(e)}', 'danger')
    
    categories_existantes = inventory_service.obtenir_categories()
    return render_template('products/edit.html', produit=produit, categories_existantes=categories_existantes)

@product_bp.route('/<product_id>/supprimer', methods=['POST'])
def delete_product(product_id):
    """Supprimer un produit"""
    try:
        produit = inventory_service.obtenir_produit(product_id)
        if not produit:
            flash('Produit introuvable.', 'danger')
        else:
            nom = produit.nom
            inventory_service.supprimer_produit(product_id)
            flash(f'Produit "{nom}" supprimé avec succès.', 'success')
    except Exception as e:
        flash(f'Erreur lors de la suppression: {str(e)}', 'danger')
    
    return redirect(url_for('products.list_products'))

@product_bp.route('/<product_id>/details')
def product_details(product_id):
    """Détails d'un produit avec historique des mouvements"""
    produit = inventory_service.obtenir_produit(product_id)
    if not produit:
        flash('Produit introuvable.', 'danger')
        return redirect(url_for('products.list_products'))
    
    mouvements = inventory_service.obtenir_mouvements(product_id, limite=50)
    mouvements_dict = [m.to_dict() for m in mouvements]
    
    return render_template('products/details.html', 
                         produit=produit, 
                         mouvements=mouvements_dict)
