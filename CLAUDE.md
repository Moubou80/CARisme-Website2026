# CLAUDE.md — Site CARisme (carisme.fr)

> Contexte projet pour tout agent (Claude Code, etc.) travaillant sur ce repo.
> Repo **public** : ne JAMAIS y écrire de secret (identifiants SMTP, URLs de webhooks privés, comptes de service, UUID de déploiement, clés API).

## 1. Le projet
- **CARisme** : maison premium — **location automobile** (avec ou sans chauffeur), **importation** et **personnalisation** de véhicules, ainsi qu'un univers lifestyle (**montres**, **sacs**).
- Site **vitrine statique** en ligne : https://carisme.fr
- Langue : **français**. Ton : **chic, premium, désirable** — élégant et soigné (univers luxe, pas « low-cost »).

## 2. Stack & déploiement
- 100 % **statique** : HTML + CSS + JS (pas de framework, pas de build).
- Servi par **nginx**, déploiement **automatique via Coolify** : un `git push` sur `main` suffit. **Aucune étape manuelle.**
- Flux : modifier → `git add -A` → `git commit` → `git push`.
- Toujours `git pull` au début, avant toute modif (repo multi-machines, GitHub = source de vérité).

## 3. Structure des fichiers
- Accueil : `index.html`
- Parcours location : `type-location.html` → `flotte-conduis.html` (sans chauffeur) / `flotte-chauffeur.html` (avec chauffeur)
- Fiches véhicules : `a3-detail.html`, `rs3-detail.html`, `golf-detail.html`, `cupra-detail.html`, `clio-noire-detail.html`, `clio-gris-detail.html`, `troc-detail.html`
- Lifestyle : `montres.html`, `sacs.html`
- Légal : `mentions-legales.html`, `cgv.html`, `politique-confidentialite.html`
- ⚠️ **Le CSS est inline** dans un bloc `<style>` des pages (pas de fichier `assets/styles.css` séparé comme sur BETALIS). Pour modifier la charte, rester cohérent d'une page à l'autre.

## 4. Charte graphique (à respecter absolument)
- **Polices** : `--serif: 'Playfair Display'` (titres, élégance) · `--sans: 'Jost'` (corps, léger).
- **Palette** (variables CSS) :
  - `--dark:#1A1612` (fond profond) · `--charcoal:#2C2620`
  - `--cream:#F5F0E8` · `--warm:#EDE5D5` (clairs chauds)
  - `--gold:#B8965A` · `--gold-lt:#D4AF74` (accents or — signature de la marque)
  - `--muted:rgba(26,22,18,0.45)`
- Esprit : **or sur fond sombre**, raffiné, beaucoup d'air. Réutiliser les classes/sections existantes plutôt que d'inventer du style.

## 5. Conventions
- Terminal **zsh** : ne JAMAIS mettre de commentaire `#` en ligne dans un bloc de commandes.
- Toute nouvelle page reprend la structure existante (head : title + meta + canonical + og + favicons + fonts ; nav ; contenu ; footer ; scripts). Garder la nav et le footer **cohérents sur toutes les pages**.
- Contenu en français, registre premium.

## 6. Formulaires (via n8n)
- **Liste d'attente Montres** (`montres.html`) et **Liste d'attente Sacs** (`sacs.html`) → enregistrées dans Google Sheets via des webhooks n8n.
- **Formulaire chauffeur** (`flotte-chauffeur.html`) → Google Sheets + notification email.
- Les URLs de webhook sont déjà dans le JS des pages concernées. Ne pas renommer les champs côté front sans adapter le workflow n8n correspondant.

## 7. Cookies & Analytics (conformité CNIL)
- **Bandeau de consentement RGPD** déjà en place. Google Analytics (`G-Y0FLSM78CM`) ne doit se charger **qu'après consentement**.
- ⚠️ Ne jamais coller le snippet GA en dur sans le piloter par le consentement.

## 8. Pipeline images
- Visuels générés via **Gemini** (`gemini-3.1-flash-image-preview`) orchestré par n8n, puis publiés (GitHub → Coolify).
- Style attendu : **photographie automobile premium**, cohérente avec l'univers luxe (lumière soignée, fonds sobres, accents or).
- Les images générées par le studio Telegram arrivent dans `images/<slug>.jpg` — pour en intégrer une, référencer ce chemin exact (le slug est renvoyé par le bot).

## 9. Données société (publiques — pages légales)
- **CARisme**, SAS — **RCS Versailles 993 656 404**.
- Siège : **1703 Route de 40 sous, 78630 Orgeval**.
- Contact : `contact@carisme.fr`.
- (Données complètes : voir `mentions-legales.html`.)

## 10. Recettes
**Ajouter un véhicule à la flotte :**
1. Dupliquer une fiche existante (ex. `a3-detail.html`) comme modèle.
2. Adapter : `<title>`, meta, canonical, og, le contenu (modèle, specs, prix, photos), les images.
3. Ajouter la vignette du véhicule dans la page flotte concernée (`flotte-conduis.html` et/ou `flotte-chauffeur.html`) + le parcours `type-location.html`.
4. Ajouter l'URL au `sitemap.xml`.
5. Commit + push.

**Ajouter / mettre à jour une page lifestyle (montres, sacs)** : repartir de la page existante, garder la charte, mettre à jour visuels + textes + formulaire de liste d'attente.

## 11. Règles d'or / à NE PAS faire
- ❌ Aucun secret dans ce repo (public).
- ❌ Ne pas publier de **contenu juridique** (CGV, mentions, confidentialité) sans relecture humaine. *(Note : `cgv.html` existe déjà mais contient du contenu **placeholder** à compléter avec les vraies conditions.)*
- ❌ Ne pas casser la charte « or sur fond sombre » ni la cohérence nav/footer.
- ✅ Toute modif multi-pages (nav, footer) appliquée **partout**.
- ✅ Vérifier le rendu, puis `git push` (le déploiement suit tout seul).
