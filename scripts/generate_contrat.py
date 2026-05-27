#!/usr/bin/env python3
"""CARisme - Genere le contrat de location PDF remplissable (2 pages A4)."""

from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white

# ─── Palette ────────────────────────────────────────────────────────────────
GOLD   = HexColor('#B8965A')
DARK   = HexColor('#1A1612')
CREAM  = HexColor('#F5F0E8')
MUTED  = HexColor('#888077')
BORDER = HexColor('#CCBFA8')
FIELD  = HexColor('#FDFCFA')
ALT    = HexColor('#F5F2EE')

# ─── Mise en page ────────────────────────────────────────────────────────────
W, H = A4          # 595.27 x 841.89 pt
ML = MR = 40
MT = MB = 30
IW = W - ML - MR   # ~515 pt

# ─── Sortie ─────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
OUT  = ROOT / 'output' / 'contrat-location-carisme.pdf'
OUT.parent.mkdir(exist_ok=True)

cv   = canvas.Canvas(str(OUT), pagesize=A4)
form = cv.acroForm


# ════════════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════════════

def hline(y, x1=None, x2=None, color=BORDER, lw=0.4):
    x1 = x1 if x1 is not None else ML
    x2 = x2 if x2 is not None else W - MR
    cv.saveState()
    cv.setStrokeColor(color)
    cv.setLineWidth(lw)
    cv.line(x1, y, x2, y)
    cv.restoreState()


def section_bar(y, title):
    """Barre de section sombre avec accent dore. Retourne y en bas de la barre."""
    bh = 18
    cv.saveState()
    cv.setFillColor(DARK)
    cv.rect(ML, y - bh, IW, bh, fill=1, stroke=0)
    cv.setFillColor(GOLD)
    cv.rect(ML, y - bh, 4, bh, fill=1, stroke=0)
    cv.setFont('Helvetica-Bold', 8)
    cv.drawString(ML + 12, y - bh + 6, title)
    cv.restoreState()
    return y - bh


def label_field(name, label, x, y, w, fh=17):
    """Label + champ AcroForm remplissable."""
    cv.saveState()
    cv.setFillColor(MUTED)
    cv.setFont('Helvetica', 6.5)
    cv.drawString(x, y + fh + 2, label)
    cv.restoreState()
    form.textfield(
        name=name,
        tooltip=label,
        x=x, y=y,
        width=w, height=fh,
        fontSize=9,
        textColor=DARK,
        fillColor=FIELD,
        borderColor=BORDER,
        borderWidth=0.5,
        fieldFlags='doNotSpellCheck',
        forceBorder=True,
    )


RH = 34  # hauteur de ligne : label(8) + champ(17) + inter(9)


def row2(y, n1, l1, n2, l2, fh=17):
    """Deux champs cote-a-cote. Retourne y apres la ligne."""
    fw = (IW - 12) / 2
    label_field(n1, l1, ML,           y, fw, fh)
    label_field(n2, l2, ML + fw + 12, y, fw, fh)
    return y - RH


def fuel_gauge(y, pfx, title):
    """Jauge carburant avec 5 cases a cocher. Retourne y en dessous."""
    cv.saveState()
    cv.setFillColor(DARK)
    cv.setFont('Helvetica-Bold', 7.5)
    cv.drawString(ML, y, title)
    cv.restoreState()

    gw   = IW * 0.62
    bh   = 14
    yb   = y - 22
    lbls = ['0', '1/4', '1/2', '3/4', 'PLEIN']
    step = gw / 4.0

    # Barre de jauge
    cv.saveState()
    cv.setFillColor(CREAM)
    cv.setStrokeColor(BORDER)
    cv.setLineWidth(0.5)
    cv.roundRect(ML, yb, gw, bh, 3, fill=1, stroke=1)
    # Graduations internes
    cv.setStrokeColor(HexColor('#C5B99A'))
    cv.setLineWidth(0.4)
    for i in range(1, 4):
        xi = ML + i * step
        cv.line(xi, yb, xi, yb + bh)
    # Legende droite
    cv.setFillColor(MUTED)
    cv.setFont('Helvetica', 6.5)
    cv.drawString(ML + gw + 8, yb + bh / 2 - 3, 'Niveau')
    cv.drawString(ML + gw + 8, yb + bh / 2 - 12, 'carburant')
    cv.restoreState()

    # Labels + cases a cocher
    for i, lbl in enumerate(lbls):
        xi = ML + i * step
        cv.saveState()
        cv.setFillColor(MUTED)
        cv.setFont('Helvetica', 6.5)
        tw = cv.stringWidth(lbl, 'Helvetica', 6.5)
        cv.drawString(xi - tw / 2, yb - 9, lbl)
        cv.restoreState()
        form.checkbox(
            name=f'{pfx}_{i}',
            tooltip=f'Carburant {lbl}',
            checked=False,
            x=xi - 5,
            y=yb - 22,
            size=10,
            borderColor=GOLD,
            fillColor=FIELD,
            textColor=GOLD,
            borderWidth=0.75,
            buttonStyle='check',
            forceBorder=True,
        )

    return yb - 32


def page_footer(pg):
    cv.saveState()
    hline(MB + 14, color=GOLD, lw=0.6)
    cv.setFillColor(MUTED)
    cv.setFont('Helvetica', 6.2)
    cv.drawString(
        ML, MB + 4,
        'CARisme SAS  \xb7  1703 Route de 40 sous, 78630 Orgeval  '
        '\xb7  RCS Versailles 993\xa0656\xa0404  \xb7  TVA FR47993656404',
    )
    cv.drawRightString(W - MR, MB + 4, f'Page {pg} / 2')
    cv.restoreState()


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1
# ════════════════════════════════════════════════════════════════════════════
y = H - MT   # 811.89

# ── EN-TETE ──────────────────────────────────────────────────────────────────
cv.saveState()
cv.setFillColor(GOLD)
cv.setFont('Times-BoldItalic', 40)
brand_w = cv.stringWidth('CARisme', 'Times-BoldItalic', 40)
cv.drawString((W - brand_w) / 2, y - 44, 'CARisme')
cv.restoreState()
y -= 52

hline(y, color=GOLD, lw=0.9)
y -= 10

cv.saveState()
cv.setFillColor(DARK)
cv.setFont('Helvetica-Bold', 12)
titre = 'CONTRAT DE LOCATION DE V\xc9HICULE'
tw = cv.stringWidth(titre, 'Helvetica-Bold', 12)
cv.drawString((W - tw) / 2, y, titre)
y -= 15

cv.setFillColor(MUTED)
cv.setFont('Helvetica', 7.5)
for line in [
    'CARisme SAS  \xb7  1703 Route de 40 sous, 78630 Orgeval',
    'RCS Versailles 993 656 404  \xb7  TVA FR47993656404',
    'Assurance Allianz  \xb7  N\xb0 contrat : _____________________________',
]:
    lw2 = cv.stringWidth(line, 'Helvetica', 7.5)
    cv.drawString((W - lw2) / 2, y, line)
    y -= 11
cv.restoreState()

y -= 8
hline(y, color=GOLD, lw=0.4)
y -= 14

# ── SECTION 1 — LOCATAIRE ────────────────────────────────────────────────────
y = section_bar(y, 'SECTION 1  --  LOCATAIRE')
y -= 14

y = row2(y, 's1_nom',        'NOM',                        's1_prenom',      'PR\xc9NOM')
y = row2(y, 's1_ddn',        'DATE DE NAISSANCE',           's1_adresse',     'ADRESSE COMPL\xc8TE')
y = row2(y, 's1_email',      'EMAIL',                       's1_tel',         'T\xc9L\xc9PHONE')
y = row2(y, 's1_permis',     'N\xb0 PERMIS DE CONDUIRE',    's1_date_permis', "DATE D'OBTENTION DU PERMIS")
y -= 6

# ── SECTION 2 — VEHICULE ─────────────────────────────────────────────────────
y = section_bar(y, 'SECTION 2  --  V\xc9HICULE')
y -= 14

y = row2(y, 's2_modele', 'MARQUE / MOD\xc8LE',        's2_immat',  'IMMATRICULATION')
y = row2(y, 's2_km_dep', 'KILOM\xc9TRAGE D\xc9PART (km)', 's2_km_ret', 'KILOM\xc9TRAGE RETOUR (km)')
y -= 4

y = fuel_gauge(y, 'fuel_dep', 'NIVEAU CARBURANT  --  D\xc9PART')
y -= 8
y = fuel_gauge(y, 'fuel_ret', 'NIVEAU CARBURANT  --  RETOUR')
y -= 10

# ── SECTION 3 — CONDITIONS DE LOCATION ───────────────────────────────────────
y = section_bar(y, 'SECTION 3  --  CONDITIONS DE LOCATION')
y -= 14

y = row2(y, 's3_dep',     'DATE / HEURE DE D\xc9PART',        's3_ret',     'DATE / HEURE DE RETOUR')
y = row2(y, 's3_prix_j',  'PRIX JOURNALIER (€)',           's3_nb_j',    'NOMBRE DE JOURS')
y = row2(y, 's3_km_prev', 'KILOM\xc9TRAGE PR\xc9VU (km)',      's3_prix_km', 'PRIX KM SUPPL\xc9MENTAIRE (€/km)')
y = row2(y, 's3_total',   'MONTANT TOTAL (€)',              's3_caution', 'CAUTION (€)')

page_footer(1)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 2
# ════════════════════════════════════════════════════════════════════════════
cv.showPage()
y = H - MT

# Mini en-tete page 2
cv.saveState()
cv.setFillColor(GOLD)
cv.setFont('Times-BoldItalic', 20)
cv.drawString(ML, y - 20, 'CARisme')
cv.setFillColor(DARK)
cv.setFont('Helvetica-Bold', 8.5)
cv.drawString(ML + 80, y - 15, 'CONTRAT DE LOCATION  --  CONDITIONS G\xc9N\xc9RALES & SIGNATURES')
cv.restoreState()
y -= 32
hline(y, color=GOLD, lw=0.6)
y -= 14

# ── SECTION 4 — CONDITIONS GENERALES ─────────────────────────────────────────
y = section_bar(y, 'SECTION 4  --  CONDITIONS G\xc9N\xc9RALES')
y -= 12

cgv = [
    ('Permis de conduire',
     'Permis B obligatoire -- \xe2ge minimum 20 ans ou 2 ans de permis.'),
    ('V\xe9hicules +400 cv',
     '3 ans de permis de conduire minimum requis.'),
    ('V\xe9hicules +500 cv',
     '5 ans de permis de conduire minimum requis.'),
    ('Carburant',
     'Carburant manquant \xe0 la restitution factur\xe9 2,50 € / litre.'),
    ('Nettoyage',
     'Frais de nettoyage de 30 € si le v\xe9hicule est rendu sale.'),
    ('Retard',
     'Tout retard de restitution est factur\xe9 au prorata du prix journalier.'),
    ('Dommages',
     'Franchise selon devis garage, d\xe9duite de la caution vers\xe9e.'),
    ('Caution',
     'D\xe9bit\xe9e en cas de dommages ; facture compl\xe9mentaire si d\xe9passement.'),
    ('Traceur GPS',
     'Un traceur GPS est pr\xe9sent sur tous les v\xe9hicules (s\xe9curit\xe9 uniquement).'),
    ('Droit applicable',
     'Contrat soumis au droit fran\xe7ais. Litige : tribunal comp\xe9tent de Versailles.'),
]

for i, (cat, text) in enumerate(cgv):
    row_h = 15
    cv.saveState()
    cv.setFillColor(ALT if i % 2 == 0 else white)
    cv.rect(ML, y - row_h + 2, IW, row_h, fill=1, stroke=0)
    cv.setFillColor(GOLD)
    cv.setFont('Helvetica-Bold', 7.5)
    cv.drawString(ML + 5, y - row_h + 6, f'- {cat} :')
    cw = cv.stringWidth(f'- {cat} :  ', 'Helvetica-Bold', 7.5)
    cv.setFillColor(DARK)
    cv.setFont('Helvetica', 8)
    cv.drawString(ML + 5 + cw, y - row_h + 6, text)
    cv.restoreState()
    y -= row_h

y -= 12
hline(y, color=GOLD, lw=0.4)
y -= 14

# ── SECTION 5 — SIGNATURES ────────────────────────────────────────────────────
y = section_bar(y, 'SECTION 5  --  SIGNATURES')
y -= 16

# "Lu et approuve"
cv.saveState()
cv.setFillColor(DARK)
cv.setFont('Helvetica-Bold', 8.5)
cv.drawString(ML, y, 'Lu et approuv\xe9 par le locataire :')
cv.restoreState()
form.checkbox(
    name='lu_approuve',
    tooltip='Lu et approuve',
    checked=False,
    x=ML + 212, y=y - 2,
    size=12,
    borderColor=GOLD,
    fillColor=FIELD,
    textColor=GOLD,
    borderWidth=1,
    buttonStyle='check',
    forceBorder=True,
)
y -= 28

# Date + N contrat
label_field('sig_date',    'DATE DE SIGNATURE',   ML,                     y, IW * 0.34)
label_field('contrat_num', 'N\xb0 CONTRAT',        ML + IW * 0.34 + 12,   y, IW * 0.28)
y -= RH

# Boites de signature
sig_h = 90
sig_w = (IW - 16) / 2

cv.saveState()
cv.setFillColor(DARK)
cv.setFont('Helvetica-Bold', 7.5)
cv.drawString(ML, y, 'SIGNATURE DU LOUEUR (CARisme)')
cv.drawString(ML + sig_w + 16, y, 'SIGNATURE DU LOCATAIRE')
y -= 8
sig_y = y - sig_h

# Boite gauche (loueur)
cv.setFillColor(FIELD)
cv.setStrokeColor(BORDER)
cv.setLineWidth(0.5)
cv.rect(ML, sig_y, sig_w, sig_h, fill=1, stroke=1)
cv.setFillColor(MUTED)
cv.setFont('Helvetica', 7.5)
cv.drawString(ML + 6, sig_y + 14, 'Karim AZOUGUI')
cv.drawString(ML + 6, sig_y + 5,  'G\xe9rant CARisme SAS')

# Boite droite (locataire)
cv.setFillColor(FIELD)
cv.setStrokeColor(BORDER)
cv.setLineWidth(0.5)
cv.rect(ML + sig_w + 16, sig_y, sig_w, sig_h, fill=1, stroke=1)
cv.restoreState()

# Champ signature locataire (remplissable)
form.textfield(
    name='sig_locataire',
    tooltip='Signature du locataire',
    x=ML + sig_w + 18, y=sig_y + 2,
    width=sig_w - 4, height=sig_h - 4,
    fontSize=9,
    textColor=DARK,
    fillColor=FIELD,
    borderColor=None,
    borderWidth=0,
    fieldFlags='multiline doNotSpellCheck',
    forceBorder=False,
)

y = sig_y - 18

# Encart rappel caution
cv.saveState()
cv.setFillColor(HexColor('#FBF5EA'))
cv.setStrokeColor(GOLD)
cv.setLineWidth(0.7)
cv.roundRect(ML, y - 38, IW, 38, 4, fill=1, stroke=1)
cv.setFillColor(DARK)
cv.setFont('Helvetica-Bold', 7.5)
cv.drawString(ML + 10, y - 12, 'RAPPEL CAUTION :')
cv.setFillColor(MUTED)
cv.setFont('Helvetica', 7.5)
cv.drawString(
    ML + 115, y - 12,
    'La caution est encaiss\xe9e \xe0 la signature et restitu\xe9e sous 7 jours ouvr\xe9s apr\xe8s restitution,',
)
cv.drawString(
    ML + 10, y - 24,
    'sous r\xe9serve d\'absence de dommage ou kilom\xe9trage d\xe9pass\xe9. '
    'Tout d\xe9passement fait l\'objet d\'une facturation compl\xe9mentaire.',
)
cv.restoreState()

page_footer(2)

# ─── Sauvegarde ─────────────────────────────────────────────────────────────
cv.save()
print(f'PDF genere : {OUT}')
