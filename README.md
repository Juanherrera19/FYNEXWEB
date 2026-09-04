# FYNEX — Sitio corporativo

Sitio público de FYNEX: quiénes somos y el catálogo de nuestras apps y juegos.

FYNEX es la desarrolladora. Cada producto (Debts Goodbye y los que vengan) tiene su
propio repositorio y su propio subdominio; este sitio solo los presenta y enlaza.

```
www.fynexhq.com   este sitio (catálogo)
dgb.fynexhq.com   Debts Goodbye (repositorio aparte)
```

## Por qué es estático

No hay servidor ni base de datos: `build.py` genera archivos HTML y cualquier hosting
estático los sirve al instante.

Esto importa por una razón concreta: la página más pública del negocio no debe depender
de un servicio que se duerme. Alojada en Cloudflare Pages o Netlify no tiene arranque
en frío, es gratis y no hay nada que mantener.

## Estructura

```
build.py                 Genera dist/ a partir del catálogo y las plantillas
contenido/catalogo.py    Los productos. Única fuente de verdad
plantillas/home.html     Portada
plantillas/app.html      Página de detalle de un producto
estaticos/               CSS e imágenes, se copian tal cual
dist/                    Salida generada. No se versiona
```

## Uso

```bash
python build.py            # genera dist/
python build.py --servir   # genera y levanta http://127.0.0.1:8080 para revisarlo
```

No hay dependencias: solo Python 3.8 o superior de la biblioteca estándar.

## Agregar un producto al catálogo

Añade una entrada en `contenido/catalogo.py` y vuelve a generar. No hay que tocar
plantillas ni estilos.

```python
{
    "slug": "mi-app",                       # define la URL: /apps/mi-app/
    "nombre": "Mi App",
    "url_propia": "https://mia.fynexhq.com",  # None si aún no tiene sitio
    "estado": "publicada",                  # o "proximamente"
    "destacada": False,                     # solo un producto puede encabezar
    "tipo": "app",                          # o "juego"
    "categoria": "Productividad",
    "tagline": "Una frase que diga qué hace.",
    "descripcion_corta": "Va en la tarjeta del catálogo.",
    "descripcion_larga": "Párrafo de la página de detalle. Vacío la omite.",
    "icono": "img/apps/mi-app.png",         # ruta dentro de estaticos/
    "color": "#3b82f6",
    "caracteristicas": [
        {"emoji": "⚡", "titulo": "Rápida", "texto": "Explica el beneficio."},
    ],
    "tiendas": [
        {"nombre": "Google Play", "url": "https://play.google.com/...", "icono": "▶"},
    ],
    "plataformas": ["Android", "Web"],
    "url_privacidad": "https://mia.fynexhq.com/privacy-policy",
}
```

El icono va en `estaticos/img/apps/`. Un producto en `"proximamente"` aparece atenuado
en el catálogo y no genera página de detalle.

## Despliegue

El sitio son archivos estáticos, así que sirve cualquier hosting. Configuración:

- **Comando de build**: `python build.py`
- **Directorio de salida**: `dist`

### Cloudflare Pages o Netlify

Conecta el repositorio y usa esos dos valores. El despliegue se dispara solo con cada
push. Ambos sirven `404.html` automáticamente para rutas inexistentes.

### GitHub Pages

Necesita una acción que ejecute el build y publique `dist/`, porque `dist/` no se
versiona.

### DNS

En el proveedor del dominio:

```
fynexhq.com       ->  este sitio
www.fynexhq.com   ->  este sitio
dgb.fynexhq.com   ->  el servicio de Debts Goodbye
```

## Marca

El logo es el fénix, y es exclusivo de FYNEX como desarrolladora. **No se usa dentro
de las apps**: cada producto conserva su propia identidad. Las cadenas y los signos de
peso pertenecen solo a Debts Goodbye.

```
estaticos/img/fynex-logo-original.png   1024px, el archivo maestro
estaticos/img/fynex-logo.png             320px, para usos grandes
estaticos/img/fynex-logo-sm.png           96px, cabecera y favicon
```

Para reemplazar el logo, sustituye el original y regenera los otros dos tamaños:

```python
from PIL import Image
src = Image.open('estaticos/img/fynex-logo-original.png').convert('RGBA')
for nombre, lado in [('fynex-logo-sm.png', 96), ('fynex-logo.png', 320)]:
    src.resize((lado, lado), Image.LANCZOS).save('estaticos/img/' + nombre, optimize=True)
```

Los colores del sitio salen del logo y viven en `estaticos/fynex.css`, en las variables
`--fx-acento` (naranja) y `--fx-acento-2` (dorado).

## Notas

- Todo texto que sale del catálogo se escapa antes de insertarse en la página. Hoy el
  catálogo lo escribimos nosotros, pero así el día que venga de otra fuente ya está
  preparado.
- Si una plantilla queda con un marcador `{{...}}` sin valor, el build falla a
  propósito: es mejor verlo al generar que descubrirlo en producción.
- El sitio genera `robots.txt` y `sitemap.xml` automáticamente a partir del catálogo.
- Las animaciones se anulan bajo `prefers-reduced-motion`.
