/**
 * FYNEX — Experiencia Cinematográfica de Vuelo del Fénix al Scroll
 * 
 * Vincula la secuencia de 112 fotogramas fotorrealistas del Fénix 3D
 * con GSAP ScrollTrigger, adaptando trayectoria, escala, profundidad y
 * partículas incandescentes mientras vuela tras las ventanas translúcidas
 * de la página hasta alinearse con la barra inferior del pie de página.
 */
(function () {
    'use strict';

    var TOTAL_FRAMES = 112;
    var BASE_W = 1280;
    var BASE_H = 720;

    // Metadatos de cada fotograma: [centro_x, centro_y, ancho_ave, alto_ave]
    var FRAMES_META = [
        [618.1, 366.3, 439, 569], [617.8, 366.0, 439, 567], [619.2, 366.0, 439, 568], [620.2, 365.8, 439, 569],
        [621.7, 365.4, 439, 569], [622.8, 363.9, 437, 569], [627.1, 362.7, 439, 569], [630.6, 361.6, 441, 569],
        [632.0, 359.8, 443, 573], [632.4, 359.2, 447, 573], [632.9, 358.2, 449, 581], [632.8, 357.2, 461, 583],
        [632.4, 356.7, 461, 585], [633.4, 358.9, 469, 589], [632.9, 365.7, 483, 593], [630.8, 376.3, 507, 601],
        [624.5, 386.6, 537, 611], [617.8, 394.6, 569, 631], [614.3, 405.2, 595, 659], [610.0, 410.5, 607, 663],
        [604.2, 413.4, 575, 663], [610.4, 406.9, 503, 663], [612.6, 397.5, 499, 659], [634.3, 379.3, 535, 651],
        [634.3, 379.1, 535, 651], [643.9, 370.4, 605, 649], [676.1, 370.6, 545, 664], [707.1, 360.3, 524, 653],
        [744.2, 345.8, 581, 649], [744.2, 345.8, 581, 649], [748.9, 338.9, 634, 655], [750.9, 333.2, 663, 661],
        [749.2, 333.9, 660, 669], [749.1, 333.9, 661, 669], [747.2, 333.1, 664, 671], [742.4, 329.2, 659, 683],
        [729.1, 314.8, 648, 719], [729.0, 314.6, 648, 719], [719.6, 316.1, 627, 719], [707.7, 317.2, 627, 719],
        [691.9, 308.9, 674, 719], [691.7, 309.0, 674, 719], [687.1, 308.7, 700, 719], [677.5, 313.2, 734, 719],
        [646.0, 331.1, 832, 719], [646.0, 331.0, 832, 719], [632.2, 339.0, 876, 695], [599.0, 351.1, 944, 664],
        [564.5, 345.7, 974, 633], [564.4, 345.8, 974, 633], [549.6, 340.9, 990, 602], [530.0, 334.0, 1011, 505],
        [473.9, 338.0, 1037, 471], [474.0, 338.0, 1037, 472], [454.1, 343.3, 1017, 502], [429.8, 348.7, 987, 528],
        [383.9, 374.0, 933, 541], [383.4, 374.0, 933, 541], [375.1, 385.6, 923, 558], [374.7, 390.9, 873, 574],
        [397.3, 404.2, 821, 571], [397.3, 404.2, 823, 571], [419.4, 415.4, 815, 568], [440.5, 430.1, 817, 565],
        [481.4, 453.4, 915, 573], [481.5, 453.7, 914, 571], [491.1, 471.9, 941, 569], [508.0, 510.0, 957, 575],
        [627.0, 519.5, 1027, 571], [627.4, 519.6, 1027, 571], [687.2, 513.7, 1161, 565], [715.6, 509.3, 1139, 567],
        [781.4, 469.7, 1099, 624], [781.9, 469.5, 1099, 623], [799.2, 447.7, 1058, 640], [830.5, 408.1, 1027, 657],
        [860.6, 363.4, 1025, 689], [860.7, 363.4, 1025, 689], [876.3, 345.2, 1023, 683], [889.0, 320.5, 1021, 689],
        [893.5, 267.0, 1031, 701], [893.6, 266.9, 1031, 701], [889.5, 253.3, 1033, 699], [882.9, 221.0, 1019, 699],
        [880.6, 220.7, 859, 655], [880.7, 220.6, 860, 655], [874.1, 222.0, 858, 649], [873.8, 234.5, 495, 629],
        [917.3, 254.7, 517, 379], [917.5, 254.7, 517, 379], [937.3, 265.7, 562, 412], [1002.2, 277.8, 591, 599],
        [1055.9, 311.8, 587, 574], [1056.0, 312.0, 587, 574], [1055.9, 313.4, 587, 597], [1072.0, 335.2, 569, 600],
        [1102.7, 373.5, 453, 592], [1126.1, 435.7, 335, 569], [1126.1, 436.0, 335, 569], [1132.7, 471.5, 381, 549],
        [1127.5, 525.1, 443, 495], [1111.8, 569.8, 459, 404], [1112.0, 569.8, 460, 404], [1105.9, 580.2, 447, 353],
        [1096.9, 588.6, 424, 259], [1084.5, 578.7, 443, 228], [1084.4, 578.6, 443, 228], [1089.5, 570.3, 413, 246],
        [1089.1, 567.0, 400, 270], [1090.8, 565.6, 383, 285], [1090.6, 565.5, 382, 286], [1091.1, 565.7, 381, 286]
    ];

    var canvas = document.getElementById('fenixScrollCanvas');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Reducir movimiento si el usuario lo prefiere
    var prefiereReducido = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Estado de la animación
    var images = new Array(TOTAL_FRAMES);
    var imagesLoaded = new Array(TOTAL_FRAMES).fill(false);
    var lastRenderedFrame = 0;
    var currentProgress = 0;
    var targetProgress = 0;
    var currentFrameIndex = 0;
    var isCanvasReady = false;

    // Dimensiones en pantalla y densidad de píxeles
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var viewW = window.innerWidth;
    var viewH = window.innerHeight;

    // Elementos DOM para coordinación de posición
    var heroVisual = document.querySelector('.fx-hero-visual');
    var heroLogoImg = document.querySelector('.fx-hero-logo-img');
    var footerEl = document.querySelector('.fx-footer');

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
            hue: 24 + Math.random() * 26, // Rango naranja a oro cálido (24 - 50)
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

    // ── Pre-carga Inteligente de Fotogramas ──
    function obtenerUrlFrame(idx) {
        var num = String(idx + 1).padStart(3, '0');
        return '/img/fenix_scroll/f_' + num + '.webp';
    }

    function precargarSecuencia() {
        // Carga inmediata del primer fotograma para que aparezca al instante
        var f0 = new Image();
        f0.onload = function () {
            images[0] = f0;
            imagesLoaded[0] = true;
            isCanvasReady = true;
            document.body.classList.add('fx-canvas-activo');
            renderizar(0, 0);

            // Cargar en cascada prioritaria: primero hitos clave (cada 8 frames), luego el resto
            var hitos = [];
            for (var i = 1; i < TOTAL_FRAMES; i += 8) hitos.push(i);
            hitos.push(TOTAL_FRAMES - 1);

            var indiceHito = 0;
            function cargarSiguienteHito() {
                if (indiceHito >= hitos.length) {
                    cargarRestoFrames();
                    return;
                }
                var idx = hitos[indiceHito++];
                var img = new Image();
                img.onload = function () {
                    images[idx] = img;
                    imagesLoaded[idx] = true;
                    cargarSiguienteHito();
                };
                img.onerror = cargarSiguienteHito;
                img.src = obtenerUrlFrame(idx);
            }
            cargarSiguienteHito();
        };
        f0.src = obtenerUrlFrame(0);
    }

    function cargarRestoFrames() {
        var idx = 1;
        function lote() {
            var cargadosEnLote = 0;
            while (idx < TOTAL_FRAMES && cargadosEnLote < 4) {
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
                if ('requestIdleCallback' in window) {
                    window.requestIdleCallback(lote, { timeout: 250 });
                } else {
                    setTimeout(lote, 30);
                }
            }
        }
        lote();
    }

    // Obtener el fotograma más cercano disponible si el actual aún se está decodificando
    function obtenerMejorImagen(idx) {
        if (imagesLoaded[idx] && images[idx]) return images[idx];
        // Búsqueda en espiral hacia atrás y adelante
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

    // ── Cálculo Cinemático de Posición, Escala y Trayectoria ──
    function calcularTransformacionAve(progreso, frameIdx) {
        var meta = FRAMES_META[frameIdx] || [640, 360, 500, 500];
        var metaCx = meta[0];
        var metaCy = meta[1];

        var esMovil = viewW < 992;
        var ratioPantalla = viewW / viewH;

        var drawW, drawH, drawX, drawY;

        if (!esMovil) {
            // ESCRITORIO / PANTALLA ANCHA
            var baseScale = Math.max(viewW / BASE_W, viewH / BASE_H);
            drawW = BASE_W * baseScale;
            drawH = BASE_H * baseScale;
            
            // Centrado de la cámara base
            var cxDef = (viewW - drawW) * 0.5;
            var cyDef = (viewH - drawH) * 0.5;

            // En el Hero (progreso de 0.0 a 0.20): anclar armónicamente con la columna derecha
            var heroPeso = Math.max(0, 1 - (progreso / 0.18));
            var heroShiftX = 0;
            var heroShiftY = 0;

            if (heroVisual && heroPeso > 0.001) {
                var heroRect = heroVisual.getBoundingClientRect();
                var targetHeroCx = heroRect.left + heroRect.width * 0.5;
                var targetHeroCy = heroRect.top + heroRect.height * 0.5;

                // Dónde caería el ave en el fotograma 0 con la cámara base
                var birdBaseX = cxDef + metaCx * baseScale;
                var birdBaseY = cyDef + metaCy * baseScale;

                heroShiftX = (targetHeroCx - birdBaseX) * heroPeso;
                heroShiftY = (targetHeroCy - birdBaseY) * heroPeso;
            }

            // En el Footer (progreso de 0.85 a 1.0): fijar y coordinar suavemente con la barra inferior
            var footerPeso = Math.max(0, (progreso - 0.85) / 0.15);
            var footerShiftX = 0;
            var footerShiftY = 0;

            if (footerPeso > 0.001) {
                // El ave en el frame final descansa en la esquina inferior derecha
                // Aseguramos que la base del ave se alinee justo sobre la barra legal
                var birdFinalY = cyDef + metaCy * baseScale;
                var targetBottomY = viewH - 180; // Zona de confort visual sobre la barra legal
                footerShiftY = (targetBottomY - birdFinalY) * footerPeso * 0.65;
            }

            drawX = cxDef + heroShiftX + footerShiftX;
            drawY = cyDef + heroShiftY + footerShiftY;

        } else {
            // MÓVIL / PANTALLA VERTICAL
            // Ajustamos escala para que las alas nunca se salgan del ancho del dispositivo
            var maxBirdW = 1000;
            var mobileScale = Math.min((viewW * 0.94) / maxBirdW, (viewH * 0.5) / BASE_H);
            drawW = BASE_W * mobileScale;
            drawH = BASE_H * mobileScale;

            // En móvil, centrar horizontalmente respecto al centro focal del ave en cada frame
            var birdScreenX = metaCx * mobileScale;
            drawX = (viewW * 0.5) - birdScreenX;

            // Verticalmente: en Hero empieza arriba, en catálogo y estudio acompaña el tercio medio,
            // y en footer reposa en la parte inferior sobre el copyright
            var startY = (viewH * 0.28) - (metaCy * mobileScale);
            var midY = (viewH * 0.42) - (metaCy * mobileScale);
            var endY = (viewH * 0.72) - (metaCy * mobileScale);

            var currY;
            if (progreso < 0.3) {
                var p = progreso / 0.3;
                currY = startY + (midY - startY) * p;
            } else if (progreso < 0.8) {
                currY = midY;
            } else {
                var p2 = (progreso - 0.8) / 0.2;
                currY = midY + (endY - midY) * p2;
            }
            drawY = currY;
        }

        return {
            x: drawX,
            y: drawY,
            w: drawW,
            h: drawH,
            birdScreenX: drawX + metaCx * (drawW / BASE_W),
            birdScreenY: drawY + metaCy * (drawH / BASE_H)
        };
    }

    // ── Motor de Renderizado Principal ──
    var ultimoFrameRenderizado = -1;
    var ultimaPosAve = { x: viewW * 0.5, y: viewH * 0.5 };

    function renderizar(progreso, velScroll) {
        if (!isCanvasReady) return;

        // Limpiar lienzo
        ctx.clearRect(0, 0, viewW, viewH);

        // Fotograma actual según progreso del scroll
        var frameIndex = Math.min(TOTAL_FRAMES - 1, Math.max(0, Math.floor(progreso * (TOTAL_FRAMES - 1))));
        var img = obtenerMejorImagen(frameIndex);

        // Calcular trayectoria y coordenadas del ave
        var t = calcularTransformacionAve(progreso, frameIndex);

        // Detectar movimiento del ave para emitir estela de chispas ardientes
        var deltaX = t.birdScreenX - ultimaPosAve.x;
        var deltaY = t.birdScreenY - ultimaPosAve.y;
        var dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        if (dist > 3 || Math.abs(velScroll) > 0.005) {
            emitirChispasEstela(t.birdScreenX, t.birdScreenY, Math.min(dist / 12, 1.5));
        }
        ultimaPosAve.x = t.birdScreenX;
        ultimaPosAve.y = t.birdScreenY;

        // 1. Dibujar el Ave Fénix con nitidez fotorrealista y suavizado óptico
        if (img) {
            ctx.save();
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = 'high';
            ctx.drawImage(img, t.x, t.y, t.w, t.h);
            ctx.restore();
        }

        // 2. Dibujar Chispas de la Estela del Vuelo (Detrás y alrededor)
        if (chispasEstela.length > 0) {
            ctx.save();
            ctx.shadowBlur = 10;
            for (var c = chispasEstela.length - 1; c >= 0; c--) {
                var p = chispasEstela[c];
                p.x += p.vx;
                p.y += p.vy;
                p.vx *= 0.96;
                p.vy += 0.04; // Leve flotación
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

        // 3. Dibujar Cenizas e Igniciones Flotantes del Ambiente
        ctx.save();
        ctx.shadowBlur = 6;
        for (var i = 0; i < particulas.length; i++) {
            var part = particulas[i];
            part.tiempo += 0.02;
            part.x += part.vx + Math.sin(part.tiempo * part.oscilacion) * 0.45;
            part.y += part.vy;

            // Reaparecer al cruzar los límites
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

        ultimoFrameRenderizado = frameIndex;
    }

    // ── Bucle de Animación Continuo para Partículas ──
    var animando = true;
    var ultimoTiempo = performance.now();
    var velocidadScrollSuave = 0;

    function bucleAnimacion(ahora) {
        if (!animando) return;
        var dt = Math.min(32, ahora - ultimoTiempo);
        ultimoTiempo = ahora;

        // Suavizado inercial del progreso (lerp de alta precisión)
        var dif = targetProgress - currentProgress;
        currentProgress += dif * 0.14;
        velocidadScrollSuave = Math.abs(dif);

        renderizar(currentProgress, velocidadScrollSuave);
        requestAnimationFrame(bucleAnimacion);
    }

    // ── Integración con GSAP ScrollTrigger ──
    function iniciarScrollTrigger() {
        if (window.gsap && window.ScrollTrigger) {
            window.gsap.registerPlugin(window.ScrollTrigger);

            window.ScrollTrigger.create({
                trigger: document.body,
                start: "top top",
                end: "bottom bottom",
                scrub: 0.55, // Respuesta fluida y elástica al scroll
                onUpdate: function (self) {
                    targetProgress = self.progress;
                }
            });
            window.ScrollTrigger.refresh();
        } else {
            // Mecanismo de contingencia nativo si la librería externa tarda en cargar
            window.addEventListener('scroll', function () {
                var maxScroll = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
                var actual = window.pageYOffset || document.documentElement.scrollTop;
                targetProgress = Math.min(1, Math.max(0, actual / maxScroll));
            }, { passive: true });
        }
    }

    // ── Eventos y Ciclo de Vida ──
    window.addEventListener('resize', function () {
        redimensionar();
        if (window.ScrollTrigger) window.ScrollTrigger.refresh();
        renderizar(currentProgress, 0);
    });

    // Iniciar
    redimensionar();
    inicializarParticulas();
    precargarSecuencia();
    iniciarScrollTrigger();
    requestAnimationFrame(bucleAnimacion);

})();
