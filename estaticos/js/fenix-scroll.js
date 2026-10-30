/**
 * FYNEX — Motor Cinematográfico de Vuelo del Fénix Ultra-Optimizado (v2.2)
 * 
 * - Renderizado reactivo a 60-120fps con suavizado inercial adaptativo y cero lag.
 * - Decodificación asíncrona fuera del hilo principal (img.decode()) para erradicar el jank.
 * - Priorización dinámica de fotogramas según velocidad y posición del scroll.
 * - Caching estricto de elementos DOM y cálculos geométricos (cero layout thrashing).
 * - Iluminación adaptativa: halo radial GPU + contorno ígneo con optimización en vuelo rápido.
 * - Bucle autónomo de 22 frames al llegar al reposo final, alineado al subpíxel.
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
    var idleTicks = 0;

    // ── Secuencia de Animación Fija Final (Bucle Autónomo de 22 Fotogramas) ──
    var TOTAL_IDLE_FRAMES = 22;
    var idleImages = new Array(TOTAL_IDLE_FRAMES);
    var idleImagesLoaded = new Array(TOTAL_IDLE_FRAMES).fill(false);
    var idleAnimIndex = 0;
    var lastIdleTime = 0;
    var IDLE_FRAME_INTERVAL = 42; // ~24fps animación fluida cinematográfica
    var idleCargandoIniciado = false;

    var viewW = window.innerWidth;
    var viewH = window.innerHeight;
    var isMobile = viewW < 860;
    var dpr = 1;

    // Referencias DOM y caché de geometría (erradica reflows en cada frame)
    var heroPictureEl = null;
    var scrollIndicatorEl = null;
    var cachedHeroGeo = { x: 0, absY: 0, scale: 1, valido: false };
    var cachedMaxScroll = 1;

    // ── Sistema de Partículas Liviano (Cenizas y Chispas de Vuelo) ──
    var particulas = [];
    var NUM_PARTICULAS = isMobile ? 12 : 22;
    var chispasEstela = [];
    var ultimaPosAve = { x: 0, y: 0 };

    function crearParticulaAmbiente(yAleatoria) {
        return {
            x: Math.random() * viewW,
            y: yAleatoria ? Math.random() * viewH : viewH + Math.random() * 30,
            vx: (Math.random() - 0.5) * 0.4,
            vy: -(0.3 + Math.random() * 0.8),
            size: 1.0 + Math.random() * 2.0,
            alpha: 0.15 + Math.random() * 0.40,
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
        var cantidad = Math.min(2, Math.max(1, Math.floor(velocidad * 3)));
        for (var i = 0; i < cantidad; i++) {
            var angulo = Math.PI * 0.5 + (Math.random() - 0.5) * 0.8;
            var vel = 1.2 + Math.random() * 2.2;
            chispasEstela.push({
                x: x + (Math.random() - 0.5) * 40,
                y: y + (Math.random() - 0.5) * 30,
                vx: Math.cos(angulo) * vel,
                vy: -Math.sin(angulo) * vel - 0.6,
                size: 1.2 + Math.random() * 1.8,
                vida: 1.0,
                decay: 0.04 + Math.random() * 0.04,
                color: Math.random() > 0.4 ? '255, 190, 46' : '255, 122, 24'
            });
        }
    }

    // ── Carga y Decodificación Asíncrona (Off-Thread) ──
    function obtenerUrlFrame(idx) {
        var num = String(idx + 1).padStart(3, '0');
        return baseAssetPath + 'img/fenix_scroll/f_' + num + '.webp';
    }

    function cargarFrameIndividual(i, callback) {
        if (imagesLoaded[i]) {
            if (callback) callback();
            return;
        }
        if (images[i]) return; // ya encolado

        var img = new Image();
        images[i] = img;
        img.onload = function () {
            if (img.decode) {
                img.decode().then(function () {
                    imagesLoaded[i] = true;
                    if (callback) callback();
                }).catch(function () {
                    imagesLoaded[i] = true;
                    if (callback) callback();
                });
            } else {
                imagesLoaded[i] = true;
                if (callback) callback();
            }
        };
        img.src = obtenerUrlFrame(i);
    }

    function priorizarFramesCercanos(targetFrame) {
        for (var off = 0; off <= 4; off++) {
            var fa = targetFrame - off;
            var fb = targetFrame + off;
            if (fa >= 0 && !imagesLoaded[fa]) cargarFrameIndividual(fa);
            if (fb < TOTAL_FRAMES && !imagesLoaded[fb]) cargarFrameIndividual(fb);
        }
    }

    function precargarSecuencia() {
        // 1. Fotograma 1 inmediato
        cargarFrameIndividual(0, function () {
            document.body.classList.add('fx-canvas-activo');
            renderizar(0, 0);

            // 2. Pre-cargar hitos uniformes distribuidos por todo el sitio (cada 5 frames)
            for (var h = 5; h < TOTAL_FRAMES; h += 5) {
                cargarFrameIndividual(h);
            }
            cargarFrameIndividual(TOTAL_FRAMES - 1);

            // 3. Pre-cargar los fotogramas intermedios de forma escalonada
            var idx = 1;
            function cargarRestantes() {
                var lote = 0;
                while (idx < TOTAL_FRAMES && lote < 8) {
                    if (!imagesLoaded[idx] && !images[idx]) {
                        cargarFrameIndividual(idx);
                        lote++;
                    }
                    idx++;
                }
                if (idx < TOTAL_FRAMES) {
                    setTimeout(cargarRestantes, 15);
                } else {
                    setTimeout(precargarFramesIdle, 100);
                }
            }
            setTimeout(cargarRestantes, 25);
        });
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

    // ── Pre-carga y Selección de Fotogramas del Bucle Fijo Final ──
    function obtenerUrlIdleFrame(idx) {
        var num = String(idx + 1).padStart(2, '0');
        return baseAssetPath + 'img/fenix_scroll/final_' + num + '.webp';
    }

    function precargarFramesIdle() {
        if (idleCargandoIniciado) return;
        idleCargandoIniciado = true;
        for (var i = 0; i < TOTAL_IDLE_FRAMES; i++) {
            (function (index) {
                var img = new Image();
                img.onload = function () {
                    if (img.decode) {
                        img.decode().then(function () {
                            idleImages[index] = img;
                            idleImagesLoaded[index] = true;
                        }).catch(function () {
                            idleImages[index] = img;
                            idleImagesLoaded[index] = true;
                        });
                    } else {
                        idleImages[index] = img;
                        idleImagesLoaded[index] = true;
                    }
                };
                img.src = obtenerUrlIdleFrame(index);
            })(i);
        }
    }

    function obtenerMejorImagenIdle(idx) {
        if (idleImagesLoaded[idx] && idleImages[idx]) return idleImages[idx];
        for (var offset = 1; offset < TOTAL_IDLE_FRAMES; offset++) {
            var ant = (idx - offset + TOTAL_IDLE_FRAMES) % TOTAL_IDLE_FRAMES;
            if (idleImagesLoaded[ant] && idleImages[ant]) return idleImages[ant];
            var pos = (idx + offset) % TOTAL_IDLE_FRAMES;
            if (idleImagesLoaded[pos] && idleImages[pos]) return idleImages[pos];
        }
        return images[TOTAL_FRAMES - 1] || images[0];
    }

    // ── Dimensionado y Caching Geométrico (Cero layout thrashing en RAF) ──
    function actualizarGeometriaHero() {
        heroPictureEl = document.querySelector('.fx-hero-logo-frame picture') || document.querySelector('.fx-hero-logo-img');
        scrollIndicatorEl = document.getElementById('heroScrollIndicator');

        var el = document.querySelector('.fx-hero-logo-img') || document.querySelector('.fx-hero-logo-frame');
        if (el) {
            var r = el.getBoundingClientRect();
            if (r.width > 20 && r.height > 20) {
                var scrollTop = window.pageYOffset || document.documentElement.scrollTop || 0;
                var absCx = r.left + r.width * 0.462;
                var absCy = (r.top + scrollTop) + r.height * 0.498;
                var birdH = r.height * 0.982;
                cachedHeroGeo = {
                    x: absCx,
                    absY: absCy,
                    scale: birdH / 569,
                    valido: true
                };
                return;
            }
        }
        if (!isMobile) {
            var fScale = Math.min((viewW * 0.90) / 1050, (viewH * 0.86) / BASE_H);
            cachedHeroGeo = {
                x: Math.min(viewW - 220, viewW * 0.5 + Math.min(viewW, 1200) * 0.24),
                absY: Math.min(viewH * 0.48, 420),
                scale: fScale,
                valido: false
            };
        } else {
            var mScale = Math.min((viewW * 0.92) / 950, (viewH * 0.48) / BASE_H);
            cachedHeroGeo = {
                x: viewW * 0.72,
                absY: viewH * 0.22,
                scale: mScale,
                valido: false
            };
        }
    }

    function redimensionar() {
        viewW = window.innerWidth;
        viewH = window.innerHeight;
        isMobile = viewW < 860;

        // Limitar DPR para máxima fluidez y cero saturación de memoria
        var maxDpr = isMobile ? 1.15 : 1.35;
        dpr = Math.min(window.devicePixelRatio || 1, maxDpr);

        canvas.width = Math.round(viewW * dpr);
        canvas.height = Math.round(viewH * dpr);
        canvas.style.width = viewW + 'px';
        canvas.style.height = viewH + 'px';

        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.scale(dpr, dpr);

        NUM_PARTICULAS = isMobile ? 12 : 22;
        if (particulas.length > NUM_PARTICULAS) {
            particulas.length = NUM_PARTICULAS;
        }

        var doc = document.documentElement;
        var body = document.body;
        cachedMaxScroll = Math.max(1, (doc.scrollHeight || 0) - viewH, (body.scrollHeight || 0) - viewH);

        actualizarGeometriaHero();
    }

    // ── Cálculo Cinemático de Posición y Escala (Solo Matemáticas, 0ms DOM) ──
    function calcularTransformacionAve(progreso, frameIdx) {
        var meta = FRAMES_META[frameIdx] || [640, 360, 500, 500];
        var metaCx = meta[0];
        var metaCy = meta[1];

        var scrollTop = window.pageYOffset || document.documentElement.scrollTop || 0;
        var heroTargetX = cachedHeroGeo.x;
        var heroTargetY = cachedHeroGeo.absY - scrollTop;
        var heroScale = cachedHeroGeo.scale;

        var birdScreenX, birdScreenY, currentScale;

        if (!isMobile) {
            var desktopScale = Math.min((viewW * 0.92) / 1050, (viewH * 0.88) / BASE_H);

            // Catálogo: ¡CENTRAL!
            var catTargetX = viewW * 0.50;
            var catTargetY = viewH * 0.50;

            // Estudio / Principios
            var estTargetX = viewW * 0.52;
            var estTargetY = viewH * 0.44;

            // Pie de página
            var footTargetX = viewW - Math.min(320, viewW * 0.22);
            var footTargetY = viewH - 170;
            var footScale = Math.min(desktopScale * 1.05, (viewH * 0.55) / 569);

            if (progreso < 0.26) {
                var p = progreso / 0.26;
                birdScreenX = heroTargetX + (catTargetX - heroTargetX) * p;
                birdScreenY = heroTargetY + (catTargetY - heroTargetY) * p;
                currentScale = heroScale + (desktopScale - heroScale) * p;
            } else if (progreso < 0.65) {
                var p2 = (progreso - 0.26) / 0.39;
                birdScreenX = catTargetX + (estTargetX - catTargetX) * p2;
                birdScreenY = catTargetY + (estTargetY - catTargetY) * p2;
                currentScale = desktopScale;
            } else {
                var p3 = (progreso - 0.65) / 0.35;
                birdScreenX = estTargetX + (footTargetX - estTargetX) * p3;
                birdScreenY = estTargetY + (footTargetY - estTargetY) * p3;
                currentScale = desktopScale + (footScale - desktopScale) * p3;
            }

        } else {
            // MÓVIL: Trayectoria vertical compacta y centrada
            var mobileScale = Math.min((viewW * 0.95) / 950, (viewH * 0.50) / BASE_H);
            var mHeroScale = heroScale || mobileScale;

            var msX = heroTargetX, msY = heroTargetY;
            var mmX = viewW * 0.50, mmY = viewH * 0.40;
            var meX = viewW * 0.50, meY = viewH * 0.70;

            if (progreso < 0.26) {
                var pm = progreso / 0.26;
                birdScreenX = msX + (mmX - msX) * pm;
                birdScreenY = msY + (mmY - msY) * pm;
                currentScale = mHeroScale + (mobileScale - mHeroScale) * pm;
            } else if (progreso < 0.75) {
                birdScreenX = mmX;
                birdScreenY = mmY;
                currentScale = mobileScale;
            } else {
                var pm2 = (progreso - 0.75) / 0.25;
                birdScreenX = mmX + (meX - mmX) * pm2;
                birdScreenY = mmY + (meY - mmY) * pm2;
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

    // ── Renderizado Principal de 60-120 FPS ──
    function renderizar(progreso, velScroll) {
        ctx.clearRect(0, 0, viewW, viewH);

        // Control de transición con el logo estático del Hero e indicador Desliza (usando referencias cacheadas)
        var birdAlpha = 1.0;

        if (scrollIndicatorEl) {
            if (progreso > 0.04) {
                if (!scrollIndicatorEl.classList.contains('oculto')) {
                    scrollIndicatorEl.classList.add('oculto');
                }
            } else {
                if (scrollIndicatorEl.classList.contains('oculto')) {
                    scrollIndicatorEl.classList.remove('oculto');
                }
            }
        }

        if (heroPictureEl) {
            if (progreso <= 0.006) {
                heroPictureEl.style.opacity = '1';
                birdAlpha = 0;
            } else if (progreso < 0.045) {
                var cross = (progreso - 0.006) / (0.045 - 0.006);
                heroPictureEl.style.opacity = (1 - cross).toFixed(3);
                birdAlpha = cross;
            } else {
                heroPictureEl.style.opacity = '0';
                birdAlpha = 1.0;
            }
        }

        var esFinal = progreso >= 0.985;
        var frameIndex = Math.min(TOTAL_FRAMES - 1, Math.max(0, Math.round(progreso * (TOTAL_FRAMES - 1))));
        var img;

        if (esFinal) {
            var ahora = performance.now();
            if (ahora - lastIdleTime >= IDLE_FRAME_INTERVAL) {
                idleAnimIndex = (idleAnimIndex + 1) % TOTAL_IDLE_FRAMES;
                lastIdleTime = ahora;
            }
            img = obtenerMejorImagenIdle(idleAnimIndex);
        } else {
            img = obtenerMejorImagen(frameIndex);
            idleAnimIndex = 0;
            lastIdleTime = 0;
        }

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

        var esMovimientoRapido = Math.abs(velScroll) > 0.008;

        // 1. Halo y Estela de Fuego Radiante (Gradiente radial GPU fluido)
        if (img && birdAlpha > 0.005) {
            ctx.save();
            var glowRadius = Math.max(t.w, t.h) * 0.44;
            var auraGrad = ctx.createRadialGradient(
                t.birdScreenX, t.birdScreenY, glowRadius * 0.12,
                t.birdScreenX, t.birdScreenY, glowRadius
            );
            auraGrad.addColorStop(0, 'rgba(230, 81, 0, ' + (0.35 * birdAlpha) + ')');
            auraGrad.addColorStop(0.40, 'rgba(245, 124, 0, ' + (0.18 * birdAlpha) + ')');
            auraGrad.addColorStop(0.75, 'rgba(255, 112, 67, ' + (0.06 * birdAlpha) + ')');
            auraGrad.addColorStop(1, 'rgba(255, 50, 0, 0)');

            ctx.fillStyle = auraGrad;
            ctx.beginPath();
            ctx.arc(t.birdScreenX, t.birdScreenY, glowRadius, 0, Math.PI * 2);
            ctx.fill();

            // Dibujo nítido del Fénix con contorno ígneo optimizado:
            // Si el desplazamiento es rápido, se suprime shadowBlur para garantizar 60-120 FPS sin saturar la GPU.
            if (!esMovimientoRapido) {
                ctx.shadowColor = 'rgba(255, 120, 20, ' + (0.65 * birdAlpha).toFixed(3) + ')';
                ctx.shadowBlur = isMobile ? 8 : 12;
            }
            ctx.globalAlpha = birdAlpha;
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = esMovimientoRapido ? 'medium' : 'high';
            ctx.drawImage(img, t.x, t.y, t.w, t.h);
            ctx.restore();
        }

        // 2. Chispas de Vuelo reactivas
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
                ctx.fillStyle = 'rgba(' + ch.color + ', ' + (rAlpha * 0.25).toFixed(2) + ')';
                ctx.beginPath();
                ctx.arc(ch.x, ch.y, ch.size * 2.0, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = 'rgba(255, 255, 255, ' + (rAlpha * 0.85).toFixed(2) + ')';
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
            part.tiempo += 0.02;
            part.x += part.vx + Math.sin(part.tiempo * part.osc) * 0.35;
            part.y += part.vy;

            if (part.y < -20 || part.x < -20 || part.x > viewW + 20) {
                particulas[i] = crearParticulaAmbiente(false);
                continue;
            }

            ctx.fillStyle = 'rgba(' + part.color + ', ' + part.alpha.toFixed(2) + ')';
            ctx.beginPath();
            ctx.arc(part.x, part.y, part.size, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.restore();
    }

    // ── Bucle de Animación Ultra-Fluido ──
    var rafId = null;
    var estaActivo = true;

    function bucleAnimacion() {
        if (!estaActivo) return;

        var dif = targetProgress - currentProgress;
        var absDif = Math.abs(dif);
        var moving = absDif > 0.0001;

        if (moving) {
            // Aceleración reactiva proporcional:
            // Cuanto más rápido se desplaza el usuario, más inmediata es la respuesta (0 lag)
            var lerpSpeed;
            if (absDif > 0.08) {
                lerpSpeed = 0.92;
            } else if (absDif > 0.03) {
                lerpSpeed = 0.75;
            } else if (absDif > 0.01) {
                lerpSpeed = 0.58;
            } else {
                lerpSpeed = isMobile ? 0.44 : 0.48;
            }

            currentProgress += dif * lerpSpeed;
            if (Math.abs(targetProgress - currentProgress) < 0.0003) {
                currentProgress = targetProgress;
            }

            idleTicks = 0;
            renderizar(currentProgress, absDif);
            rafId = requestAnimationFrame(bucleAnimacion);
        } else {
            currentProgress = targetProgress;
            idleTicks++;

            // En reposo: renderizar continuo si está en animación final fija, o a 30fps para chispas/cenizas
            var esFinal = currentProgress >= 0.985;
            if (esFinal || idleTicks % 2 === 0 || chispasEstela.length > 0) {
                renderizar(currentProgress, 0);
            }
            rafId = requestAnimationFrame(bucleAnimacion);
        }
    }

    // ── Control de Scroll Pasivo y Reactivo ──
    function calcularProgresoScroll() {
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
        return Math.min(1, Math.max(0, scrollTop / cachedMaxScroll));
    }

    function onScroll() {
        targetProgress = calcularProgresoScroll();
        var targetFrame = Math.min(TOTAL_FRAMES - 1, Math.max(0, Math.round(targetProgress * (TOTAL_FRAMES - 1))));
        priorizarFramesCercanos(targetFrame);

        if (targetProgress > 0.35 && !idleCargandoIniciado) {
            precargarFramesIdle();
        }
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

    // Iniciar eventos nativos optimizados
    function iniciarControladoresScroll() {
        window.addEventListener('scroll', onScroll, { passive: true });
        window.addEventListener('wheel', onScroll, { passive: true });
        window.addEventListener('touchmove', onScroll, { passive: true });

        if (window.gsap && window.ScrollTrigger) {
            window.gsap.registerPlugin(window.ScrollTrigger);
            window.ScrollTrigger.create({
                start: 0,
                end: "max",
                onUpdate: function (self) {
                    targetProgress = self.progress;
                    var tFrame = Math.min(TOTAL_FRAMES - 1, Math.max(0, Math.round(targetProgress * (TOTAL_FRAMES - 1))));
                    priorizarFramesCercanos(tFrame);
                }
            });
        }

        onScroll();
    }

    window.addEventListener('resize', function () {
        redimensionar();
        onScroll();
        renderizar(currentProgress, 0);
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            redimensionar();
            actualizarGeometriaHero();
        });
    }

    redimensionar();
    inicializarParticulas();
    precargarSecuencia();
    iniciarControladoresScroll();
    currentProgress = targetProgress;
    rafId = requestAnimationFrame(bucleAnimacion);

})();
