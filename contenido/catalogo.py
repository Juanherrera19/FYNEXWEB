"""
Catálogo de productos de FYNEX.

Esta es la única fuente de verdad del sitio: agregar una app o un juego es añadir una
entrada aquí y volver a generar. No hay que tocar plantillas ni estilos.
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
        "version": "1.2.18",
        "tagline": "Sal de tus deudas con un plan, no con suerte.",
        "descripcion_corta": (
            "Controla ingresos, gastos, deudas y tarjetas en un solo lugar con Fynex IA, "
            "métodos Avalancha y Bola de Nieve, simulador de 9 créditos y widgets para Android."
        ),
        "descripcion_larga": (
            "Debts Goodbye reúne tu vida financiera en una sola vista integral: cuánto entra, "
            "cuánto sale, cuánto debes y cuánto te queda disponible. Diseñada por FYNEX para móvil "
            "y web sobre la misma base de datos en tiempo real, incorpora un asesor financiero con IA "
            "(Fynex IA), estrategias científicas de amortización acelerada (Avalancha y Bola de Nieve), "
            "matemática unificada de cuotas de tarjeta de crédito con anclaje bancario, simulador "
            "multiproducto de 9 modalidades de crédito, presupuestos flexibles con categorías personalizables "
            "y widgets interactivos para la pantalla de inicio de Android."
        ),
        "icono": "img/apps/debts-goodbye.png",
        "color": "#1E7881",
        "metas": [
            {
                "valor": "100% Gratis",
                "etiqueta": "Sin anuncios ni suscripciones ocultas",
                "icono": "🛡️",
            },
            {
                "valor": "9 Créditos",
                "etiqueta": "Simulador multiproducto con tablas EA/MV",
                "icono": "🧮",
            },
            {
                "valor": "Fynex IA",
                "etiqueta": "Asesor inteligente y 5 consultas gratis/día",
                "icono": "✨",
            },
            {
                "valor": "Móvil & Web",
                "etiqueta": "Sincronización total y widgets de escritorio",
                "icono": "📱",
            },
        ],
        "showcase": [
            {
                "id": "ia",
                "badge": "Asesor Financiero IA",
                "titulo": "Fynex IA a tu Servicio",
                "subtitulo": "Estrategias personalizadas para liquidar tus deudas",
                "desc": (
                    "Chat inteligente con diagnóstico patrimonial en tiempo real, cálculo de DTI "
                    "(Deuda sobre Ingreso), flujo de caja libre, registro conversacional de gastos "
                    "e ingresos con tarjeta interactiva de confirmación y exportación de informe ejecutivo en PDF."
                ),
                "captura": "img/apps/debts-goodbye/capturas/01_fynex_ia_real.png",
                "slide": "img/apps/debts-goodbye/publicitarias/slide_01_fynex_ia.jpg",
            },
            {
                "id": "dashboard",
                "badge": "Visión Financiera 360°",
                "titulo": "Control Total de tus Finanzas",
                "subtitulo": "Ingresos, gastos, deudas y flujo libre en un solo lugar",
                "desc": (
                    "Dashboard unificado con posición financiera neta en vivo, ingresos mensuales, "
                    "gastos ejecutados, saldo consolidado de deudas y cupo disponible en tarjetas de crédito."
                ),
                "captura": "img/apps/debts-goodbye/capturas/02_dashboard_resumen_real.png",
                "slide": "img/apps/debts-goodbye/publicitarias/slide_02_dashboard_resumen.jpg",
            },
            {
                "id": "deudas",
                "badge": "Métodos Avalancha y Bola de Nieve",
                "titulo": "Plan Maestro de Deudas",
                "subtitulo": "Ahorra millones en intereses y acelera tu libertad",
                "desc": (
                    "Organiza tus obligaciones por entidad bancaria, tasas EA/MV y plazo. Incluye "
                    "estrategias científicas de pago anticipado y soporte exclusivo para Crédito Educativo "
                    "con período de gracia de capital (pago exclusivo de intereses causados)."
                ),
                "captura": "img/apps/debts-goodbye/capturas/03_plan_deudas_real.png",
                "slide": "img/apps/debts-goodbye/publicitarias/slide_03_plan_deudas.jpg",
            },
            {
                "id": "tarjetas",
                "badge": "Gestión Inteligente de Tarjetas",
                "titulo": "Tarjetas y Matemática de Cuotas",
                "subtitulo": "Cupos, fechas de corte, pagos mínimos y diferidos",
                "desc": (
                    "Motor matemático único de cuotas compartidas entre web y app móvil. Fija anclas "
                    "para ajustar compras si el extracto bancario difiere, simula pagos mínimos y calcula "
                    "exactamente cuánto liberarás mes a mes."
                ),
                "captura": "img/apps/debts-goodbye/capturas/04_tarjetas_credito_real.png",
                "slide": "img/apps/debts-goodbye/publicitarias/slide_04_tarjetas_credito.jpg",
            },
            {
                "id": "simulador",
                "badge": "Simulador Multiproducto",
                "titulo": "9 Modalidades de Crédito y Conversión EA/MV",
                "subtitulo": "Calcula cuotas exactas de libre inversión, vivienda y UVR",
                "desc": (
                    "Simula créditos de vehículo, libranza, leasing habitacional y préstamos con seguro "
                    "de vida y capitalización. Visualiza el calendario de amortización detallado y exporta a Excel/PDF."
                ),
                "captura": "img/apps/debts-goodbye/capturas/05_simulador_credito_real.png",
                "slide": "img/apps/debts-goodbye/publicitarias/slide_05_simulador_credito.jpg",
            },
            {
                "id": "presupuestos",
                "badge": "Presupuestos y Flujo de Caja",
                "titulo": "Protege tu Flujo de Caja",
                "subtitulo": "Establece metas mensuales y evita gastos innecesarios",
                "desc": (
                    "Crea categorías personalizadas con iconos y colores dinámicos. Configura límites "
                    "de gasto, decide con un interruptor si incluir o separar deudas del presupuesto general "
                    "y recibe alertas preventivas antes de sobregirarte."
                ),
                "captura": "img/apps/debts-goodbye/capturas/06_presupuestos_flujo_real.png",
                "slide": "img/apps/debts-goodbye/publicitarias/slide_06_presupuestos_flujo.jpg",
            },
        ],
        "novedades": [
            {
                "titulo": "Widgets para Android (AppWidgets)",
                "desc": "Resumen Financiero (4x2) y Acciones Rápidas (2x2) nativos en pantalla de inicio con sincronización automática en tiempo real.",
                "icono": "📱",
            },
            {
                "titulo": "Crédito Educativo con Período de Gracia",
                "desc": "Cálculo financiero que durante la prórroga de capital exige solo intereses causados, liberando flujo para amortizar la deuda más cara.",
                "icono": "🎓",
            },
            {
                "titulo": "Presupuesto de Deudas Flexible",
                "desc": "Límite editable para la categoría Deudas con opción para decidir si computan dentro del presupuesto mensual o se gestionan por separado.",
                "icono": "📊",
            },
            {
                "titulo": "Modales Asíncronos Integrados",
                "desc": "Reemplazo de diálogos nativos por ventanas modales asíncronas con diseño estilizado, autoenfoque y atajos Enter y Escape en web.",
                "icono": "💻",
            },
            {
                "titulo": "Gastos de Viaje Compartidos",
                "desc": "Reparte cuentas entre varias personas en salidas o viajes grupales y liquida quién le debe cuánto a quién con un solo clic.",
                "icono": "✈️",
            },
            {
                "titulo": "Android 15+ Edge-to-Edge y R8",
                "desc": "Cumplimiento total de Google Play SDK 36: diseño visual borde a borde nativo, ofuscación R8 y cero identificadores de publicidad.",
                "icono": "⚡",
            },
        ],
        "caracteristicas": [
            {
                "emoji": "📊",
                "titulo": "Todo tu dinero en una vista",
                "texto": "Ingresos, gastos, deudas y tarjetas en un solo panel, con tu posición financiera neta siempre clara y al día.",
            },
            {
                "emoji": "🤖",
                "titulo": "Fynex IA: Tu copiloto financiero",
                "texto": "Diagnósticos en vivo, 5 consultas diarias sin costo, registro conversacional de apuntes y reportes ejecutivos en PDF.",
            },
            {
                "emoji": "💳",
                "titulo": "Cuotas que avanzan solas",
                "texto": "Las compras a cuotas avanzan con el calendario. Si el banco difiere, fijas un ancla y la progresión continúa desde ahí.",
            },
            {
                "emoji": "🎯",
                "titulo": "Presupuestos con categorías propias",
                "texto": "Define cuánto gastar en cada aspecto de tu vida, personalizando nombres, iconos dinámicos y paletas de color.",
            },
            {
                "emoji": "🧮",
                "titulo": "Simulador de 9 tipos de crédito",
                "texto": "Compara escenarios para libre inversión, vivienda, UVR o vehículos y descubre cuánto ahorras en intereses abonando de otra forma.",
            },
            {
                "emoji": "📱",
                "titulo": "Widgets de escritorio en Android",
                "texto": "Consulta balances, ingresos y gastos directamente desde la pantalla de inicio de tu smartphone sin abrir la app.",
            },
            {
                "emoji": "✈️",
                "titulo": "Gastos de viaje compartidos",
                "texto": "Divide cuentas comunes entre amigos o familiares y obtén la liquidación exacta de quién le debe a quién.",
            },
            {
                "emoji": "🔒",
                "titulo": "Privacidad y cero publicidad",
                "texto": "Tus finanzas son estrictamente tuyas. Sin anuncios invasivos, sin venta de datos a terceros y con total transparencia.",
            },
        ],
        "tiendas": [
            {
                "nombre": "Google Play",
                "url": "https://play.google.com/store/apps/details?id=com.debtsgoodbye.free",
                "icono": "▶",
            },
        ],
        "plataformas": ["Android 15+", "Web App", "Multiplataforma"],
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
        "tagline": "Algo nuevo se está cocinando en FYNEX.",
        "descripcion_corta": "Nuestra próxima aplicación de productividad ya está en diseño y desarrollo. Muy pronto por aquí.",
        "descripcion_larga": "",
        "icono": None,
        "color": "#6366f1",
        "metas": [],
        "showcase": [],
        "novedades": [],
        "caracteristicas": [],
        "tiendas": [],
        "plataformas": ["Próximamente"],
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
        "tagline": "Nuestro primer juego móvil está en camino.",
        "descripcion_corta": "Una experiencia interactiva diseñada para cautivar y disfrutar. Vuelve pronto para conocer el lanzamiento.",
        "descripcion_larga": "",
        "icono": None,
        "color": "#f97316",
        "metas": [],
        "showcase": [],
        "novedades": [],
        "caracteristicas": [],
        "tiendas": [],
        "plataformas": ["Próximamente"],
        "url_privacidad": None,
    },
]

# Datos del estudio, usados en la portada y el pie.
ESTUDIO = {
    "nombre": "FYNEX",
    "descripcion": "Estudio de diseño y desarrollo de apps y juegos móviles y web de alto impacto.",
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
