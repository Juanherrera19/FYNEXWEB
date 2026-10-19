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
            "métodos Avalancha y Bola de Nieve, simulador de amortización y widgets para Android."
        ),
        "descripcion_larga": (
            "Debts Goodbye reúne tu vida financiera en una sola vista integral: cuánto entra, "
            "cuánto sale, cuánto debes y cuánto te queda disponible. Diseñada por FYNEX para móvil "
            "y web sobre la misma base de datos en tiempo real, incorpora un asesor financiero con IA "
            "(Fynex IA), estrategias científicas de amortización acelerada (Avalancha y Bola de Nieve), "
            "matemática unificada de cuotas de tarjeta de crédito con anclaje bancario, simulador "
            "multiproducto de amortización y crédito, presupuestos flexibles con categorías personalizables "
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
                "valor": "Simulador",
                "etiqueta": "Amortización, tasas EA/MV y ahorro en cuotas",
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
                "nombre_corto": "Asesor IA",
                "icono_corto": "✨",
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
                "nombre_corto": "Visión 360°",
                "icono_corto": "📊",
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
                "nombre_corto": "Plan Deudas",
                "icono_corto": "📉",
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
                "nombre_corto": "Tarjetas",
                "icono_corto": "💳",
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
                "nombre_corto": "Simulador",
                "icono_corto": "🧮",
                "titulo": "Simulador de Crédito y Amortización",
                "subtitulo": "Calcula cuotas exactas, tablas de amortización y UVR",
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
                "nombre_corto": "Presupuestos",
                "icono_corto": "🎯",
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
                "titulo": "Simulador de amortización y crédito",
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
        "arquitectura": [
            {
                "titulo": "FastAPI + Python Backend",
                "desc": "Matemática única centralizada en servicios backend con tipado estricto Pydantic y alta velocidad de respuesta.",
            },
            {
                "titulo": "Flutter Multiplataforma",
                "desc": "Experiencia nativa ultra fluida a 60-120 FPS en Android, iOS y Web con una única base de código compartida.",
            },
            {
                "titulo": "Base de Datos Dual & Pool",
                "desc": "Capa de abstracción que soporta SQLite local para desarrollo y PostgreSQL con pool de conexiones en producción.",
            },
            {
                "titulo": "Android 15+ Edge-to-Edge & R8",
                "desc": "Diseño visual nativo borde a borde, optimización DEX, ofuscación R8 y cero identificadores de publicidad.",
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
        "tipo_dispositivo": "movil",
        "url_privacidad": "https://dgb.fynexhq.com/privacy-policy",
    },
    {
        "slug": "audiout",
        "nombre": "AUDIOUT",
        "url_propia": None,
        "url_descargas": "/apps/audiout/descargas/",
        "estado": "publicada",
        "destacada": False,
        "tipo": "app",
        "tipo_dispositivo": "desktop",
        "categoria": "Audio & Utilidades",
        "version": "1.0.0",
        "tagline": "Enrutador y duplicador de audio con sincronización acústica al unísono.",
        "descripcion_corta": (
            "Duplica y enruta audio en Windows 10 y 11 hacia múltiples parlantes (Bluetooth, HDMI, Altavoces) "
            "con sincronización milimétrica al unísono, cero eco, motor LockedDelayFIFO y división por aplicaciones."
        ),
        "descripcion_larga": (
            "AUDIOUT v1.0 es una solución profesional, ligera y de alto rendimiento desarrollada por FYNEX "
            "para resolver la duplicación y el enrutamiento simultáneo de audio en Windows 10 y Windows 11. "
            "Gracias a su innovador motor DSP LockedDelayFIFO, elimina por completo el desfase acumulado y el sonido "
            "robótico por filtrado peine entre dispositivos con diferentes latencias de transporte (como parlantes "
            "Bluetooth A2DP frente a monitores HDMI o altavoces integrados), garantizando una emisión de ondas al mismo "
            "milisegundo exacto tanto en streaming continuo como en cambios o pausas de video en YouTube, Netflix o Spotify."
        ),
        "icono": "img/apps/audiout/audiout-logo.png",
        "color": "#0284c7",
        "metas": [
            {
                "valor": "165 ms",
                "etiqueta": "Compensación de latencia Bluetooth unísono",
                "icono": "⚡",
            },
            {
                "valor": "Cero Eco",
                "etiqueta": "Eliminación de filtrado peine acústico",
                "icono": "🎧",
            },
            {
                "valor": "WASAPI Float",
                "etiqueta": "32-bit a 48,000 Hz estéreo en tiempo real",
                "icono": "🎛️",
            },
            {
                "valor": "<1.5% CPU",
                "etiqueta": "Bajo consumo y ~30 MB de memoria",
                "icono": "💻",
            },
        ],
        "descargas": [
            {
                "id": "setup",
                "nombre": "Instalador Oficial Windows (.exe)",
                "sub": "Windows 10 / Windows 11 (64-bit)",
                "badge": "✦ Recomendado",
                "badge_tipo": "rec",
                "icono": "💿",
                "url": "https://drive.google.com/drive/folders/1BzHp_vREEDwLDs0Da5LQYO0hL3LB_vkk?usp=sharing",
                "archivo": "AUDIOUT_Setup.exe",
                "primario": True,
                "destacado": True,
                "pronto": False,
                "desc": "Asistente de instalación oficial guiado. Crea accesos directos en Escritorio y Menú Inicio, opción de auto-inicio con Windows y desinstalador formal.",
                "puntos": [
                    "Instalación limpia y asistente visual",
                    "Accesos directos con logotipo oficial",
                    "Registro en Configuración de Windows para desinstalar en 1 clic",
                ],
            },
            {
                "id": "portable",
                "nombre": "Versión Portable (.exe)",
                "sub": "Windows 10 / Windows 11 (64-bit)",
                "badge": "⚡ Sin Instalación",
                "badge_tipo": "portable",
                "icono": "📦",
                "url": "https://drive.google.com/file/d/1YDPI7CLVR6s9NkTyFppCLN3LuaNW1PUf/view?usp=sharing",
                "archivo": "AUDIOUT.exe",
                "primario": False,
                "destacado": False,
                "pronto": False,
                "desc": "Ejecutable directo autosuficiente sin necesidad de instalación. Ideal para llevar en memoria USB o ejecutar directamente en cualquier PC.",
                "puntos": [
                    "No requiere instalación ni permisos de administrador",
                    "Listo para llevar en USB y ejecutar al instante",
                    "Cero archivos residuales en el sistema",
                ],
            },
            {
                "id": "android",
                "nombre": "AUDIOUT para Android",
                "sub": "Android 10+ (Smartphones y Tablets)",
                "badge": "🤖 En Desarrollo",
                "badge_tipo": "pronto",
                "icono": "📱",
                "url": None,
                "archivo": "Google Play",
                "primario": False,
                "destacado": False,
                "pronto": True,
                "desc": "Sincronización y duplicación remota de audio para smartphones y tablets Android. Próximamente disponible de forma oficial en Google Play Store.",
                "puntos": [
                    "Control inalámbrico de latencia desde tu móvil",
                    "Widgets interactivos para pantalla de inicio",
                    "Pronto disponible en Google Play Store",
                ],
            },
        ],
        "plataformas": ["Windows 10 / 11", "Android (Pronto)"],
        "aviso_plataforma": "La versión de AUDIOUT para Android estará disponible muy pronto.",
        "showcase": [
            {
                "id": "unisono",
                "badge": "Modo Unísono Perfecto",
                "nombre_corto": "Multi-Salida",
                "icono_corto": "📢",
                "titulo": "Multi-Salida y Sincronización al Unísono",
                "subtitulo": "Bluetooth y Monitor HDMI sonando al mismo milisegundo exacto",
                "desc": (
                    "Captura real de AUDIOUT: panel principal con selección de parlante Bluetooth Maestro, "
                    "salida secundaria (HDMI/Altavoces), ajuste milimétrico de retardo (165 ms), "
                    "medidores VU estéreo en vivo y botón de sincronización al unísono con un clic."
                ),
                "captura": "img/apps/audiout/capturas_reales/01_multi_salida_real.png",
            },
            {
                "id": "enrutador",
                "badge": "WinRT AudioPolicy",
                "nombre_corto": "Por Programa",
                "icono_corto": "🔀",
                "titulo": "Enrutador por Programa Independiente",
                "subtitulo": "Asigna salidas dedicadas y controla volúmenes por aplicación",
                "desc": (
                    "Captura real de AUDIOUT: lista interactiva de aplicaciones activas en Windows con buscador en vivo. "
                    "Asigna una salida exclusiva a Spotify, videojuegos o Chrome con controles individuales de volumen y silencio."
                ),
                "captura": "img/apps/audiout/capturas_reales/02_enrutador_programa_real.png",
            },
            {
                "id": "pestanas",
                "badge": "División de Navegador",
                "nombre_corto": "Pestañas Web",
                "icono_corto": "🌐",
                "titulo": "Separar Audio de Pestañas de Navegador",
                "subtitulo": "Enruta pestañas individuales de Chrome, Edge y Brave",
                "desc": (
                    "Captura real de AUDIOUT: guía integrada para enviar pestañas específicas (YouTube, Netflix o llamadas) "
                    "a diferentes salidas físicas de audio utilizando extensiones de navegador ligeras y gratuitas."
                ),
                "captura": "img/apps/audiout/capturas_reales/03_pestanas_navegador_real.png",
            },
            {
                "id": "ajustes",
                "badge": "Vidrio Esmerilado Acrylic",
                "nombre_corto": "Ajustes & Logos",
                "icono_corto": "⚙️",
                "titulo": "Personalización Visual & Bandeja del Sistema",
                "subtitulo": "Efecto acrílico DWM translúcido y minimizado en segundo plano",
                "desc": (
                    "Captura real de AUDIOUT: activación de fondo difuminado (Frosted Glass Acrylic), regulación de opacidad, "
                    "soporte para fondos de pantalla personalizados y opciones para minimizar a la bandeja del sistema (System Tray)."
                ),
                "captura": "img/apps/audiout/capturas_reales/04_ajustes_logos_real.png",
            },
        ],
        "novedades": [
            {
                "titulo": "Auto-Sincronización Continua e Inteligente",
                "desc": "El motor LockedDelayFIFO drena colas parásitas y converge permanentemente en 165 ms exactos, manteniendo el unísono bloqueado entre pausas o cambios de video.",
                "icono": "🔒",
            },
            {
                "titulo": "Modo Unísono Perfecto (Compensación BT)",
                "desc": "Anulación de la latencia A2DP de radiofrecuencia de parlantes Bluetooth frente a HDMI o altavoces integrados, logrando cero eco en 1 clic.",
                "icono": "🎯",
            },
            {
                "titulo": "Eliminación del Sonido Robótico (Comb Filtering)",
                "desc": "Supresión total de cancelaciones de fase acústicas destructivas y activación del reloj de 1 ms en Windows (timeBeginPeriod) para evitar buffer underruns.",
                "icono": "🎵",
            },
            {
                "titulo": "Enrutador por Programa (WinRT AudioPolicy)",
                "desc": "División de audio por procesos activos: envía Spotify al parlante, Discord a auriculares y Chrome a la pantalla con controles individuales.",
                "icono": "🔀",
            },
            {
                "titulo": "Fondo Difuminado (Frosted Glass Acrylic DWM)",
                "desc": "Efecto acrílico translúcido nativo sobre el escritorio de Windows con soporte para fondos de pantalla personalizados y regulación de opacidad.",
                "icono": "🪟",
            },
            {
                "titulo": "Minimizar a la Bandeja del Sistema (Tray)",
                "desc": "El audio continúa duplicándose en segundo plano sin ocupar espacio en la barra de tareas, con menú contextual rápido junto al reloj.",
                "icono": "🔽",
            },
        ],
        "caracteristicas": [
            {
                "emoji": "🎧",
                "titulo": "Unísono acústico entre Bluetooth y HDMI",
                "texto": "Alinea altavoces con retardos físicos dispares para lograr una experiencia estéreo envolvente sin eco ni desincronización.",
            },
            {
                "emoji": "⚡",
                "titulo": "Motor LockedDelayFIFO anti-desfase",
                "texto": "Búfer elástico que ajusta dinámicamente las muestras por segundo, impidiendo acumulaciones de retardo al cambiar de video.",
            },
            {
                "emoji": "🎛️",
                "titulo": "Enrutamiento selectivo por aplicación",
                "texto": "Elige qué programa suena por qué dispositivo físico mediante integración directa con el subsistema de audio de Windows.",
            },
            {
                "emoji": "🔬",
                "titulo": "Calibración con pulso sonoro",
                "texto": "Comprueba el unísono mediante un clic sincronizado cada 0.8s y afina con botones de micro-ajuste milisegundo a milisegundo.",
            },
            {
                "emoji": "🪟",
                "titulo": "Estética moderna translúcida",
                "texto": "Efecto de vidrio esmerilado acrílico DWM, fondos personalizados y controles visuales nítidos de alta legibilidad.",
            },
            {
                "emoji": "📦",
                "titulo": "Instalador y Versión Portable",
                "texto": "Disponible con instalador oficial que añade accesos directos o versión 100% portable lista para llevar en tu memoria USB.",
            },
            {
                "emoji": "🚀",
                "titulo": "Consumo ultraligero de recursos",
                "texto": "Motor en punto flotante WASAPI que consume apenas un 1% de CPU y ~30 MB de RAM, ideal para estar siempre activo.",
            },
            {
                "emoji": "🤖",
                "titulo": "Ecosistema móvil en camino",
                "texto": "La versión para dispositivos Android está en desarrollo activo y estará disponible muy pronto.",
            },
        ],
        "arquitectura": [
            {
                "titulo": "Motor DSP LockedDelayFIFO",
                "desc": "Búfer elástico en tiempo real que drena colas inter-hilo al instante y absorbe derivas de reloj oscilador sin alterar el tono musical.",
            },
            {
                "titulo": "WASAPI Loopback Estéreo 32-bit Float",
                "desc": "Captura y renderizado de audio digital a 48,000 Hz con latencia nativa mínima y temporizador de alta precisión de 1.0 ms (timeBeginPeriod).",
            },
            {
                "titulo": "IPolicyConfig COM & WinRT AudioPolicy",
                "desc": "Alternancia atómica en memoria del dispositivo maestro del sistema operativo y asignación de endpoints por PID sin reiniciar procesos.",
            },
            {
                "titulo": "Threading Aislado STA (sys.coinit_flags = 2)",
                "desc": "Aislamiento estricto de hilos COM de Windows para convivencia limpia y concurrente entre la interfaz gráfica, el tray y el DSP de audio.",
            },
        ],
        "cta_titulo": "Experimenta el sonido al unísono definitivo en Windows",
        "cta_desc": "Descarga AUDIOUT de forma gratuita para Windows 10 y 11. Disponible en instalador oficial con accesos directos o versión portable lista para USB.",
        "tiendas": [],
        "url_privacidad": None,
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
