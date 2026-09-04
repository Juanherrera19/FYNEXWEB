#!/usr/bin/env python3
"""
Generador del sitio de FYNEX.

Lee el catálogo (contenido/catalogo.py), rellena las plantillas y escribe un sitio
estático en dist/. No hay servidor ni base de datos: el resultado son archivos HTML
que cualquier hosting estático sirve al instante, sin arranque en frío.

    python build.py            genera dist/
    python build.py --servir   genera y levanta un servidor local para revisarlo

Todo texto que sale del catálogo se escapa antes de insertarse. Hoy el catálogo lo
escribimos nosotros, pero así el día que venga de otra fuente la página ya está
preparada.
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
    """Botón al sitio propio del producto y botones de tienda."""
    partes = []

    if app.get("url_propia"):
        partes.append(
            '<a href="%s" class="fx-btn fx-btn-primario%s">Abrir %s</a>'
            % (esc(app["url_propia"]), clase_extra, esc(app["nombre"]))
        )

    for tienda in app.get("tiendas", []):
        partes.append(
            '<a href="%s" class="fx-btn fx-btn-secundario%s" target="_blank" '
            'rel="noopener noreferrer">%s %s</a>'
            % (esc(tienda["url"]), clase_extra, esc(tienda.get("icono", "↗")),
               esc(tienda["nombre"]))
        )

    if not partes:
        partes.append('<span class="fx-insignia-pronto">Próximamente</span>')

    return "".join(partes)


def tarjeta(app: dict) -> str:
    """Una tarjeta del catálogo."""
    pronto = app["estado"] != "publicada"
    clases = "fx-card fx-revelar" + (" fx-card-pronto" if pronto else "")

    if app.get("icono"):
        icono = ('<img src="/%s" alt="" class="fx-card-icono" width="62" height="62" '
                 'loading="lazy">' % esc(app["icono"]))
    else:
        icono = '<div class="fx-card-icono fx-card-icono-vacio">✦</div>'

    if pronto:
        pie = '<span class="fx-insignia-pronto">Próximamente</span>'
    else:
        pie = ('<a href="/apps/%s/" class="fx-btn fx-btn-secundario fx-btn-sm">Ver detalles</a>'
               % esc(app["slug"])) + botones(app, " fx-btn-sm")

    return """
        <article class="%s" style="--app-color: %s;">
            %s
            <div class="fx-card-cat">%s</div>
            <h3>%s</h3>
            <p>%s</p>
            <div class="fx-card-pie">%s</div>
        </article>""" % (
        clases, esc(app["color"]), icono, esc(app["categoria"]),
        esc(app["nombre"]), esc(app["descripcion_corta"]), pie,
    )


def seccion_destacada(app) -> str:
    if not app:
        return ""

    visual = ""
    if app.get("icono"):
        visual = ('<div class="fx-destacada-visual">'
                  '<img src="/%s" alt="%s" width="260" height="260"></div>'
                  % (esc(app["icono"]), esc(app["nombre"])))

    return """
<section class="fx-seccion">
    <div class="fx-contenedor">
        <div class="fx-destacada fx-revelar" style="--app-color: %s;">
            <div class="fx-destacada-txt">
                <span class="fx-destacada-cat">Destacada · %s</span>
                <h3>%s</h3>
                <p class="fx-tagline">%s</p>
                <p class="fx-desc">%s</p>
                <div class="fx-acciones" style="justify-content:flex-start;">
                    <a href="/apps/%s/" class="fx-btn fx-btn-secundario">Ver detalles</a>
                    %s
                </div>
            </div>
            %s
        </div>
    </div>
</section>""" % (
        esc(app["color"]), esc(app["categoria"]), esc(app["nombre"]),
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

    if app.get("icono"):
        icono = ('<img src="/%s" alt="%s" class="fx-app-icono" width="122" height="122">'
                 % (esc(app["icono"]), esc(app["nombre"])))
    else:
        icono = '<div class="fx-app-icono fx-card-icono-vacio">✦</div>'

    descripcion = ""
    if app.get("descripcion_larga"):
        descripcion = """
<section class="fx-seccion fx-seccion-alt">
    <div class="fx-contenedor">
        <div class="fx-seccion-cab">
            <h2>Qué hace</h2>
            <p>%s</p>
        </div>
    </div>
</section>""" % esc(app["descripcion_larga"])

    caracteristicas = ""
    if app.get("caracteristicas"):
        tarjetas = "".join("""
            <article class="fx-caracteristica fx-revelar">
                <span class="emoji">%s</span>
                <h4>%s</h4>
                <p>%s</p>
            </article>""" % (esc(c["emoji"]), esc(c["titulo"]), esc(c["texto"]))
            for c in app["caracteristicas"])
        caracteristicas = """
<section class="fx-seccion">
    <div class="fx-contenedor">
        <div class="fx-seccion-cab centrado">
            <h2>Lo que puedes hacer</h2>
        </div>
        <div class="fx-caracteristicas">%s</div>
    </div>
</section>""" % tarjetas

    # La política de privacidad vive en el sitio del producto, no aquí.
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
        "ICONO": icono,
        "PLATAFORMAS": "".join('<span class="fx-plataforma">%s</span>' % esc(p)
                               for p in app.get("plataformas", [])),
        "BOTONES": botones(app),
        "DESCRIPCION": descripcion,
        "CARACTERISTICAS": caracteristicas,
        "FOOTER_APPS": apps_del_pie(),
        "ESTUDIO_DESC": esc(catalogo.ESTUDIO["descripcion"]),
        "PRIVACIDAD": privacidad,
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

    (SALIDA / "404.html").write_text(generar_404(), encoding="utf-8")
    paginas += 1

    # robots.txt y sitemap, para que el sitio se indexe bien
    base = catalogo.ESTUDIO["url"].rstrip("/")
    (SALIDA / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % base, encoding="utf-8")

    urls = ["%s/" % base] + [
        "%s/apps/%s/" % (base, a["slug"]) for a in catalogo.publicadas()
    ]
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
