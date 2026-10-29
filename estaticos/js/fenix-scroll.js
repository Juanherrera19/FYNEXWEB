/**
 * FYNEX — Experiencia Cinematográfica de Vuelo del Fénix al Scroll
 * 
 * Vincula la secuencia de 112 fotogramas fotorrealistas del Fénix 3D
 * con scroll en tiempo real (avance y rebobinado hacia atrás), adaptando
 * trayectoria, escala, profundidad y partículas incandescentes mientras
 * vuela tras las ventanas translúcidas hasta alinearse con el pie de página.
 */
(function () {
    'use strict';

    var TOTAL_FRAMES = 112;
    var BASE_W = 1280;
    var BASE_H = 720;

    // Metadatos precisos de cada fotograma limpio: [centro_x, centro_y, ancho_ave, alto_ave]
    var FRAMES_META = [
        [618.8, 366.3, 439, 569], [618.5, 366.0, 439, 571], [620.2, 366.0, 439, 571], [621.7, 365.2, 439, 571],
        [624.0, 363.2, 439, 571], [627.0, 360.9, 439, 571], [630.6, 361.6, 443, 571], [632.4, 361.8, 447, 573],
        [632.7, 359.7, 451, 573], [633.0, 358.7, 453, 579], [633.5, 357.3, 459, 583], [632.9, 356.5, 471, 589],
        [632.4, 355.9, 471, 589], [633.3, 357.8, 479, 595], [633.3, 363.6, 489, 599], [632.6, 374.1, 515, 607],
        [625.9, 385.1, 545, 617], [620.3, 394.6, 577, 639], [616.3, 404.7, 605, 656], [611.7, 410.4, 617, 660],
        [604.1, 412.1, 583, 660], [612.7, 404.9, 517, 658], [613.7, 393.8, 509, 660], [634.2, 375.7, 535, 650],
        [634.2, 375.3, 539, 650], [644.2, 367.6, 609, 656], [675.5, 369.2, 547, 659], [706.8, 358.9, 525, 647],
        [744.4, 344.2, 585, 646], [744.6, 344.1, 585, 646], [749.3, 337.0, 637, 650], [751.4, 331.3, 665, 656],
        [749.8, 331.7, 663, 664], [749.8, 331.6, 663, 664], [747.7, 330.8, 665, 668], [743.0, 326.7, 661, 680],
        [728.7, 313.8, 648, 709], [728.7, 313.7, 648, 709], [718.5, 316.1, 627, 709], [707.1, 317.8, 627, 709],
        [691.7, 309.7, 674, 709], [691.7, 309.7, 674, 709], [687.0, 309.4, 699, 709], [677.6, 313.3, 734, 709],
        [646.4, 330.0, 834, 709], [646.3, 329.9, 834, 709], [633.2, 338.3, 877, 690], [599.0, 350.3, 945, 658],
        [566.5, 345.8, 977, 627], [566.2, 345.9, 977, 628], [551.2, 340.9, 991, 602], [531.9, 334.2, 1011, 504],
        [478.0, 337.5, 1032, 471], [478.0, 337.5, 1032, 471], [458.5, 342.3, 1012, 505], [434.4, 347.3, 982, 531],
        [390.7, 370.8, 930, 543], [390.2, 370.9, 930, 543], [379.8, 381.7, 918, 561], [379.1, 388.3, 873, 573],
        [400.8, 400.7, 823, 573], [400.8, 400.7, 823, 573], [420.2, 412.8, 815, 573], [439.9, 427.7, 816, 571],
        [479.5, 452.2, 915, 581], [479.5, 452.2, 914, 577], [489.4, 470.5, 939, 575], [505.7, 506.8, 963, 571],
        [618.1, 516.5, 1029, 568], [617.9, 516.4, 1031, 568], [677.2, 512.2, 1158, 564], [702.9, 508.1, 1140, 564],
        [770.0, 472.4, 1105, 617], [770.8, 472.3, 1105, 617], [791.6, 451.5, 1062, 634], [823.8, 414.1, 1033, 654],
        [855.7, 368.7, 1031, 688], [855.8, 368.7, 1031, 687], [871.5, 350.2, 1025, 689], [885.1, 325.0, 1023, 695],
        [894.0, 272.9, 1031, 698], [893.8, 272.9, 1031, 698], [890.2, 257.3, 1035, 696], [883.6, 223.2, 1021, 696],
        [882.5, 220.3, 861, 667], [882.5, 220.2, 861, 667], [876.2, 221.7, 859, 651], [874.2, 234.2, 567, 493],
        [916.6, 254.4, 519, 380], [916.7, 254.4, 519, 380], [936.3, 265.2, 565, 413], [1001.2, 277.6, 591, 511],
        [1054.3, 311.2, 589, 573], [1054.6, 311.4, 589, 573], [1054.6, 311.2, 586, 575], [1070.7, 329.0, 571, 594],
        [1102.3, 367.9, 457, 591], [1126.6, 427.3, 330, 569], [1126.6, 427.3, 330, 568], [1133.3, 463.0, 378, 549],
        [1127.9, 517.3, 438, 495], [1111.3, 562.6, 454, 405], [1111.2, 562.6, 454, 405], [1104.9, 574.7, 442, 353],
        [1095.4, 583.8, 418, 257], [1084.0, 572.9, 436, 229], [1084.0, 572.9, 437, 229], [1088.9, 563.6, 407, 245],
        [1088.3, 559.4, 395, 270], [1089.7, 557.3, 378, 286], [1089.8, 557.2, 378, 287], [1090.4, 557.5, 376, 287]
    ];

    var canvas = document.getElementById('fenixScrollCanvas');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Detectar ruta base automáticamente para compatibilidad con localhost, file:// y subdirectorios de GitHub Pages
    var baseAssetPath = (function () {
        var baseEl = document.querySelector('base[href]');
        if (baseEl && baseEl.href) return baseEl.href.replace(/\/$/, '') + '/';

        var scripts = document.getElementsByTagName('script');
        for (var i = 0; i < scripts.length; i++) {
            var src = scripts[i].src || '';
            if (src.indexOf('fenix-scroll.js') !== -1) {
                return src.substring(0, src.lastIndexOf('/js/fenix-scroll.js') + 1);
            }
        }
        var path = window.location.pathname || '';
        if (path.endsWith('.html') || path.endsWith('.htm')) {
            path = path.substring(0, path.lastIndexOf('/') + 1);
        }
        return (window.location.origin || '') + (path.endsWith('/') ? path : path + '/');
    })();

    // Reducir movimiento si el usuario lo prefiere
    var prefiereReducido = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Estado de la animación y fotogramas
    var images = new Array(TOTAL_FRAMES);
    var imagesLoaded = new Array(TOTAL_FRAMES).fill(false);
    var currentProgress = 0;
    var targetProgress = 0;
    var isCanvasReady = false;

    // Dimensiones en pantalla y densidad de píxeles
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var viewW = window.innerWidth;
    var viewH = window.innerHeight;

    // ── Sistema de Partículas (Cenizas y Chispas de Vuelo) ──
    var particulas = [];
    var NUM_PARTICULAS_AMBIENTE = 35;
    var chispasEstela = [];

    function crearParticulaAmbiente(yAleatoria) {
        return {
            x: Math.random() * viewW,
            y: yAleatoria ? Math.random() * viewH : viewH + Math.random() * 40,
            vx: (Math.random() - 0.5) * 0.7,
            vy: -(0.5 + Math.random() * 1.2),
            size: 1.2 + Math.random() * 2.8,
            alpha: 0.2 + Math.random() * 0.65,
            hue: 24 + Math.random() * 26,
            tiempo: Math.random() * 100,
            oscilacion: 0.8 + Math.random() * 1.4
        };
    }

    function inicializarParticulas() {
        particulas = [];
        for (var i = 0; i < NUM_PARTICULAS_AMBIENTE; i++) {
            particulas.push(crearParticulaAmbiente(true));
        }
    }

    function emitirChispasEstela(x, y, velocidad) {
        if (prefiereReducido) return;
        var cantidad = Math.min(4, Math.max(1, Math.floor(velocidad * 6)));
        for (var i = 0; i < cantidad; i++) {
            var angulo = Math.PI * 0.5 + (Math.random() - 0.5) * 1.2;
            var vel = 1.5 + Math.random() * 3.5;
            chispasEstela.push({
                x: x + (Math.random() - 0.5) * 60,
                y: y + (Math.random() - 0.5) * 40,
                vx: Math.cos(angulo) * vel + (Math.random() - 0.5) * 2,
                vy: -Math.sin(angulo) * vel - 1.2,
                size: 2.0 + Math.random() * 2.5,
                alpha: 0.95,
                vida: 1.0,
                degradacion: 0.02 + Math.random() * 0.035,
                color: Math.random() > 0.4 ? '#ffbe2e' : (Math.random() > 0.5 ? '#ff7a18' : '#ffffff')
            });
        }
    }

    // ── Pre-carga de Fotogramas ──
    function obtenerUrlFrame(idx) {
        var num = String(idx + 1).padStart(3, '0');
        return baseAssetPath + 'img/fenix_scroll/f_' + num + '.webp';
    }

    function precargarSecuencia() {
        // Carga inmediata del primer fotograma
        var f0 = new Image();
        f0.onload = function () {
            images[0] = f0;
            imagesLoaded[0] = true;
            isCanvasReady = true;
            document.body.classList.add('fx-canvas-activo');
            renderizar(currentProgress, 0);

            // Cargar en cascada prioritaria
            cargarRestoFrames();
        };
        f0.onerror = function () {
            console.warn('[FYNEX Fénix] Reintentando carga de f_001 desde fallback...');
            f0.src = '/img/fenix_scroll/f_001.webp';
        };
        f0.src = obtenerUrlFrame(0);
    }

    function cargarRestoFrames() {
        // Primero cargar fotogramas clave de navegación
        var hitos = [10, 25, 45, 60, 75, 90, 100, TOTAL_FRAMES - 1];
        hitos.forEach(function (h) {
            if (!imagesLoaded[h]) {
                var img = new Image();
                img.onload = function () { images[h] = img; imagesLoaded[h] = true; };
                img.src = obtenerUrlFrame(h);
            }
        });

        // Luego cargar todos los restantes en lotes continuos
        var idx = 1;
        function lote() {
            var cargadosEnLote = 0;
            while (idx < TOTAL_FRAMES && cargadosEnLote < 6) {
                if (!imagesLoaded[idx]) {
                    (function (i) {
                        var img = new Image();
                        img.onload = function () {
                            images[i] = img;
                            imagesLoaded[i] = true;
                        };
                        img.src = obtenerUrlFrame(i);
                    })(idx);
                    cargadosEnLote++;
                }
                idx++;
            }
            if (idx < TOTAL_FRAMES) {
                setTimeout(lote, 25);
            }
        }
        lote();
    }

    // Obtener la mejor imagen disponible (rebobina o avanza sin dejar huecos negros)
    function obtenerMejorImagen(idx) {
        if (imagesLoaded[idx] && images[idx]) return images[idx];
        for (var offset = 1; offset < TOTAL_FRAMES; offset++) {
            var anterior = idx - offset;
            if (anterior >= 0 && imagesLoaded[anterior] && images[anterior]) return images[anterior];
            var posterior = idx + offset;
            if (posterior < TOTAL_FRAMES && imagesLoaded[posterior] && images[posterior]) return images[posterior];
        }
        return images[0];
    }

    // ── Dimensionado y Adaptabilidad del Lienzo ──
    function redimensionar() {
        viewW = window.innerWidth;
        viewH = window.innerHeight;
        dpr = Math.min(window.devicePixelRatio || 1, 2);

        canvas.width = Math.round(viewW * dpr);
        canvas.height = Math.round(viewH * dpr);
        canvas.style.width = viewW + 'px';
        canvas.style.height = viewH + 'px';

        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.scale(dpr, dpr);
    }

    // ── Detección de Geometría del Logo del Hero para Alineación Perfecta ──
    function obtenerGeometriaHero(esMovil) {
        var el = document.querySelector('.fx-hero-logo-img') || document.querySelector('.fx-hero-logo-frame');
        if (el) {
            var r = el.getBoundingClientRect();
            if (r.width > 20 && r.height > 20) {
                var scrollTop = window.pageYOffset || document.documentElement.scrollTop || 0;
                var absCx = r.left + r.width * 0.462;
                var absCy = (r.top + scrollTop) + r.height * 0.498;
                var birdH = r.height * 0.982;
                var scale = birdH / 569;
                return {
                    x: absCx,
                    y: absCy - scrollTop,
                    scale: scale,
                    valido: true
                };
            }
        }
        if (!esMovil) {
            var fScale = Math.min((viewW * 0.92) / 1050, (viewH * 0.88) / BASE_H);
            return {
                x: Math.min(viewW - 220, viewW * 0.5 + Math.min(viewW, 1200) * 0.24),
                y: Math.min(viewH * 0.50, 420),
                scale: fScale,
                valido: false
            };
        } else {
            var mScale = Math.min((viewW * 0.95) / 950, (viewH * 0.52) / BASE_H);
            return {
                x: viewW * 0.5,
                y: viewH * 0.26,
                scale: mScale,
                valido: false
            };
        }
    }

    // ── Cálculo Cinemático de Posición, Escala y Trayectoria ──
    function calcularTransformacionAve(progreso, frameIdx) {
        var meta = FRAMES_META[frameIdx] || [640, 360, 500, 500];
        var metaCx = meta[0];
        var metaCy = meta[1];

        var esMovil = viewW < 860;
        var heroGeo = obtenerGeometriaHero(esMovil);

        var drawW, drawH, drawX, drawY, birdScreenX, birdScreenY, currentScale;

        if (!esMovil) {
            // ESCRITORIO — Trayectoria Cinematográfica Visible y Coordinada
            var desktopScale = Math.min((viewW * 0.92) / 1050, (viewH * 0.88) / BASE_H);

            var heroTargetX = heroGeo.x;
            var heroTargetY = heroGeo.y;
            var heroScale = heroGeo.scale;

            var catTargetX = viewW * 0.44;
            var catTargetY = viewH * 0.52;

            var estTargetX = viewW * 0.62;
            var estTargetY = viewH * 0.42;

            var footTargetX = viewW - Math.min(320, viewW * 0.22);
            var footTargetY = viewH - 170;
            var footScale = Math.min(desktopScale * 1.05, (viewH * 0.55) / 569);

            if (progreso < 0.25) {
                var p = progreso / 0.25;
                birdScreenX = heroTargetX + (catTargetX - heroTargetX) * p;
                birdScreenY = heroTargetY + (catTargetY - heroTargetY) * p;
                currentScale = heroScale + (desktopScale - heroScale) * p;
            } else if (progreso < 0.65) {
                var p2 = (progreso - 0.25) / 0.40;
                birdScreenX = catTargetX + (estTargetX - catTargetX) * p2;
                birdScreenY = catTargetY + (estTargetY - catTargetY) * p2;
                currentScale = desktopScale;
            } else {
                var p3 = (progreso - 0.65) / 0.35;
                birdScreenX = estTargetX + (footTargetX - estTargetX) * p3;
                birdScreenY = estTargetY + (footTargetY - estTargetY) * p3;
                currentScale = desktopScale + (footScale - desktopScale) * p3;
            }

            drawW = BASE_W * currentScale;
            drawH = BASE_H * currentScale;
            drawX = birdScreenX - metaCx * currentScale;
            drawY = birdScreenY - metaCy * currentScale;

        } else {
            // MÓVIL / PANTALLA VERTICAL
            var mobileScale = Math.min((viewW * 0.95) / 950, (viewH * 0.52) / BASE_H);
            var mHeroScale = heroGeo.scale || mobileScale;

            var startX = heroGeo.x;
            var startY = heroGeo.y;
            var midX = viewW * 0.5;
            var midY = (viewH * 0.40);
            var endX = viewW * 0.5;
            var endY = (viewH * 0.70);

            if (progreso < 0.25) {
                var pm = progreso / 0.25;
                birdScreenX = startX + (midX - startX) * pm;
                birdScreenY = startY + (midY - startY) * pm;
                currentScale = mHeroScale + (mobileScale - mHeroScale) * pm;
            } else if (progreso < 0.80) {
                birdScreenX = midX;
                birdScreenY = midY;
                currentScale = mobileScale;
            } else {
                var pm2 = (progreso - 0.80) / 0.20;
                birdScreenX = midX + (endX - midX) * pm2;
                birdScreenY = midY + (endY - midY) * pm2;
                currentScale = mobileScale;
            }

            drawW = BASE_W * currentScale;
            drawH = BASE_H * currentScale;
            drawX = birdScreenX - metaCx * currentScale;
            drawY = birdScreenY - metaCy * currentScale;
        }

        return {
            x: drawX,
            y: drawY,
            w: drawW,
            h: drawH,
            birdScreenX: birdScreenX,
            birdScreenY: birdScreenY
        };
    }

    // ── Motor de Renderizado Principal ──
    var ultimaPosAve = { x: viewW * 0.5, y: viewH * 0.5 };

    function renderizar(progreso, velScroll) {
        if (!isCanvasReady) return;

        ctx.clearRect(0, 0, viewW, viewH);

        // Control dinámico de crossfade entre el logo animado del Hero y el lienzo de scroll
        var heroPicture = document.querySelector('.fx-hero-logo-frame picture') || document.querySelector('.fx-hero-logo-img');
        var birdAlpha = 1.0;

        if (heroPicture) {
            if (progreso <= 0.02) {
                heroPicture.style.opacity = '1';
                birdAlpha = 0; // Al inicio en el Hero se mantiene la animación estática aleteando
            } else if (progreso < 0.10) {
                var cross = (progreso - 0.02) / (0.10 - 0.02);
                heroPicture.style.opacity = (1 - cross).toFixed(3);
                birdAlpha = cross;
            } else {
                heroPicture.style.opacity = '0';
                birdAlpha = 1.0;
            }
        }

        // Fotograma actual según progreso del scroll (avanza hacia adelante o rebobina hacia atrás)
        var frameIndex = Math.min(TOTAL_FRAMES - 1, Math.max(0, Math.round(progreso * (TOTAL_FRAMES - 1))));
        var img = obtenerMejorImagen(frameIndex);

        var t = calcularTransformacionAve(progreso, frameIndex);

        // Detectar movimiento para estela de chispas
        var deltaX = t.birdScreenX - ultimaPosAve.x;
        var deltaY = t.birdScreenY - ultimaPosAve.y;
        var dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        if (dist > 3 || Math.abs(velScroll) > 0.004) {
            emitirChispasEstela(t.birdScreenX, t.birdScreenY, Math.min(dist / 10, 1.6));
        }
        ultimaPosAve.x = t.birdScreenX;
        ultimaPosAve.y = t.birdScreenY;

        // 1. Dibujar el Fénix en su pose actual
        if (img && birdAlpha > 0.005) {
            ctx.save();
            ctx.globalAlpha = birdAlpha;
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = 'high';
            ctx.drawImage(img, t.x, t.y, t.w, t.h);
            ctx.restore();
        }

        // 2. Chispas de la estela de vuelo
        if (chispasEstela.length > 0) {
            ctx.save();
            ctx.shadowBlur = 10;
            for (var c = chispasEstela.length - 1; c >= 0; c--) {
                var p = chispasEstela[c];
                p.x += p.vx;
                p.y += p.vy;
                p.vx *= 0.96;
                p.vy += 0.04;
                p.vida -= p.degradacion;

                if (p.vida <= 0) {
                    chispasEstela.splice(c, 1);
                    continue;
                }

                ctx.shadowColor = p.color;
                ctx.fillStyle = p.color;
                ctx.globalAlpha = Math.max(0, p.vida * p.alpha);
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size * p.vida, 0, Math.PI * 2);
                ctx.fill();
            }
            ctx.restore();
        }

        // 3. Cenizas incandescentes de fondo
        ctx.save();
        ctx.shadowBlur = 6;
        for (var i = 0; i < particulas.length; i++) {
            var part = particulas[i];
            part.tiempo += 0.02;
            part.x += part.vx + Math.sin(part.tiempo * part.oscilacion) * 0.45;
            part.y += part.vy;

            if (part.y < -20) {
                part.y = viewH + 20;
                part.x = Math.random() * viewW;
            }
            if (part.x < -30) part.x = viewW + 30;
            if (part.x > viewW + 30) part.x = -30;

            var alphaP = part.alpha * (0.8 + 0.2 * Math.sin(part.tiempo * 3));
            ctx.shadowColor = 'hsla(' + part.hue + ', 100%, 55%, ' + alphaP + ')';
            ctx.fillStyle = 'hsla(' + part.hue + ', 95%, 60%, ' + alphaP + ')';
            ctx.globalAlpha = alphaP;

            ctx.beginPath();
            ctx.arc(part.x, part.y, part.size, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.restore();
    }

    // ── Bucle de Animación Continuo con Rebobinado Suave ──
    var animando = true;
    var ultimoTiempo = performance.now();
    var velocidadScrollSuave = 0;

    function bucleAnimacion(ahora) {
        if (!animando) return;
        var dt = Math.min(32, ahora - ultimoTiempo);
        ultimoTiempo = ahora;

        // Suavizado inercial bidireccional (avanza al bajar, rebobina al subir)
        var dif = targetProgress - currentProgress;
        currentProgress += dif * 0.20;
        if (targetProgress === 0 && currentProgress < 0.02) {
            currentProgress = 0;
        } else if (targetProgress === 1 && currentProgress > 0.98) {
            currentProgress = 1;
        } else if (Math.abs(dif) < 0.001) {
            currentProgress = targetProgress;
        }
        velocidadScrollSuave = Math.abs(dif);

        renderizar(currentProgress, velocidadScrollSuave);
        requestAnimationFrame(bucleAnimacion);
    }

    // ── Cálculo Preciso de Progreso de Scroll en Cualquier Navegador ──
    function calcularProgresoScroll() {
        var doc = document.documentElement;
        var body = document.body;
        var maxScroll = Math.max(
            1,
            (doc.scrollHeight || 0) - window.innerHeight,
            (body.scrollHeight || 0) - window.innerHeight
        );
        var scrollTop = window.pageYOffset || doc.scrollTop || body.scrollTop || 0;
        return Math.min(1, Math.max(0, scrollTop / maxScroll));
    }

    function actualizarScroll() {
        targetProgress = calcularProgresoScroll();
    }

    // ── Integración Dual: Scroll Nativo + GSAP ScrollTrigger ──
    function iniciarControladoresScroll() {
        // 1. Escucha nativa permanente: garantiza respuesta instantánea y rebobinado reversible
        window.addEventListener('scroll', actualizarScroll, { passive: true });
        window.addEventListener('wheel', actualizarScroll, { passive: true });
        window.addEventListener('touchmove', actualizarScroll, { passive: true });

        // 2. Si GSAP ScrollTrigger está disponible, vincularlo también
        if (window.gsap && window.ScrollTrigger) {
            window.gsap.registerPlugin(window.ScrollTrigger);

            window.ScrollTrigger.create({
                start: 0,
                end: "max",
                onUpdate: function (self) {
                    targetProgress = self.progress;
                }
            });
        }

        actualizarScroll();
    }

    // ── Eventos de Redimensionamiento ──
    window.addEventListener('resize', function () {
        redimensionar();
        actualizarScroll();
        if (window.ScrollTrigger) window.ScrollTrigger.refresh();
        renderizar(currentProgress, 0);
    });

    // Iniciar sistema
    redimensionar();
    inicializarParticulas();
    precargarSecuencia();
    iniciarControladoresScroll();
    requestAnimationFrame(bucleAnimacion);

})();
