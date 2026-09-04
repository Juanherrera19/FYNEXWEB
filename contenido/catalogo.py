"""
Catálogo de productos de FYNEX.

Esta es la única fuente de verdad del sitio: agregar una app o un juego es añadir una
entrada aquí y volver a generar. No hay que tocar plantillas ni estilos.

Campos de cada entrada
----------------------
slug            Identifica el producto. Define su URL: /apps/<slug>/
nombre          Nombre comercial.
url_propia      Sitio propio del producto (su subdominio). None si aún no tiene.
estado          "publicada" o "proximamente".
destacada       True para el producto que encabeza la portada. Solo uno.
tipo            "app" o "juego". Se muestra como etiqueta.
categoria       Categoría corta, en mayúsculas pequeñas sobre la tarjeta.
tagline         Una frase. Lo que hace, dicho en corto.
descripcion_corta   Va en la tarjeta del catálogo y en las etiquetas para compartir.
descripcion_larga   Párrafo de la página de detalle. Vacío = no se muestra la sección.
icono           Ruta relativa dentro de estaticos/. None dibuja un marcador.
color           Color de acento del producto, en hexadecimal.
caracteristicas Lista de {emoji, titulo, texto} para la página de detalle.
tiendas         Lista de {nombre, url, icono}. Vacía = "Próximamente".
plataformas     Etiquetas sueltas: Android, iOS, Web...
url_privacidad  Política de privacidad del producto. None la omite.
"""

from typing import List, Optional

DOMINIO = "fynexhq.com"

APPS: List[dict] = [
    {
        "slug": "debts-goodbye",
        "nombre": "Debts Goodbye",
        "url_propia": "https://dgb.fynexhq.com",
        "estado": "publicada",
        "destacada": True,
        "tipo": "app",
        "categoria": "Finanzas personales",
        "tagline": "Sal de tus deudas con un plan, no con suerte.",
        "descripcion_corta": (
            "Controla ingresos, gastos, deudas y tarjetas de crédito en un solo lugar, "
            "con simuladores que te muestran cuánto ahorras al pagar distinto."
        ),
        "descripcion_larga": (
            "Debts Goodbye reúne tu vida financiera en una sola vista: cuánto entra, "
            "cuánto sale, cuánto debes y cuánto te queda. Registra tus deudas y tarjetas, "
            "sigue las cuotas mes a mes, define presupuestos por categoría y simula "
            "escenarios de pago para ver, en números, cuánto interés te ahorras si "
            "abonas de otra forma."
        ),
        "icono": "img/apps/debts-goodbye.png",
        "color": "#1E7881",
        "caracteristicas": [
            {
                "emoji": "📊",
                "titulo": "Todo tu dinero en una vista",
                "texto": "Ingresos, gastos, deudas y tarjetas en un solo panel, con tu posición financiera neta siempre a la vista.",
            },
            {
                "emoji": "💳",
                "titulo": "Cuotas que se llevan solas",
                "texto": "Las compras a cuotas avanzan con el calendario, y si tu banco cuenta distinto, corriges el estado real y sigue avanzando desde ahí.",
            },
            {
                "emoji": "🎯",
                "titulo": "Presupuestos por categoría",
                "texto": "Define cuánto puedes gastar en cada cosa, con tus propias categorías, iconos y colores.",
            },
            {
                "emoji": "🧮",
                "titulo": "Simuladores de pago",
                "texto": "Compara escenarios y descubre cuánto interés te ahorras pagando de otra manera.",
            },
            {
                "emoji": "✈️",
                "titulo": "Gastos de viaje compartidos",
                "texto": "Reparte cuentas entre varias personas y liquida quién le debe cuánto a quién.",
            },
            {
                "emoji": "🤖",
                "titulo": "Asesor con IA",
                "texto": "Preguntas sobre tus propias finanzas, respondidas con tus datos reales.",
            },
        ],
        "tiendas": [
            {
                "nombre": "Google Play",
                "url": "https://play.google.com/store/apps/details?id=com.debtsgoodbye.free",
                "icono": "▶",
            },
        ],
        "plataformas": ["Android", "Web"],
        "url_privacidad": "https://dgb.fynexhq.com/privacy-policy",
    },
    {
        "slug": "proximamente-app",
        "nombre": "En construcción",
        "url_propia": None,
        "estado": "proximamente",
        "destacada": False,
        "tipo": "app",
        "categoria": "Productividad",
        "tagline": "Algo nuevo se está cocinando.",
        "descripcion_corta": "Nuestra próxima aplicación ya está en desarrollo. Muy pronto por aquí.",
        "descripcion_larga": "",
        "icono": None,
        "color": "#6366f1",
        "caracteristicas": [],
        "tiendas": [],
        "plataformas": [],
        "url_privacidad": None,
    },
    {
        "slug": "proximamente-juego",
        "nombre": "En construcción",
        "url_propia": None,
        "estado": "proximamente",
        "destacada": False,
        "tipo": "juego",
        "categoria": "Juegos",
        "tagline": "Nuestro primer juego está en camino.",
        "descripcion_corta": "Seguimos construyendo. Vuelve pronto para conocerlo.",
        "descripcion_larga": "",
        "icono": None,
        "color": "#f97316",
        "caracteristicas": [],
        "tiendas": [],
        "plataformas": [],
        "url_privacidad": None,
    },
]

# Datos del estudio, usados en la portada y el pie.
ESTUDIO = {
    "nombre": "FYNEX",
    "descripcion": "Estudio de desarrollo de apps y juegos para móvil y web.",
    "email": "contacto@fynexhq.com",
    "url": "https://www.fynexhq.com",
}


def todas() -> List[dict]:
    return APPS


def publicadas() -> List[dict]:
    return [a for a in APPS if a["estado"] == "publicada"]


def destacada() -> Optional[dict]:
    """El producto que encabeza la portada."""
    for a in APPS:
        if a.get("destacada") and a["estado"] == "publicada":
            return a
    pubs = publicadas()
    return pubs[0] if pubs else None


def por_slug(slug: str) -> Optional[dict]:
    for a in APPS:
        if a["slug"] == slug:
            return a
    return None
