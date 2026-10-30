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
        if tienda.get("pronto") or not tienda.get("url"):
            continue
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
    """Botones para la tarjeta del catálogo en la portada (uno debajo de otro)."""
    partes = []
    if app.get("url_propia"):
        partes.append(
            '<a href="%s" target="_blank" rel="noopener noreferrer" class="fx-btn fx-btn-primario fx-btn-sm fx-btn-bloque">Abrir %s ↗</a>'
            % (esc(app["url_propia"]), esc(app["nombre"]))
        )
    elif app.get("url_descargas"):
        partes.append(
            '<a href="%s" class="fx-btn fx-btn-primario fx-btn-sm fx-btn-bloque">Descargar ⬇</a>'
            % esc(app["url_descargas"])
        )
    for tienda in app.get("tiendas", []):
        if tienda.get("pronto") or not tienda.get("url"):
            partes.append(
                '<div class="fx-btn fx-btn-gris fx-btn-sm fx-btn-bloque" title="Próximamente disponible en Google Play">'
                '<span>%s</span> <span>%s · Pronto disponible</span>'
                '</div>' % (esc(tienda.get("icono", "▶")), esc(tienda["nombre"]))
            )
        else:
            partes.append(
                '<a href="%s" class="fx-btn fx-btn-secundario fx-btn-sm fx-btn-bloque" target="_blank" rel="noopener noreferrer">%s %s</a>'
                % (esc(tienda["url"]), esc(tienda.get("icono", "▶")), esc(tienda["nombre"]))
            )
    return "".join(partes)


def tarjeta(app: dict) -> str:
    """Una tarjeta del catálogo con diseño split de 2 columnas inspirado en maqueta visual."""
    pronto = app["estado"] != "publicada"
    slug = esc(app["slug"])
    nombre = esc(app["nombre"])
    color = esc(app["color"])
    categoria = esc(app.get("categoria", "App"))
    tipo = esc(app.get("tipo", "app"))
    clases = "fx-card fx-card-%s fx-revelar%s" % (slug, " fx-card-pronto" if pronto else "")

    # 1. Columna Izquierda: Mockup de Dispositivo Inclinado con Marco y Enfoque Seguro
    if slug == "debts-goodbye":
        mockup_html = """
            <div class="fx-card-mockup-col fx-mockup-col-debts">
                <div class="fx-card-mockup-glow" aria-hidden="true"></div>
                <div class="fx-card-decor-ray" aria-hidden="true"></div>
                <div class="fx-device-phone fx-tilt-phone">
                    <div class="fx-phone-speaker" aria-hidden="true"></div>
                    <div class="fx-phone-camera" aria-hidden="true"></div>
                    <div class="fx-phone-screen-frame">
                        <img src="/img/apps/debts-goodbye/capturas/02_dashboard_resumen_real.png" 
                             alt="Debts Goodbye Dashboard Financiero" 
                             class="fx-device-screen-img" 
                             width="148" 
                             height="260" 
                             loading="lazy">
                    </div>
                </div>
            </div>"""
    elif slug == "audiout":
        mockup_html = """
            <div class="fx-card-mockup-col fx-mockup-col-audiout">
                <div class="fx-card-mockup-glow" aria-hidden="true"></div>
                <div class="fx-card-decor-ray" aria-hidden="true"></div>
                <div class="fx-device-desktop fx-tilt-window">
                    <div class="fx-desktop-bar" aria-hidden="true">
                        <span class="fx-desktop-dot rojo"></span>
                        <span class="fx-desktop-dot amarillo"></span>
                        <span class="fx-desktop-dot verde"></span>
                        <span class="fx-desktop-title-tiny">Audiout Studio</span>
                    </div>
                    <div class="fx-desktop-screen-frame">
                        <img src="/img/apps/audiout/capturas_reales/01_multi_salida_real.png" 
                             alt="Audiout Panel Multi-Salida" 
                             class="fx-device-screen-img" 
                             width="190" 
                             height="165" 
                             loading="lazy">
                    </div>
                </div>
            </div>"""
    else:
        icono_holo = "🎮" if tipo == "juego" else "✦"
        tag_holo = "JUEGO EN DESARROLLO" if tipo == "juego" else "APP EN DESARROLLO"
        mockup_html = """
            <div class="fx-card-mockup-col">
                <div class="fx-card-mockup-glow" aria-hidden="true"></div>
                <div class="fx-device-holo">
                    <div class="fx-holo-pulse" aria-hidden="true">%s</div>
                    <span class="fx-holo-tag">%s</span>
                    <span class="fx-holo-lab">FYNEX LABS</span>
                </div>
            </div>""" % (icono_holo, tag_holo)

    # 2. Columna Derecha: Icono, Título, Tagline, Chips de Plataforma y Botones
    if app.get("icono"):
        icono_html = ('<img src="/%s" alt="%s" class="fx-card-ico-img" width="48" height="48" loading="lazy">' 
                      % (esc(app["icono"]), nombre))
    else:
        icono_html = '<div class="fx-card-ico-img fx-card-ico-placeholder">✦</div>'

    if pronto:
        status_html = '<span class="fx-card-status-pill pronto"><span class="fx-card-status-dot"></span>Próximamente</span>'
        btn_primario = '<span class="fx-btn-vermas fx-btn-vermas-disabled"><span>En desarrollo</span></span>'
        btn_accion = ""
    else:
        status_html = '<span class="fx-card-status-pill"><span class="fx-card-status-dot"></span>Disponible</span>'
        btn_primario = ('<a href="/apps/%s/" class="fx-btn-vermas"><span>Ver más</span> <span class="fx-flecha">→</span></a>' 
                        % slug)
        
        if app.get("url_propia"):
            btn_accion = ('<a href="%s" target="_blank" rel="noopener noreferrer" class="fx-btn-accion-rapida" title="Abrir Web App"><span>Abrir app ↗</span></a>' 
                          % esc(app["url_propia"]))
        elif app.get("url_descargas"):
            btn_accion = ('<a href="%s" class="fx-btn-accion-rapida" title="Descargas oficiales"><span>Descargar ⬇</span></a>' 
                          % esc(app["url_descargas"]))
        else:
            btn_accion = ""

    # Chips de plataformas con iconos
    chips = []
    for p in app.get("plataformas", []):
        p_str = esc(p)
        p_low = p.lower()
        if "android" in p_low:
            ico = "🤖"
        elif "windows" in p_low:
            ico = "💻"
        elif "web" in p_low or "pwa" in p_low:
            ico = "🌐"
        elif "multi" in p_low:
            ico = "⚡"
        else:
            ico = "✦"
        chips.append('<span class="fx-plat-pill"><span class="fx-plat-ico">%s</span>%s</span>' % (ico, p_str))
    chips_html = "".join(chips)

    if slug == "debts-goodbye":
        tagline_txt = "Toma el control de tus finanzas. Planifica, ahorra y alcanza tus metas."
    elif slug == "audiout":
        tagline_txt = "Tu audio, donde lo necesitas. Conecta, distribuye y disfruta."
    else:
        tagline_txt = esc(app.get("tagline") or app.get("descripcion_corta", ""))

    return """
        <article class="%s" data-tipo="%s" data-slug="%s" style="--app-color: %s;">
            %s
            <div class="fx-card-info-col">
                <div class="fx-card-head-row">
                    <div class="fx-card-ico-wrap">%s</div>
                    <div class="fx-card-head-meta">
                        <span class="fx-card-cat-tag">%s</span>
                        %s
                    </div>
                </div>
                <h3 class="fx-card-title">%s</h3>
                <p class="fx-card-tagline">%s</p>
                <div class="fx-card-plataformas">%s</div>
                <div class="fx-card-btns-row">
                    %s
                    %s
                </div>
            </div>
        </article>""" % (
        clases, tipo, slug, color,
        mockup_html,
        icono_html, categoria, status_html,
        nombre, tagline_txt, chips_html,
        btn_primario, btn_accion
    )


def seccion_destacada(app) -> str:
    """Sección de proyecto destacado (eliminada a petición)."""
    return ""


def botones_hero(app: dict) -> str:
    """Botones para el hero principal de la página de producto."""
    slug = app.get("slug")
    if slug == "debts-goodbye":
        return """
            <a href="https://dgb.fynexhq.com" target="_blank" rel="noopener noreferrer" class="fx-btn fx-btn-primario">
                <span>Abrir Web App</span> <span class="fx-flecha">↗</span>
            </a>
            <a href="https://play.google.com/store/apps/details?id=com.debtsgoodbye.free" target="_blank" rel="noopener noreferrer" class="fx-btn fx-btn-secundario">
                <span>▶ Google Play</span>
            </a>
            <a href="#showcase" class="fx-btn fx-btn-terciario">
                <span>Explorar módulos</span> <span class="fx-flecha">↓</span>
            </a>"""
    elif slug == "audiout":
        return """
            <a href="/apps/audiout/descargas/" class="fx-btn fx-btn-primario">
                <span>Descargar v1.0.0 (.exe)</span> <span class="fx-flecha">⬇</span>
            </a>
            <a href="/apps/audiout/descargas/#portable" class="fx-btn fx-btn-secundario">
                <span>⚡ Versión Portable</span>
            </a>
            <a href="#showcase" class="fx-btn fx-btn-terciario">
                <span>Ver capturas en vivo</span> <span class="fx-flecha">↓</span>
            </a>"""
    else:
        return botones(app)


def generar_hero_visual(app: dict) -> str:
    """Mockup destacado de producto con chips de métricas en vivo."""
    slug = app.get("slug")
    if slug == "debts-goodbye":
        return """
            <div class="fx-hero-mockup-stage stage-phone">
                <div class="fx-hero-glow-back" style="background: radial-gradient(circle, rgba(30,120,129,0.38) 0%, transparent 68%);"></div>
                <div class="fx-floating-chip chip-arriba-der">
                    <span class="chip-ico">📉</span>
                    <div class="chip-info">
                        <span class="chip-tit">Ahorro proyectado</span>
                        <span class="chip-val">-42% en intereses</span>
                    </div>
                </div>
                <div class="fx-celular-frame fx-celular-hero">
                    <div class="fx-celular-speaker"></div>
                    <div class="fx-celular-pantalla">
                        <img src="/img/apps/debts-goodbye/capturas/02_dashboard_resumen_real.png" 
                             alt="Debts Goodbye Dashboard Financiero" 
                             class="fx-celular-img" 
                             width="275" 
                             height="435" 
                             loading="eager">
                    </div>
                </div>
                <div class="fx-floating-chip chip-abajo-izq">
                    <span class="chip-ico">🤖</span>
                    <div class="chip-info">
                        <span class="chip-tit">Asesor Fynex IA</span>
                        <span class="chip-val">Diagnóstico DTI Activo</span>
                    </div>
                </div>
            </div>"""
    elif slug == "audiout":
        return """
            <div class="fx-hero-mockup-stage stage-desktop">
                <div class="fx-hero-glow-back" style="background: radial-gradient(circle, rgba(2,132,199,0.36) 0%, transparent 68%);"></div>
                <div class="fx-floating-chip chip-arriba-der">
                    <span class="chip-ico">🔊</span>
                    <div class="chip-info">
                        <span class="chip-tit">Sincronización Acústica</span>
                        <span class="chip-val">0 ms Desfase Acumulado</span>
                    </div>
                </div>
                <div class="fx-desktop-frame fx-desktop-hero">
                    <div class="fx-desktop-bar">
                        <span class="fx-desktop-dot rojo"></span>
                        <span class="fx-desktop-dot amarillo"></span>
                        <span class="fx-desktop-dot verde"></span>
                        <span class="fx-desktop-title-tiny">Audiout v1.0.0 — Panel Multi-Salida</span>
                    </div>
                    <div class="fx-desktop-pantalla">
                        <img src="/img/apps/audiout/capturas_reales/01_multi_salida_real.png" 
                             alt="Audiout Panel Multi-Salida" 
                             class="fx-desktop-img" 
                             width="460" 
                             height="420" 
                             loading="eager">
                    </div>
                </div>
                <div class="fx-floating-chip chip-abajo-izq">
                    <span class="chip-ico">🎛️</span>
                    <div class="chip-info">
                        <span class="chip-tit">Motor DSP WASAPI</span>
                        <span class="chip-val">32-bit Float · 48 kHz</span>
                    </div>
                </div>
            </div>"""
    else:
        icono_src = app.get("icono")
        if icono_src:
            return '<div class="fx-app-icono-wrap"><img src="/%s" alt="%s" class="fx-app-icono" width="136" height="136"></div>' % (esc(icono_src), esc(app["nombre"]))
        return '<div class="fx-app-icono-wrap"><div class="fx-app-icono fx-card-icono-vacio">✦</div></div>'


def generar_hero_garantias(app: dict) -> str:
    """Franja de garantías de privacidad y calidad técnica para el hero."""
    slug = app.get("slug")
    if slug == "debts-goodbye":
        return """
            <div class="fx-hero-garantias">
                <div class="fx-garantia-item">
                    <span class="fx-garantia-ico">🛡️</span>
                    <div class="fx-garantia-content">
                        <strong>100% Privado</strong>
                        <span>Cero anuncios · Sin rastreadores</span>
                    </div>
                </div>
                <div class="fx-garantia-item">
                    <span class="fx-garantia-ico">🧮</span>
                    <div class="fx-garantia-content">
                        <strong>Algoritmo Avalancha</strong>
                        <span>Ahorra millones en intereses</span>
                    </div>
                </div>
                <div class="fx-garantia-item">
                    <span class="fx-garantia-ico">✨</span>
                    <div class="fx-garantia-content">
                        <strong>Copiloto Fynex IA</strong>
                        <span>Diagnóstico DTI en tiempo real</span>
                    </div>
                </div>
            </div>"""
    elif slug == "audiout":
        return """
            <div class="fx-hero-garantias">
                <div class="fx-garantia-item">
                    <span class="fx-garantia-ico">⚡</span>
                    <div class="fx-garantia-content">
                        <strong>Cero Eco Acústico</strong>
                        <span>Compensación BT A2DP vs HDMI</span>
                    </div>
                </div>
                <div class="fx-garantia-item">
                    <span class="fx-garantia-ico">🔒</span>
                    <div class="fx-garantia-content">
                        <strong>LockedDelayFIFO</strong>
                        <span>Búfer elástico anti-desfase</span>
                    </div>
                </div>
                <div class="fx-garantia-item">
                    <span class="fx-garantia-ico">🛡️</span>
                    <div class="fx-garantia-content">
                        <strong>Sin Drivers de Kernel</strong>
                        <span>100% Estable en Windows 10/11</span>
                    </div>
                </div>
            </div>"""
    return ""


def generar_pilares(app: dict) -> str:
    """Pilares profundos de propuesta de valor e ingeniería de cada producto."""
    slug = app.get("slug")
    if slug == "debts-goodbye":
        return """
<section class="fx-seccion fx-seccion-pilares">
    <div class="fx-contenedor">
        <div class="fx-seccion-cab centrado fx-revelar">
            <span class="fx-app-badge-oficial" style="margin-bottom: 14px;">✦ INGENIERÍA FINANCIERA</span>
            <h2>Control patrimonial con rigor matemático</h2>
            <p>Debts Goodbye no es una simple libreta de apuntes: es un motor algorítmico diseñado para optimizar tu flujo de caja, eliminar intereses parásitos y proteger tu privacidad.</p>
        </div>
        <div class="fx-pilares-grid fx-revelar">
            <article class="fx-pilar-card">
                <div class="fx-pilar-numero">01</div>
                <div class="fx-pilar-icono">🧮</div>
                <h3>Amortización Científica: Avalancha vs Bola de Nieve</h3>
                <p>Compara el impacto financiero de liquidar primero las deudas de mayor tasa efectiva anual (Avalancha) frente a las de menor saldo (Bola de Nieve). Incluye soporte exclusivo para Crédito Educativo con período de gracia de capital.</p>
                <div class="fx-pilar-chip">Ahorro proyectado de hasta 42% en intereses</div>
            </article>
            <article class="fx-pilar-card">
                <div class="fx-pilar-numero">02</div>
                <div class="fx-pilar-icono">💳</div>
                <h3>Matemática Unificada de Tarjetas con Anclaje Bancario</h3>
                <p>Motor de cuotas compartidas que avanza automáticamente con el calendario. Si el extracto bancario difiere por seguros o comisiones, puedes fijar un "ancla" y la serie temporal se recalcula en tiempo real.</p>
                <div class="fx-pilar-chip">Sincronización exacta con extractos bancarios</div>
            </article>
            <article class="fx-pilar-card">
                <div class="fx-pilar-numero">03</div>
                <div class="fx-pilar-icono">🤖</div>
                <h3>Copiloto Fynex IA con Privacidad Absoluta</h3>
                <p>Diagnóstico patrimonial instantáneo, cálculo de ratio DTI (Deuda sobre Ingreso), registro conversacional por lenguaje natural y exportación ejecutiva en PDF. Cero publicidad, cero rastreadores y sin venta de datos a terceros.</p>
                <div class="fx-pilar-chip">5 consultas gratuitas diarias · 100% Privado</div>
            </article>
        </div>
    </div>
</section>"""
    elif slug == "audiout":
        return """
<section class="fx-seccion fx-seccion-pilares">
    <div class="fx-contenedor">
        <div class="fx-seccion-cab centrado fx-revelar">
            <span class="fx-app-badge-oficial" style="margin-bottom: 14px;">✦ INGENIERÍA DE AUDIO DIGITAL</span>
            <h2>Transmisión acústica sincronizada para Windows</h2>
            <p>Audiout resuelve los desafíos físicos de la latencia de radiofrecuencia Bluetooth y el desfase de transporte entre periféricos de sonido independientes.</p>
        </div>
        <div class="fx-pilares-grid fx-revelar">
            <article class="fx-pilar-card">
                <div class="fx-pilar-numero">01</div>
                <div class="fx-pilar-icono">⚡</div>
                <h3>La Física del Desfase Bluetooth vs HDMI Resuelta</h3>
                <p>Los parlantes Bluetooth A2DP introducen de 120 ms a 200 ms de latencia por hardware. Audiout retarda las salidas cableadas en la cantidad milimétrica exacta (ej. 165 ms) para que el sonido llegue a tus oídos al mismo instante físico, eliminando el filtrado peine.</p>
                <div class="fx-pilar-chip">Cero eco acústico · Sincronización al unísono</div>
            </article>
            <article class="fx-pilar-card">
                <div class="fx-pilar-numero">02</div>
                <div class="fx-pilar-icono">🔒</div>
                <h3>Motor DSP LockedDelayFIFO Anti-Deriva</h3>
                <p>Búfer elástico en tiempo real que absorbe derivas de reloj oscilador y purga colas parásitas al pausar o cambiar videos en YouTube, Netflix o Spotify. Mantiene la sincronización estricta sin desafinar el audio.</p>
                <div class="fx-pilar-chip">Convergencia permanente a 0 ms de error</div>
            </article>
            <article class="fx-pilar-card">
                <div class="fx-pilar-numero">03</div>
                <div class="fx-pilar-icono">🔀</div>
                <h3>Enrutamiento Selectivo con WinRT AudioPolicy</h3>
                <p>Asigna dispositivos de audio independientes por proceso (Spotify a parlantes externos, Discord a auriculares, Chrome al monitor) sin instalar controladores de kernel invasivos ni requerir reinicios del sistema operativo.</p>
                <div class="fx-pilar-chip">WASAPI Float 32-bit · Menos de 1.5% de CPU</div>
            </article>
        </div>
    </div>
</section>"""
    else:
        desc = app.get("descripcion_larga", "")
        if not desc:
            return ""
        return """
<section class="fx-seccion">
    <div class="fx-contenedor">
        <div class="fx-seccion-cab fx-revelar" style="max-width:820px; margin-left:auto; margin-right:auto; text-align:center;">
            <h2>Acerca de %s</h2>
            <p style="font-size:1.1rem; line-height:1.7;">%s</p>
        </div>
    </div>
</section>""" % (esc(app["nombre"]), esc(desc))


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
                    <div class="fx-desktop-bar">
                        <span class="fx-desktop-dot rojo"></span>
                        <span class="fx-desktop-dot amarillo"></span>
                        <span class="fx-desktop-dot verde"></span>
                        <span class="fx-desktop-title-tiny">Audiout v1.0.0 — Centro de Control</span>
                    </div>
                    <div class="fx-desktop-pantalla">
                        <img src="/%s" alt="%s" class="fx-desktop-img" id="mockupPantalla">
                    </div>
                </div>""" % (esc(primero["captura"]), esc(primero["titulo"]))
        else:
            marco_mockup = """
                <div class="fx-celular-frame">
                    <div class="fx-celular-speaker"></div>
                    <div class="fx-celular-pantalla">
                        <img src="/%s" alt="%s" class="fx-celular-img" id="mockupPantalla">
                    </div>
                </div>""" % (esc(primero["captura"]), esc(primero["titulo"]))

        clase_showcase = "fx-showcase fx-revelar" + (" fx-showcase-desktop" if tipo_disp == "desktop" else "")

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

        <div class="%s">
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
            clase_showcase,
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
    slug = app.get("slug")
    if slug == "debts-goodbye":
        titulo_cta = "Comienza hoy tu camino hacia la libertad financiera"
        desc_cta = "Sin anuncios invasivos, sin suscripciones forzosas y con total control de tus datos. Disponible en la Web y en Google Play."
    elif slug == "audiout":
        titulo_cta = "Experimenta el sonido al unísono definitivo en Windows"
        desc_cta = "Descarga el instalador oficial guiado para Windows 10 y 11 o utiliza la versión 100% portable lista para llevar en USB."
    else:
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
        if not t.get("url"):
            continue
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

    # Hero enriquecido
    if slug == "debts-goodbye":
        badge_hero = "✦ SAAS FINANCIERO PERSONAL"
        hero_titulo = "Sal de tus deudas con un plan, no con suerte."
        tagline_txt = "Control total de ingresos, gastos, deudas y tarjetas con Fynex IA, estrategias científicas Avalancha y Bola de Nieve, y sincronización nativa en tiempo real."
    elif slug == "audiout":
        badge_hero = "✦ ESTACIÓN DE AUDIO NATIVA PARA WINDOWS"
        hero_titulo = "Sincroniza y duplica audio en Windows al unísono."
        tagline_txt = "Transmite simultáneamente a parlantes Bluetooth, HDMI y altavoces con sincronización milimétrica al instante, motor LockedDelayFIFO anti-desfase y división por programas."
    else:
        badge_hero = "✦ Producto Oficial FYNEX"
        hero_titulo = esc(app["nombre"])
        tagline_txt = esc(app.get("tagline") or app.get("descripcion_corta", ""))

    return rellenar(plantilla, {
        "NOMBRE": esc(app["nombre"]),
        "DESC_CORTA": esc(app["descripcion_corta"]),
        "COLOR": esc(app["color"]),
        "CATEGORIA": esc(app["categoria"]),
        "TAGLINE": tagline_txt,
        "VERSION": esc(app.get("version", "1.0.0")),
        "ICONO": icono,
        "ICONO_URL": esc(app.get("icono", "img/apps/debts-goodbye.png")),
        "BADGE_HERO": badge_hero,
        "HERO_TITULO": hero_titulo,
        "HERO_GARANTIAS": generar_hero_garantias(app),
        "HERO_VISUAL": generar_hero_visual(app),
        "BOTONES": botones_hero(app),
        "METRICAS": metricas,
        "SHOWCASE_GALERIA": showcase,
        "PILARES_VALOR": generar_pilares(app),
        "NOVEDADES": novedades,
        "CARACTERISTICAS": caracteristicas,
        "ARQUITECTURA": arquitectura,
        "CTA_BANNER": cta_banner,
        "NAV_CTA": nav_cta,
        "PLATAFORMAS": "".join('<span class="fx-plataforma">%s</span>' % esc(p)
                               for p in app.get("plataformas", [])),
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
