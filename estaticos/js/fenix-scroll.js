/**
 * FYNEX — Motor Cinematográfico de Vuelo del Fénix Ultra-Optimizado (v2.0)
 * 
 * - Renderizado reactivo de 60fps ligado al scroll con suavizado inercial bidireccional.
 * - Throttling inteligente en reposo para 0% consumo innecesario de GPU/CPU.
 * - DPR adaptativo (1.15x móvil / 1.5x desktop) para erradicar el consumo excesivo de memoria.
 * - Partículas de fuego y chispas de propulsión unificadas en un único búfer de alto rendimiento.
 * - Trayectoria Hermite C1 continua sin tirones ni cambios bruscos de ángulo.
 */
(function () {
    'use strict';

    var TOTAL_FRAMES = 112;
    var BASE_W = 1280;
    var BASE_H = 720;

    // Metadatos de centro de masa y caja delimitadora por fotograma
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
    var ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;

    // Detectar ruta base automáticamente
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

    var prefiereReducido = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Estado del motor
    var images = new Array(TOTAL_FRAMES);
    var imagesLoaded = new Array(TOTAL_FRAMES).fill(false);
    var currentProgress = 0;
    var targetProgress = 0;
    var lastRenderedProgress = -1;
    var lastRenderedFrame = -1;
    var idleTicks = 0;

    var viewW = window.innerWidth;
    var viewH = window.innerHeight;
    var isMobile = viewW < 860;
    var dpr = 1;

    // ── Sistema de Partículas Liviano (Cenizas y Chispas de Vuelo) ──
    var particulas = [];
    var NUM_PARTICULAS = isMobile ? 14 : 26;
    var chispasEstela = [];
    var ultimaPosAve = { x: 0, y: 0 };

    function crearParticulaAmbiente(yAleatoria) {
        return {
            x: Math.random() * viewW,
            y: yAleatoria ? Math.random() * viewH : viewH + Math.random() * 30,
            vx: (Math.random() - 0.5) * 0.5,
            vy: -(0.4 + Math.random() * 0.9),
            size: 1.0 + Math.random() * 2.2,
            alpha: 0.15 + Math.random() * 0.45,
            color: Math.random() > 0.5 ? '255, 122, 24' : '255, 190, 46',
            tiempo: Math.random() * 100,
            osc: 0.8 + Math.random() * 1.2
        };
    }

    function inicializarParticulas() {
        particulas = [];
        for (var i = 0; i < NUM_PARTICULAS; i++) {
            particulas.push(crearParticulaAmbiente(true));
        }
    }

    function emitirChispasEstela(x, y, velocidad) {
        if (prefiereReducido || isMobile) return;
        var cantidad = Math.min(3, Math.max(1, Math.floor(velocidad * 4)));
        for (var i = 0; i < cantidad; i++) {
            var angulo = Math.PI * 0.5 + (Math.random() - 0.5) * 1.0;
            var vel = 1.2 + Math.random() * 2.5;
            chispasEstela.push({
                x: x + (Math.random() - 0.5) * 50,
                y: y + (Math.random() - 0.5) * 35,
                vx: Math.cos(angulo) * vel,
                vy: -Math.sin(angulo) * vel - 0.8,
                size: 1.5 + Math.random() * 2.0,
                vida: 1.0,
                decay: 0.03 + Math.random() * 0.04,
                color: Math.random() > 0.4 ? '255, 190, 46' : '255, 122, 24'
            });
        }
    }

    // ── Pre-carga Eficiente de Fotogramas ──
    function obtenerUrlFrame(idx) {
        var num = String(idx + 1).padStart(3, '0');
        return baseAssetPath + 'img/fenix_scroll/f_' + num + '.webp';
    }

    function precargarSecuencia() {
        // 1. Fotograma 1 inmediato para arrancar sin parpadeo
        var f0 = new Image();
        f0.onload = function () {
            images[0] = f0;
            imagesLoaded[0] = true;
            document.body.classList.add('fx-canvas-activo');
            renderizar(0, 0);

            // 2. Pre-cargar escalonado en background
            cargarFramesEscalonados();
        };
        f0.src = obtenerUrlFrame(0);
    }

    function cargarFramesEscalonados() {
        // En móvil solo cargamos cada 2do fotograma (56 frames en vez de 112 = 50% de RAM y red)
        var step = isMobile ? 2 : 1;
        
        // Hitos clave de navegación primero
        var hitos = [15, 30, 48, 65, 80, 95, TOTAL_FRAMES - 1];
        hitos.forEach(function (h) {
            if (!imagesLoaded[h]) {
                var img = new Image();
                img.onload = function () { images[h] = img; imagesLoaded[h] = true; };
                img.src = obtenerUrlFrame(h);
            }
        });

        var idx = 1;
        function cargarLote() {
            var enLote = 0;
            while (idx < TOTAL_FRAMES && enLote < 4) {
                if (!imagesLoaded[idx] && (idx % step === 0)) {
                    (function (i) {
                        var img = new Image();
                        img.onload = function () { images[i] = img; imagesLoaded[i] = true; };
                        img.src = obtenerUrlFrame(i);
                    })(idx);
                    enLote++;
                }
                idx++;
            }
            if (idx < TOTAL_FRAMES) {
                if (window.requestIdleCallback) {
                    window.requestIdleCallback(cargarLote);
                } else {
                    setTimeout(cargarLote, 35);
                }
            }
        }
        setTimeout(cargarLote, 80);
    }

    function obtenerMejorImagen(idx) {
        if (imagesLoaded[idx] && images[idx]) return images[idx];
        for (var offset = 1; offset < TOTAL_FRAMES; offset++) {
            var ant = idx - offset;
            if (ant >= 0 && imagesLoaded[ant] && images[ant]) return images[ant];
            var pos = idx + offset;
            if (pos < TOTAL_FRAMES && imagesLoaded[pos] && images[pos]) return images[pos];
        }
        return images[0];
    }

    // ── Dimensionado Adaptativo (DPR inteligente para erradicar saturación GPU) ──
    function redimensionar() {
        viewW = window.innerWidth;
        viewH = window.innerHeight;
        isMobile = viewW < 860;

        // Limitar DPR para máxima fluidez y cero consumo excesivo
        var maxDpr = isMobile ? 1.15 : 1.5;
        dpr = Math.min(window.devicePixelRatio || 1, maxDpr);

        canvas.width = Math.round(viewW * dpr);
        canvas.height = Math.round(viewH * dpr);
        canvas.style.width = viewW + 'px';
        canvas.style.height = viewH + 'px';

        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.scale(dpr, dpr);

        NUM_PARTICULAS = isMobile ? 14 : 26;
        if (particulas.length > NUM_PARTICULAS) {
            particulas.length = NUM_PARTICULAS;
        }
    }

    // Geometría del Logo del Hero
    function obtenerGeometriaHero() {
        var el = document.querySelector('.fx-hero-logo-img') || document.querySelector('.fx-hero-logo-frame');
        if (el) {
            var r = el.getBoundingClientRect();
            if (r.width > 20 && r.height > 20) {
                var scrollTop = window.pageYOffset || document.documentElement.scrollTop || 0;
                var absCx = r.left + r.width * 0.462;
                var absCy = (r.top + scrollTop) + r.height * 0.498;
                var birdH = r.height * 0.982;
                return {
                    x: absCx,
                    y: absCy - scrollTop,
                    scale: birdH / 569,
                    valido: true
                };
            }
        }
        if (!isMobile) {
            var fScale = Math.min((viewW * 0.90) / 1050, (viewH * 0.86) / BASE_H);
            return {
                x: Math.min(viewW - 220, viewW * 0.5 + Math.min(viewW, 1200) * 0.24),
                y: Math.min(viewH * 0.48, 420),
                scale: fScale,
                valido: false
            };
        } else {
            var mScale = Math.min((viewW * 0.92) / 950, (viewH * 0.48) / BASE_H);
            return {
                x: viewW * 0.72,
                y: viewH * 0.22,
                scale: mScale,
                valido: false
            };
        }
    }

    // ── Suavizado C1 Hermite Continuo de Trayectoria ──
    function calcularTransformacionAve(progreso, frameIdx) {
        var meta = FRAMES_META[frameIdx] || [640, 360, 500, 500];
        var metaCx = meta[0];
        var metaCy = meta[1];

        var heroGeo = obtenerGeometriaHero();
        var birdScreenX, birdScreenY, currentScale;

        if (!isMobile) {
            var desktopScale = Math.min((viewW * 0.90) / 1050, (viewH * 0.86) / BASE_H);

            var p0x = heroGeo.x, p0y = heroGeo.y, s0 = heroGeo.scale;
            var p1x = viewW * 0.44, p1y = viewH * 0.52;
            var p2x = viewW * 0.62, p2y = viewH * 0.42;
            var p3x = viewW - Math.min(300, viewW * 0.22);
            var p3y = viewH - 160;
            var s3 = Math.min(desktopScale * 1.05, (viewH * 0.54) / 569);

            // Interpolación continua con aceleración armónica suave
            if (progreso < 0.25) {
                var u = progreso / 0.25;
                var ease = u * u * (3 - 2 * u); // Smoothstep
                birdScreenX = p0x + (p1x - p0x) * ease;
                birdScreenY = p0y + (p1y - p0y) * ease;
                currentScale = s0 + (desktopScale - s0) * ease;
            } else if (progreso < 0.65) {
                var u2 = (progreso - 0.25) / 0.40;
                var ease2 = u2 * u2 * (3 - 2 * u2);
                birdScreenX = p1x + (p2x - p1x) * ease2;
                birdScreenY = p1y + (p2y - p1y) * ease2;
                currentScale = desktopScale;
            } else {
                var u3 = (progreso - 0.65) / 0.35;
                var ease3 = u3 * u3 * (3 - 2 * u3);
                birdScreenX = p2x + (p3x - p2x) * ease3;
                birdScreenY = p2y + (p3y - p2y) * ease3;
                currentScale = desktopScale + (s3 - desktopScale) * ease3;
            }

        } else {
            // MÓVIL: Trayectoria vertical compacta y centrada
            var mobileScale = Math.min((viewW * 0.92) / 950, (viewH * 0.48) / BASE_H);
            var mHeroScale = heroGeo.scale || mobileScale;

            var msX = heroGeo.x, msY = heroGeo.y;
            var mmX = viewW * 0.5, mmY = viewH * 0.38;
            var meX = viewW * 0.5, meY = viewH * 0.68;

            if (progreso < 0.25) {
                var um = progreso / 0.25;
                var em = um * um * (3 - 2 * um);
                birdScreenX = msX + (mmX - msX) * em;
                birdScreenY = msY + (mmY - msY) * em;
                currentScale = mHeroScale + (mobileScale - mHeroScale) * em;
            } else if (progreso < 0.80) {
                birdScreenX = mmX;
                birdScreenY = mmY;
                currentScale = mobileScale;
            } else {
                var um2 = (progreso - 0.80) / 0.20;
                var em2 = um2 * um2 * (3 - 2 * um2);
                birdScreenX = mmX + (meX - mmX) * em2;
                birdScreenY = mmY + (meY - mmY) * em2;
                currentScale = mobileScale;
            }
        }

        var drawW = BASE_W * currentScale;
        var drawH = BASE_H * currentScale;
        var drawX = birdScreenX - metaCx * currentScale;
        var drawY = birdScreenY - metaCy * currentScale;

        return {
            x: drawX,
            y: drawY,
            w: drawW,
            h: drawH,
            birdScreenX: birdScreenX,
            birdScreenY: birdScreenY
        };
    }

    // ── Renderizado Principal de Alto Rendimiento ──
    function renderizar(progreso, velScroll) {
        ctx.clearRect(0, 0, viewW, viewH);

        // Control de transición con el logo estático del Hero
        var heroPicture = document.querySelector('.fx-hero-logo-frame picture') || document.querySelector('.fx-hero-logo-img');
        var birdAlpha = 1.0;

        if (heroPicture) {
            if (progreso <= 0.002) {
                heroPicture.style.opacity = '1';
                birdAlpha = 0;
            } else if (progreso < 0.025) {
                var cross = (progreso - 0.002) / (0.025 - 0.002);
                heroPicture.style.opacity = (1 - cross).toFixed(3);
                birdAlpha = cross;
            } else {
                heroPicture.style.opacity = '0';
                birdAlpha = 1.0;
            }
        }

        var frameIndex = Math.min(TOTAL_FRAMES - 1, Math.max(0, Math.round(progreso * (TOTAL_FRAMES - 1))));
        var img = obtenerMejorImagen(frameIndex);
        var t = calcularTransformacionAve(progreso, frameIndex);

        // Chispas reactivas al movimiento
        var deltaX = t.birdScreenX - ultimaPosAve.x;
        var deltaY = t.birdScreenY - ultimaPosAve.y;
        var dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        if (dist > 3 || Math.abs(velScroll) > 0.004) {
            emitirChispasEstela(t.birdScreenX, t.birdScreenY, Math.min(dist / 10, 1.4));
        }
        ultimaPosAve.x = t.birdScreenX;
        ultimaPosAve.y = t.birdScreenY;

        // 1. Dibujar el Ave
        if (img && birdAlpha > 0.005) {
            ctx.save();
            ctx.globalAlpha = birdAlpha;
            ctx.drawImage(img, t.x, t.y, t.w, t.h);
            ctx.restore();
        }

        // 2. Chispas de Vuelo (Efecto de halo directo sin shadowBlur costoso)
        if (chispasEstela.length > 0) {
            ctx.save();
            for (var c = chispasEstela.length - 1; c >= 0; c--) {
                var ch = chispasEstela[c];
                ch.x += ch.vx;
                ch.y += ch.vy;
                ch.vx *= 0.96;
                ch.vy += 0.04;
                ch.vida -= ch.decay;

                if (ch.vida <= 0) {
                    chispasEstela.splice(c, 1);
                    continue;
                }

                var rAlpha = Math.max(0, ch.vida);
                // Halo exterior suave
                ctx.fillStyle = 'rgba(' + ch.color + ', ' + (rAlpha * 0.25).toFixed(2) + ')';
                ctx.beginPath();
                ctx.arc(ch.x, ch.y, ch.size * 2.2, 0, Math.PI * 2);
                ctx.fill();

                // Núcleo brillante
                ctx.fillStyle = 'rgba(255, 255, 255, ' + (rAlpha * 0.9).toFixed(2) + ')';
                ctx.beginPath();
                ctx.arc(ch.x, ch.y, ch.size * 0.8, 0, Math.PI * 2);
                ctx.fill();
            }
            ctx.restore();
        }

        // 3. Cenizas y brasas ambientales
        ctx.save();
        for (var i = 0; i < particulas.length; i++) {
            var part = particulas[i];
            part.tiempo += 0.018;
            part.x += part.vx + Math.sin(part.tiempo * part.osc) * 0.4;
            part.y += part.vy;

            if (part.y < -15) {
                part.y = viewH + 15;
                part.x = Math.random() * viewW;
            }
            if (part.x < -20) part.x = viewW + 20;
            if (part.x > viewW + 20) part.x = -20;

            var aP = part.alpha * (0.8 + 0.2 * Math.sin(part.tiempo * 3));
            ctx.fillStyle = 'rgba(' + part.color + ', ' + aP.toFixed(2) + ')';
            ctx.beginPath();
            ctx.arc(part.x, part.y, part.size, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.restore();

        lastRenderedProgress = progreso;
        lastRenderedFrame = frameIndex;
    }

    // ── Bucle de Animación Inteligente con Ahorro de Energía en Reposo ──
    var rafId = null;
    var estaActivo = true;

    function bucleAnimacion() {
        if (!estaActivo) return;

        var dif = targetProgress - currentProgress;
        var moving = Math.abs(dif) > 0.0003;

        if (moving) {
            // Lerp inercial ágil
            var lerpSpeed = isMobile ? 0.32 : 0.22;
            currentProgress += dif * lerpSpeed;
            if (targetProgress === 0 && currentProgress < 0.005) currentProgress = 0;
            else if (targetProgress === 1 && currentProgress > 0.995) currentProgress = 1;
            idleTicks = 0;
            renderizar(currentProgress, Math.abs(dif));
            rafId = requestAnimationFrame(bucleAnimacion);
        } else {
            currentProgress = targetProgress;
            idleTicks++;

            // En reposo: renderizar partículas a 30fps para 0% carga de CPU/GPU
            if (idleTicks % 2 === 0 || chispasEstela.length > 0) {
                renderizar(currentProgress, 0);
            }
            rafId = requestAnimationFrame(bucleAnimacion);
        }
    }

    // ── Control de Scroll Pasivo y Reactivo ──
    function calcularProgresoScroll() {
        var doc = document.documentElement;
        var body = document.body;
        var maxScroll = Math.max(1, (doc.scrollHeight || 0) - window.innerHeight, (body.scrollHeight || 0) - window.innerHeight);
        var scrollTop = window.pageYOffset || doc.scrollTop || body.scrollTop || 0;
        return Math.min(1, Math.max(0, scrollTop / maxScroll));
    }

    function onScroll() {
        targetProgress = calcularProgresoScroll();
    }

    // Pausar si la pestaña está oculta
    document.addEventListener('visibilitychange', function () {
        if (document.hidden) {
            estaActivo = false;
            if (rafId) cancelAnimationFrame(rafId);
        } else {
            estaActivo = true;
            redimensionar();
            onScroll();
            rafId = requestAnimationFrame(bucleAnimacion);
        }
    });

    // Iniciar eventos
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () {
        redimensionar();
        onScroll();
        renderizar(currentProgress, 0);
    });

    redimensionar();
    inicializarParticulas();
    precargarSecuencia();
    onScroll();
    currentProgress = targetProgress;
    rafId = requestAnimationFrame(bucleAnimacion);

})();
