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
        [617.8, 366.5, 441, 569], [617.9, 366.3, 440, 569], [618.1, 366.0, 440, 568], [618.4, 365.8, 440, 569],
        [618.5, 365.7, 440, 568], [618.6, 365.4, 439, 571], [619.1, 365.4, 439, 569], [619.5, 365.2, 439, 569],
        [620.0, 364.9, 437, 569], [620.6, 364.3, 437, 570], [621.6, 363.7, 437, 569], [622.4, 363.7, 439, 571],
        [621.9, 363.0, 439, 573], [621.6, 365.2, 445, 574], [621.0, 371.0, 463, 578], [619.3, 379.8, 491, 587],
        [615.3, 388.8, 527, 602], [611.1, 396.4, 558, 619], [608.7, 404.9, 587, 648], [608.1, 410.1, 595, 656],
        [605.6, 416.1, 565, 653], [609.7, 408.7, 488, 657], [612.6, 397.4, 484, 654], [637.1, 379.2, 526, 643],
        [637.1, 379.3, 527, 643], [645.4, 369.2, 602, 636], [675.3, 368.1, 548, 661], [706.9, 357.4, 525, 650],
        [744.1, 343.3, 581, 646], [744.3, 343.1, 582, 646], [749.1, 336.0, 636, 650], [751.7, 330.1, 663, 656],
        [749.5, 330.5, 663, 664], [749.5, 330.3, 663, 664], [747.9, 330.0, 665, 668], [742.9, 325.6, 661, 679],
        [728.3, 313.5, 651, 709], [728.3, 313.4, 650, 709], [718.2, 315.8, 629, 709], [706.8, 317.7, 628, 709],
        [691.1, 309.6, 676, 709], [691.0, 309.4, 676, 709], [686.1, 308.8, 702, 709], [675.8, 312.4, 736, 709],
        [643.2, 328.8, 835, 709], [643.2, 328.7, 835, 709], [630.3, 337.5, 878, 691], [597.1, 350.1, 944, 660],
        [563.2, 345.3, 976, 629], [563.1, 345.3, 976, 630], [548.9, 341.3, 991, 606], [527.6, 334.9, 1012, 510],
        [474.1, 340.3, 1032, 474], [474.1, 340.3, 1032, 474], [454.0, 346.4, 1013, 504], [428.2, 353.2, 984, 531],
        [377.3, 379.4, 928, 543], [377.2, 379.4, 928, 543], [368.9, 392.4, 918, 560], [366.5, 401.0, 874, 576],
        [390.4, 413.5, 821, 573], [390.6, 413.6, 822, 573], [417.4, 424.7, 816, 569], [445.2, 438.2, 815, 564],
        [490.8, 455.3, 917, 553], [491.0, 455.2, 917, 553], [502.6, 473.0, 944, 553], [525.1, 518.2, 953, 557],
        [660.0, 525.7, 1027, 556], [660.2, 525.6, 1027, 556], [722.5, 516.0, 1156, 554], [750.6, 507.3, 1132, 563],
        [808.2, 460.3, 1085, 617], [808.4, 460.2, 1085, 617], [819.2, 437.0, 1050, 635], [850.4, 395.0, 1018, 651],
        [875.3, 352.4, 1019, 686], [875.4, 352.3, 1019, 687], [884.5, 337.8, 1019, 681], [894.0, 314.2, 1020, 691],
        [894.3, 266.2, 1030, 695], [894.3, 266.2, 1030, 695], [887.1, 253.8, 1035, 695], [882.1, 221.0, 1019, 693],
        [878.4, 219.0, 861, 665], [878.4, 219.0, 861, 665], [873.1, 222.0, 858, 650], [874.1, 237.7, 570, 495],
        [916.7, 254.5, 518, 381], [916.9, 254.6, 518, 382], [936.3, 265.5, 564, 412], [998.7, 278.4, 592, 506],
        [1054.2, 311.0, 588, 577], [1054.4, 311.1, 589, 576], [1054.5, 310.9, 588, 576], [1069.3, 328.8, 573, 595],
        [1101.2, 367.4, 457, 593], [1125.8, 428.4, 331, 571], [1125.9, 428.3, 331, 571], [1132.1, 463.2, 378, 551],
        [1126.8, 518.5, 438, 498], [1110.7, 563.7, 455, 408], [1110.7, 563.6, 456, 408], [1104.3, 575.5, 443, 355],
        [1095.7, 584.4, 420, 255], [1082.9, 573.2, 439, 231], [1082.8, 573.2, 439, 231], [1088.3, 564.6, 409, 247],
        [1087.5, 559.8, 397, 272], [1089.8, 557.6, 378, 289], [1089.8, 557.5, 378, 289], [1090.2, 557.6, 378, 290]
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
                x: viewW * 0.72,
                y: viewH * 0.22,
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

        // Control dinámico de transición rápida entre el logo animado del Hero y el vuelo del lienzo
        var heroPicture = document.querySelector('.fx-hero-logo-frame picture') || document.querySelector('.fx-hero-logo-img');
        var birdAlpha = 1.0;

        if (heroPicture) {
            if (progreso <= 0.002) {
                heroPicture.style.opacity = '1';
                birdAlpha = 0; // Al inicio en el Hero se mantiene la animación estática aleteando en reposo
            } else if (progreso < 0.025) {
                var cross = (progreso - 0.002) / (0.025 - 0.002);
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

        // Suavizado inercial bidireccional ágil y reactivo (avanza al bajar, rebobina al subir)
        var dif = targetProgress - currentProgress;
        currentProgress += dif * 0.45;
        if (targetProgress === 0 && currentProgress < 0.008) {
            currentProgress = 0;
        } else if (targetProgress === 1 && currentProgress > 0.992) {
            currentProgress = 1;
        } else if (Math.abs(dif) < 0.0005) {
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
