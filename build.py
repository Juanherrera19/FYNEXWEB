#!/usr/bin/env python3
"""
Generador del sitio de FYNEX.

Lee el catálogo (contenido/catalogo.py), rellena las plantillas y escribe un sitio
estático en dist/. No hay servidor ni base de datos: el resultado son archivos HTML
que cualquier hosting estático sirve al instante, sin arranque en frío.

    python build.py            genera dist/
    python build.py --servir   genera y levanta un servidor local para revisarlo
"""

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

from contenido import catalogo  # noqa: E402

PLANTILLAS = RAIZ / "plantillas"
ESTATICOS = RAIZ / "estaticos"
SALIDA = RAIZ / "dist"


# ── Utilidades ──

def esc(texto) -> str:
    """Escapa texto para insertarlo en HTML o en un atributo."""
    return html.escape(str(texto or ""), quote=True)


def rellenar(plantilla: str, valores: dict) -> str:
    """
    Sustituye los marcadores {{CLAVE}} de una plantilla.

    Si al terminar queda algún marcador sin sustituir, aborta: es un error de
    plantilla y es mejor verlo al generar que descubrirlo en producción.
    """
    resultado = plantilla
    for clave, valor in valores.items():
        resultado = resultado.replace("{{%s}}" % clave, valor)

    sobrantes = set(re.findall(r"\{\{([A-Z_]+)\}\}", resultado))
    if sobrantes:
        raise SystemExit(
            "Marcadores sin valor en la plantilla: %s" % ", ".join(sorted(sobrantes))
        )
    return resultado


# ── Fragmentos ──

def botones(app: dict, clase_extra: str = "") -> str:
    """Botones para el hero y acciones principales de la página de producto."""
    partes = []

    if app.get("url_descargas"):
        partes.append(
            '<a href="%s" class="fx-btn fx-btn-primario%s">Descargar %s ⬇</a>'
            % (esc(app["url_descargas"]), clase_extra, esc(app["nombre"]))
        )
    elif app.get("url_propia"):
        clase_btn = "fx-btn-app" if app.get("destacada") else "fx-btn-primario"
        partes.append(
            '<a href="%s" target="_blank" rel="noopener noreferrer" class="fx-btn %s%s">Abrir %s ↗</a>'
            % (esc(app["url_propia"]), clase_btn, clase_extra, esc(app["nombre"]))
        )

    for tienda in app.get("tiendas", []):
        partes.append(
            '<a href="%s" class="fx-btn fx-btn-secundario%s" target="_blank" '
            'rel="noopener noreferrer">%s %s</a>'
            % (esc(tienda["url"]), clase_extra, esc(tienda.get("icono", "▶")),
               esc(tienda["nombre"]))
        )

    if not partes:
        partes.append('<span class="fx-insignia-pronto">En desarrollo</span>')

    return "".join(partes)


def botones_tarjeta(app: dict) -> str:
    """Botones para la tarjeta del catálogo en la portada."""
    partes = []
    if app.get("url_propia"):
        partes.append(
            '<a href="%s" target="_blank" rel="noopener noreferrer" class="fx-btn fx-btn-primario fx-btn-sm">Abrir %s ↗</a>'
            % (esc(app["url_propia"]), esc(app["nombre"]))
        )
    for tienda in app.get("tiendas", []):
        partes.append(
            '<a href="%s" class="fx-btn fx-btn-secundario fx-btn-sm" target="_blank" rel="noopener noreferrer">%s %s</a>'
            % (esc(tienda["url"]), esc(tienda.get("icono", "▶")), esc(tienda["nombre"]))
        )
    return "".join(partes)


def tarjeta(app: dict) -> str:
    """Una tarjeta del catálogo con spotlight y atributos de filtro."""
    pronto = app["estado"] != "publicada"
    clases = "fx-card fx-revelar" + (" fx-card-pronto" if pronto else "")
    tipo = esc(app.get("tipo", "app"))

    if app.get("icono"):
        icono = ('<img src="/%s" alt="%s" class="fx-card-icono" width="68" height="68" '
                 'loading="lazy">' % (esc(app["icono"]), esc(app["nombre"])))
    else:
        icono = '<div class="fx-card-icono fx-card-icono-vacio">✦</div>'

    if pronto:
        badge_status = '<span class="fx-card-badge-status fx-card-badge-pronto">Próximamente</span>'
        pie = '<span class="fx-insignia-pronto">Muy pronto</span>'
    elif app.get("url_descargas"):
        badge_status = '<span class="fx-card-badge-status">Disponible</span>'
        url_detalles = f"/apps/{esc(app['slug'])}/"
        url_desc = esc(app["url_descargas"])
        pie = f"""
            <div class="fx-card-pie-col">
                <div style="display:flex; gap:8px; width:100%;">
                    <a href="{url_detalles}" class="fx-btn fx-btn-secundario fx-btn-sm" style="flex:1;">Ver detalles</a>
                    <a href="{url_desc}" class="fx-btn fx-btn-primario fx-btn-sm" style="flex:1;">Descargar ⬇</a>
                </div>
                <div class="fx-tienda-pronto-pill">
                    <span>▶</span> <span>Google Play · Pronto disponible</span>
                </div>
            </div>"""
    else:
        badge_status = '<span class="fx-card-badge-status">Disponible</span>'
        pie = ('<a href="/apps/%s/" class="fx-btn fx-btn-secundario fx-btn-sm">Ver detalles</a>'
               % esc(app["slug"])) + botones_tarjeta(app)

    chips_plataforma = "".join(
        '<span class="fx-plataforma" style="font-size:0.75rem; padding:3px 8px;">%s</span>' % esc(p)
        for p in app.get("plataformas", [])
    )

    return """
        <article class="%s" data-tipo="%s" style="--app-color: %s;">
            <div class="fx-card-top">
                %s
                <div class="fx-card-badges-row">
                    <span class="fx-card-cat">%s</span>
                    %s
                </div>
            </div>
            <h3>%s</h3>
            <p class="fx-card-desc">%s</p>
            <div class="fx-plataformas" style="margin-bottom:18px;">%s</div>
            <div class="fx-card-pie">%s</div>
        </article>""" % (
        clases, tipo, esc(app["color"]),
        icono, esc(app["categoria"]), badge_status,
        esc(app["nombre"]), esc(app["descripcion_corta"]),
        chips_plataforma, pie,
    )


def seccion_destacada(app) -> str:
    if not app:
        return ""

    visual = ""
    if app.get("icono"):
        visual = """
        <div class="fx-destacada-visual">
            <div class="fx-destacada-mockup-wrap">
                <div class="fx-flotante-badge pos-arriba">
                    <span>✨</span> <span>Fynex IA Activa</span>
                </div>
                <img src="/%s" alt="%s" class="fx-app-preview" width="250" height="250">
                <div class="fx-flotante-badge pos-abajo">
                    <span>📊</span> <span>Avalancha & Nieve</span>
                </div>
            </div>
        </div>""" % (esc(app["icono"]), esc(app["nombre"]))

    version = esc(app.get("version", "1.2.18"))

    return """
<section class="fx-seccion">
    <div class="fx-contenedor">
        <div class="fx-destacada fx-revelar" style="--app-color: %s;">
            <div class="fx-destacada-txt">
                <div class="fx-destacada-badges">
                    <span class="fx-destacada-cat">✦ Proyecto Destacado · %s</span>
                    <span class="fx-destacada-pill">v%s</span>
                    <span class="fx-destacada-pill">100%% Gratis</span>
                </div>
                <h3>%s</h3>
                <p class="fx-tagline">%s</p>
                <p class="fx-desc">%s</p>

                <div class="fx-destacada-puntos">
                    <div class="fx-destacada-punto">
                        <span class="ico">🛡️</span> <span>Sin anuncios ni paywalls</span>
                    </div>
                    <div class="fx-destacada-punto">
                        <span class="ico">✨</span> <span>Asesor Fynex IA diario</span>
                    </div>
                    <div class="fx-destacada-punto">
                        <span class="ico">🧮</span> <span>Simulador de amortización</span>
                    </div>
                    <div class="fx-destacada-punto">
                        <span class="ico">📱</span> <span>Widgets nativos Android</span>
                    </div>
                </div>

                <div class="fx-acciones" style="justify-content:flex-start;">
                    <a href="/apps/%s/" class="fx-btn fx-btn-primario">Explorar Debts Goodbye</a>
                    %s
                </div>
            </div>
            %s
        </div>
    </div>
</section>""" % (
        esc(app["color"]), esc(app["categoria"]), version, esc(app["nombre"]),
        esc(app["tagline"]), esc(app["descripcion_corta"]), esc(app["slug"]),
        botones(app), visual,
    )


def apps_del_pie() -> str:
    filas = [
        '<li><a href="/apps/%s/">%s</a></li>' % (esc(a["slug"]), esc(a["nombre"]))
        for a in catalogo.publicadas()
    ]
    if not filas:
        filas.append('<li><span style="color:#6b7688;">Próximamente</span></li>')
    return "".join(filas)


# ── Páginas ──

def generar_portada() -> str:
    plantilla = (PLANTILLAS / "home.html").read_text(encoding="utf-8")
    return rellenar(plantilla, {
        "DESTACADA": seccion_destacada(catalogo.destacada()),
        "TARJETAS": "".join(tarjeta(a) for a in catalogo.todas()),
        "FOOTER_APPS": apps_del_pie(),
        "ESTUDIO_DESC": esc(catalogo.ESTUDIO["descripcion"]),
        "ESTUDIO_EMAIL": esc(catalogo.ESTUDIO["email"]),
    })


def generar_detalle(app: dict) -> str:
    plantilla = (PLANTILLAS / "app.html").read_text(encoding="utf-8")

    # Icono principal en alta resolución
    if app.get("icono"):
        icono = ('<img src="/%s" alt="%s" class="fx-app-icono" width="136" height="136">'
                 % (esc(app["icono"]), esc(app["nombre"])))
    else:
        icono = '<div class="fx-app-icono fx-card-icono-vacio">✦</div>'

    # Franja de métricas
    metricas = ""
    if app.get("metas"):
        items = "".join("""
            <div class="fx-metrica-card">
                <div class="fx-metrica-icono">%s</div>
                <div>
                    <div class="fx-metrica-valor">%s</div>
                    <div class="fx-metrica-etiqueta">%s</div>
                </div>
            </div>""" % (esc(m["icono"]), esc(m["valor"]), esc(m["etiqueta"]))
            for m in app["metas"])
        metricas = '<div class="fx-metricas-grid fx-revelar">%s</div>' % items

    # Showcase interactivo (Galería de pantallas con mockup adaptable móvil / desktop)
    showcase = ""
    if app.get("showcase"):
        primero = app["showcase"][0]
        tabs = "".join("""
            <button type="button" class="fx-showcase-tab%s" data-id="%s" data-img="/%s" data-titulo="%s" data-badge="%s" data-desc="%s">
                <div class="fx-showcase-tab-header">
                    <span class="fx-showcase-tab-titulo">%s</span>
                    <span class="fx-showcase-tab-badge">%s</span>
                </div>
                <p class="fx-showcase-tab-desc">%s</p>
            </button>""" % (
            " activa" if i == 0 else "",
            esc(s["id"]), esc(s["captura"]), esc(s["titulo"]), esc(s["badge"]), esc(s["desc"]),
            esc(s["titulo"]), esc(s["badge"]), esc(s["desc"])
        ) for i, s in enumerate(app["showcase"]))

        chips_movil = "".join("""
            <button type="button" class="fx-showcase-chip%s" data-id="%s" data-img="/%s" data-titulo="%s" data-badge="%s" data-desc="%s">
                <span>%s</span> <span>%s</span>
            </button>""" % (
            " activa" if i == 0 else "",
            esc(s["id"]), esc(s["captura"]), esc(s["titulo"]), esc(s["badge"]), esc(s["desc"]),
            esc(s.get("icono_corto", "✦")), esc(s.get("nombre_corto", s["titulo"]))
        ) for i, s in enumerate(app["showcase"]))

        tipo_disp = app.get("tipo_dispositivo", "movil")
        if tipo_disp == "desktop":
            marco_mockup = """
                <div class="fx-desktop-frame">
                    <div class="fx-desktop-titlebar">
                        <div class="fx-desktop-dots">
                            <span class="fx-desktop-dot red"></span>
                            <span class="fx-desktop-dot yellow"></span>
                            <span class="fx-desktop-dot green"></span>
                        </div>
                        <span class="fx-desktop-title">%s v%s — developed by fynexhq</span>
                        <div class="fx-desktop-controls">
                            <span>─</span>
                            <span>▢</span>
                            <span>✕</span>
                        </div>
                    </div>
                    <div class="fx-desktop-pantalla">
                        <img src="/%s" alt="%s" class="fx-desktop-img" id="mockupPantalla">
                    </div>
                </div>""" % (esc(app["nombre"]), esc(app.get("version", "1.0.0")), esc(primero["captura"]), esc(primero["titulo"]))
        else:
            marco_mockup = """
                <div class="fx-celular-frame">
                    <div class="fx-celular-speaker"></div>
                    <div class="fx-celular-pantalla">
                        <img src="/%s" alt="%s" class="fx-celular-img" id="mockupPantalla">
                    </div>
                </div>""" % (esc(primero["captura"]), esc(primero["titulo"]))

        showcase = """
<section class="fx-seccion fx-seccion-alt" id="showcase">
    <div class="fx-contenedor">
        <div class="fx-seccion-cab centrado fx-revelar">
            <h2>Explora cada módulo de la aplicación</h2>
            <p>Capturas reales de la experiencia en ejecución. Selecciona cada herramienta para verla en acción.</p>
        </div>

        <!-- Selector horizontal deslizable para pantallas móviles -->
        <div class="fx-showcase-nav-mobile fx-revelar">
            %s
        </div>

        <div class="fx-showcase fx-revelar">
            <div class="fx-showcase-tabs">
                %s
            </div>
            <div class="fx-showcase-display">
                %s

                <div class="fx-showcase-info-active" id="infoShowcaseActiva">
                    <span class="fx-showcase-tab-badge" id="infoShowcaseBadge">%s</span>
                    <h4 id="infoShowcaseTitulo">%s</h4>
                    <p id="infoShowcaseDesc">%s</p>
                </div>

                <button type="button" class="fx-btn-inspeccionar" id="btnInspeccionar" data-img="/%s" data-titulo="%s">
                    🔍 Ampliar captura a pantalla completa
                </button>
            </div>
        </div>
    </div>
</section>""" % (
            chips_movil,
            tabs,
            marco_mockup,
            esc(primero["badge"]), esc(primero["titulo"]), esc(primero["desc"]),
            esc(primero["captura"]), esc(primero["titulo"]),
        )

    # Descripción larga
    descripcion = ""
    if app.get("descripcion_larga"):
        tit_desc = app.get("titulo_descripcion") or (
            "Control financiero con rigor matemático" if app["slug"] == "debts-goodbye"
            else "Ingeniería de audio de alto rendimiento"
        )
        descripcion = """
<section class="fx-seccion">
    <div class="fx-contenedor">
        <div class="fx-seccion-cab fx-revelar" style="max-width:820px; margin-left:auto; margin-right:auto; text-align:center;">
            <h2>%s</h2>
            <p style="font-size:1.1rem; line-height:1.7;">%s</p>
        </div>
    </div>
</section>""" % (esc(tit_desc), esc(app["descripcion_larga"]))

    # Novedades recientes del README
    novedades = ""
    if app.get("novedades"):
        cards = "".join("""
            <article class="fx-novedad-card fx-revelar">
                <div class="fx-novedad-top">
                    <span class="fx-novedad-icono">%s</span>
                    <h4>%s</h4>
                </div>
                <p>%s</p>
            </article>""" % (esc(n["icono"]), esc(n["titulo"]), esc(n["desc"]))
            for n in app["novedades"])
        tit_nov = app.get("titulo_novedades") or "Innovaciones y actualizaciones recientes"
        sub_nov = app.get("subtitulo_novedades") or "Evolución continua basada en ingeniería de precisión, compatibilidad moderna y rendimiento."
        novedades = """
<section class="fx-seccion fx-seccion-alt">
    <div class="fx-contenedor">
        <div class="fx-seccion-cab centrado fx-revelar">
            <h2>%s</h2>
            <p>%s</p>
        </div>
        <div class="fx-novedades-grid">%s</div>
    </div>
</section>""" % (esc(tit_nov), esc(sub_nov), cards)

    # Características
    caracteristicas = ""
    if app.get("caracteristicas"):
        tarjetas = "".join("""
            <article class="fx-caracteristica fx-revelar">
                <span class="emoji">%s</span>
                <h4>%s</h4>
                <p>%s</p>
            </article>""" % (esc(c["emoji"]), esc(c["titulo"]), esc(c["texto"]))
            for c in app["caracteristicas"])
        tit_car = app.get("titulo_caracteristicas") or ("Todo lo que puedes lograr con %s" % esc(app["nombre"]))
        sub_car = app.get("subtitulo_caracteristicas") or "Un conjunto integral de herramientas diseñado para durar con los más altos estándares."
        caracteristicas = """
<section class="fx-seccion">
    <div class="fx-contenedor">
        <div class="fx-seccion-cab centrado fx-revelar">
            <h2>%s</h2>
            <p>%s</p>
        </div>
        <div class="fx-caracteristicas">%s</div>
    </div>
</section>""" % (esc(tit_car), esc(sub_car), tarjetas)

    # Arquitectura e ingeniería
    arquitectura = ""
    if app.get("arquitectura"):
        cards_arq = "".join("""
            <div class="fx-arquitectura-card">
                <h5>%s</h5>
                <p>%s</p>
            </div>""" % (esc(a["titulo"]), esc(a["desc"]))
            for a in app["arquitectura"])
        tit_arq = app.get("titulo_arquitectura") or "Arquitectura e integridad técnica"
        sub_arq = app.get("subtitulo_arquitectura") or "Diseñada con estándares rigurosos de estabilidad, velocidad y rendimiento para durar en el tiempo."
        arquitectura = """
<section class="fx-seccion fx-seccion-alt">
    <div class="fx-contenedor">
        <div class="fx-seccion-cab centrado fx-revelar">
            <h2>%s</h2>
            <p>%s</p>
        </div>
        <div class="fx-arquitectura-grid fx-revelar">%s</div>
    </div>
</section>""" % (esc(tit_arq), esc(sub_arq), cards_arq)

    # Banner CTA final
    titulo_cta = app.get("cta_titulo") or "Comienza hoy tu camino hacia una mejor experiencia"
    desc_cta = app.get("cta_desc") or "Descarga la aplicación o accede directamente desde tu dispositivo."

    partes_cta = []
    if app.get("url_descargas"):
        partes_cta.append(
            '<a href="%s" class="fx-btn fx-btn-primario">Ir a Descargas de %s ⬇</a>'
            % (esc(app["url_descargas"]), esc(app["nombre"]))
        )
    elif app.get("url_propia"):
        partes_cta.append(
            '<a href="%s" target="_blank" rel="noopener noreferrer" class="fx-btn fx-btn-primario">Abrir %s en la Web ↗</a>'
            % (esc(app["url_propia"]), esc(app["nombre"]))
        )
    for t in app.get("tiendas", []):
        partes_cta.append(
            '<a href="%s" target="_blank" rel="noopener noreferrer" class="fx-btn fx-btn-secundario">%s %s</a>'
            % (esc(t["url"]), esc(t.get("icono", "▶")), esc(t["nombre"]))
        )

    aviso_cta = ""
    if app.get("aviso_plataforma"):
        aviso_cta = '<div class="fx-cta-aviso"><span class="ico">🤖</span> <span>%s</span></div>' % esc(app["aviso_plataforma"])

    cta_banner = """
<section class="fx-seccion">
    <div class="fx-contenedor">
        <div class="fx-cta-banner fx-revelar">
            <h2>%s</h2>
            <p>%s</p>
            <div class="fx-acciones">%s</div>
            %s
        </div>
    </div>
</section>""" % (esc(titulo_cta), esc(desc_cta), "".join(partes_cta), aviso_cta)

    # Botón de navegación superior (NAV_CTA)
    if app.get("url_descargas"):
        nav_cta = ('<a href="%s" class="fx-nav-cta">Descargar %s ⬇</a>'
                   % (esc(app["url_descargas"]), esc(app["nombre"])))
    elif app.get("url_propia"):
        nav_cta = ('<a href="%s" target="_blank" rel="noopener noreferrer" class="fx-nav-cta">Abrir %s ↗</a>'
                   % (esc(app["url_propia"]), esc(app["nombre"])))
    else:
        nav_cta = ""

    # Política de privacidad
    if app.get("url_privacidad"):
        privacidad = ('<a href="%s" target="_blank" rel="noopener noreferrer">'
                      'Política de privacidad</a>' % esc(app["url_privacidad"]))
    else:
        privacidad = ""

    return rellenar(plantilla, {
        "NOMBRE": esc(app["nombre"]),
        "DESC_CORTA": esc(app["descripcion_corta"]),
        "COLOR": esc(app["color"]),
        "CATEGORIA": esc(app["categoria"]),
        "TAGLINE": esc(app["tagline"]),
        "VERSION": esc(app.get("version", "1.0.0")),
        "ICONO": icono,
        "ICONO_URL": esc(app.get("icono", "img/apps/debts-goodbye.png")),
        "NAV_CTA": nav_cta,
        "PLATAFORMAS": "".join('<span class="fx-plataforma">%s</span>' % esc(p)
                               for p in app.get("plataformas", [])),
        "BOTONES": botones(app),
        "METRICAS": metricas,
        "SHOWCASE_GALERIA": showcase,
        "DESCRIPCION": descripcion,
        "NOVEDADES": novedades,
        "CARACTERISTICAS": caracteristicas,
        "ARQUITECTURA": arquitectura,
        "CTA_BANNER": cta_banner,
        "FOOTER_APPS": apps_del_pie(),
        "ESTUDIO_DESC": esc(catalogo.ESTUDIO["descripcion"]),
        "PRIVACIDAD": privacidad,
    })


def generar_descargas(app: dict) -> str:
    plantilla = (PLANTILLAS / "descargas.html").read_text(encoding="utf-8")

    if app.get("icono"):
        icono = ('<img src="/%s" alt="%s" class="fx-app-icono" width="136" height="136">'
                 % (esc(app["icono"]), esc(app["nombre"])))
    else:
        icono = '<div class="fx-app-icono fx-card-icono-vacio">✦</div>'

    tarjetas = []
    for d in app.get("descargas", []):
        es_destacada = " destacada" if d.get("destacado") else ""
        badge_tipo = d.get("badge_tipo", "rec")
        
        puntos_html = "".join(
            '<div class="fx-descarga-punto"><span class="ico">✓</span><span>%s</span></div>' % esc(pt)
            for pt in d.get("puntos", [])
        )
        
        if d.get("pronto"):
            btn_html = '<div class="fx-descarga-btn-pronto"><span>▶</span> <span>Google Play · Pronto disponible</span></div>'
        else:
            clase_btn = "fx-btn-primario" if d.get("primario") else "fx-btn-secundario"
            btn_html = (
                '<a href="%s" target="_blank" rel="noopener noreferrer" class="fx-btn %s">%s %s</a>'
                % (esc(d["url"]), clase_btn, esc(d.get("icono", "💾")), esc(d["nombre"]))
            )

        tarjetas.append("""
            <article class="fx-descarga-card%s">
                <span class="fx-descarga-badge %s">%s</span>
                <div class="fx-descarga-card-icono">%s</div>
                <h3>%s</h3>
                <div class="fx-descarga-sub"><span>💻</span> <span>%s</span></div>
                <p class="fx-descarga-desc">%s</p>
                <div class="fx-descarga-puntos">%s</div>
                %s
            </article>""" % (
            es_destacada, badge_tipo, esc(d.get("badge", "Disponible")),
            esc(d.get("icono", "💾")), esc(d["nombre"]), esc(d.get("sub", "")),
            esc(d.get("desc", "")), puntos_html, btn_html
        ))

    return rellenar(plantilla, {
        "NOMBRE": esc(app["nombre"]),
        "SLUG": esc(app["slug"]),
        "VERSION": esc(app.get("version", "1.0.0")),
        "COLOR": esc(app["color"]),
        "CATEGORIA": esc(app["categoria"]),
        "ICONO": icono,
        "ICONO_URL": esc(app.get("icono", "img/apps/audiout/audiout-logo.png")),
        "TARJETAS_DESCARGA": "".join(tarjetas),
        "FOOTER_APPS": apps_del_pie(),
        "ESTUDIO_DESC": esc(catalogo.ESTUDIO["descripcion"]),
    })


def generar_404() -> str:
    """Página de error, con el mismo marco que el resto del sitio."""
    plantilla = (PLANTILLAS / "home.html").read_text(encoding="utf-8")
    html_404 = rellenar(plantilla, {
        "DESTACADA": """
<section class="fx-seccion">
    <div class="fx-contenedor">
        <div class="fx-seccion-cab centrado">
            <h2>Esta página no existe</h2>
            <p>El enlace que seguiste no lleva a ninguna parte. Abajo está el catálogo completo.</p>
        </div>
    </div>
</section>""",
        "TARJETAS": "".join(tarjeta(a) for a in catalogo.todas()),
        "FOOTER_APPS": apps_del_pie(),
        "ESTUDIO_DESC": esc(catalogo.ESTUDIO["descripcion"]),
        "ESTUDIO_EMAIL": esc(catalogo.ESTUDIO["email"]),
    })
    return html_404.replace(
        "<title>FYNEX — Estudio de apps y juegos</title>",
        "<title>Página no encontrada — FYNEX</title>", 1)


# ── Generación ──

def construir() -> int:
    if SALIDA.exists():
        shutil.rmtree(SALIDA)
    SALIDA.mkdir(parents=True)

    # Estáticos tal cual
    shutil.copytree(ESTATICOS, SALIDA, dirs_exist_ok=True)

    paginas = 0

    (SALIDA / "index.html").write_text(generar_portada(), encoding="utf-8")
    paginas += 1

    for app in catalogo.todas():
        if app["estado"] != "publicada":
            continue
        carpeta = SALIDA / "apps" / app["slug"]
        carpeta.mkdir(parents=True, exist_ok=True)
        (carpeta / "index.html").write_text(generar_detalle(app), encoding="utf-8")
        paginas += 1

        if app.get("url_descargas"):
            carpeta_desc = carpeta / "descargas"
            carpeta_desc.mkdir(parents=True, exist_ok=True)
            (carpeta_desc / "index.html").write_text(generar_descargas(app), encoding="utf-8")
            paginas += 1

    (SALIDA / "404.html").write_text(generar_404(), encoding="utf-8")
    paginas += 1

    # robots.txt y sitemap, para que el sitio se indexe bien
    base = catalogo.ESTUDIO["url"].rstrip("/")
    (SALIDA / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % base, encoding="utf-8")

    urls = ["%s/" % base]
    for a in catalogo.publicadas():
        urls.append("%s/apps/%s/" % (base, a["slug"]))
        if a.get("url_descargas"):
            urls.append("%s/apps/%s/descargas/" % (base, a["slug"]))

    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "".join("  <url><loc>%s</loc></url>\n" % u for u in urls)
               + "</urlset>\n")
    (SALIDA / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    return paginas


def servir(puerto: int = 8080) -> None:
    import http.server
    import socketserver
    import functools

    manejador = functools.partial(http.server.SimpleHTTPRequestHandler,
                                  directory=str(SALIDA))
    with socketserver.TCPServer(("127.0.0.1", puerto), manejador) as httpd:
        print("Sirviendo dist/ en http://127.0.0.1:%d  (Ctrl+C para salir)" % puerto)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nDetenido.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera el sitio de FYNEX")
    parser.add_argument("--servir", action="store_true",
                        help="genera y levanta un servidor local")
    parser.add_argument("--puerto", type=int, default=8080)
    args = parser.parse_args()

    paginas = construir()
    print("Generadas %d páginas en %s" % (paginas, SALIDA))

    if args.servir:
        servir(args.puerto)


if __name__ == "__main__":
    main()
