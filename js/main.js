/* =========================================================
   Cleeno Reinigungen – main.js

   1.  Konfiguration
   2.  Mobile-Navigation
   3.  Sticky-Header und Scroll-Fortschritt
   4.  Einblenden beim Scrollen
   5.  Zahlen hochzählen
   6.  Reiter (Leistungsumfang)
   7.  Vorher/Nachher-Vergleich
   8.  Sprungnavigation mit aktivem Abschnitt
   9.  Jahreszahl und Vorbelegung aus der URL
   10. Checkliste mit gespeichertem Fortschritt
   11. Offertformular
   ========================================================= */
(function () {
  'use strict';

  document.documentElement.classList.add('js');

  var reduceMotion = window.matchMedia
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. Konfiguration ----------
     FORM_ENDPOINT: URL eines Formular-Dienstes (z. B. Formspree, Getform, eigene
     PHP-/Serverless-Funktion). Solange der Wert leer ist, öffnet das Formular
     stattdessen das E-Mail-Programm mit vorausgefüllter Nachricht.
     Details siehe README.md.                                                */
  var FORM_ENDPOINT = '';
  var FALLBACK_MAIL = 'offerte@cleeno-reinigungen.ch';

  /* ---------- 2. Mobile-Navigation ---------- */
  var toggle = document.querySelector('.nav__toggle');
  var drawer = document.getElementById('mobile-nav');

  if (toggle && drawer) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      drawer.classList.toggle('is-open', !open);
    });

    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        toggle.setAttribute('aria-expanded', 'false');
        drawer.classList.remove('is-open');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
        toggle.setAttribute('aria-expanded', 'false');
        drawer.classList.remove('is-open');
        toggle.focus();
      }
    });
  }

  /* ---------- 3. Sticky-Header und Scroll-Fortschritt ---------- */
  var header = document.querySelector('.site-header');
  var progressBar = document.querySelector('.progress__bar');

  if (header || progressBar) {
    var ticking = false;
    var onScroll = function () {
      if (ticking) { return; }
      ticking = true;
      window.requestAnimationFrame(function () {
        var y = window.scrollY || document.documentElement.scrollTop;
        if (header) { header.classList.toggle('is-stuck', y > 8); }
        if (progressBar) {
          var max = document.documentElement.scrollHeight - window.innerHeight;
          progressBar.style.width = (max > 0 ? Math.min(100, (y / max) * 100) : 0) + '%';
        }
        ticking = false;
      });
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
  }

  /* ---------- 4. Einblenden beim Scrollen ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if (reveals.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
      reveals.forEach(function (el) { io.observe(el); });
    } else {
      reveals.forEach(function (el) { el.classList.add('is-visible'); });
    }
  }

  /* ---------- 5. Zahlen hochzählen ---------- */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    var runCount = function (el) {
      var target = parseFloat(el.getAttribute('data-count'));
      var suffix = el.getAttribute('data-suffix') || '';
      if (reduceMotion) { el.textContent = target + suffix; return; }
      var duration = 900;
      var started = null;
      var step = function (now) {
        if (started === null) { started = now; }
        var p = Math.min(1, (now - started) / duration);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased) + suffix;
        if (p < 1) { window.requestAnimationFrame(step); }
      };
      window.requestAnimationFrame(step);
    };

    if ('IntersectionObserver' in window) {
      var countObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            runCount(entry.target);
            countObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.5 });
      counters.forEach(function (el) { countObserver.observe(el); });
    } else {
      counters.forEach(runCount);
    }
  }

  /* ---------- 6. Reiter ---------- */
  document.querySelectorAll('[data-tabs]').forEach(function (wrapper) {
    var tabs = Array.prototype.slice.call(wrapper.querySelectorAll('[role="tab"]'));
    if (!tabs.length) { return; }

    var select = function (tab, focus) {
      tabs.forEach(function (t) {
        var active = t === tab;
        t.setAttribute('aria-selected', String(active));
        t.tabIndex = active ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) { panel.hidden = !active; }
      });
      if (focus) { tab.focus(); }
    };

    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { select(tab); });
      tab.addEventListener('keydown', function (e) {
        var next = null;
        if (e.key === 'ArrowRight') { next = tabs[(i + 1) % tabs.length]; }
        if (e.key === 'ArrowLeft') { next = tabs[(i - 1 + tabs.length) % tabs.length]; }
        if (e.key === 'Home') { next = tabs[0]; }
        if (e.key === 'End') { next = tabs[tabs.length - 1]; }
        if (next) { e.preventDefault(); select(next, true); }
      });
    });

    select(tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0] || tabs[0]);
  });

  /* ---------- 7. Vorher/Nachher-Vergleich ---------- */
  document.querySelectorAll('.ba').forEach(function (ba) {
    var range = ba.querySelector('input[type="range"]');
    if (!range) { return; }
    var apply = function () { ba.style.setProperty('--split', range.value + '%'); };
    range.addEventListener('input', apply);
    apply();

    // Erst beim Sichtbarwerden einmal aufziehen – zeigt, dass man schieben kann.
    if (!reduceMotion && 'IntersectionObserver' in window) {
      var teaser = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) { return; }
          teaser.unobserve(entry.target);
          var from = 84, to = 50, start = null;
          range.value = from; apply();
          var step = function (now) {
            if (start === null) { start = now; }
            var p = Math.min(1, (now - start) / 900);
            var eased = 1 - Math.pow(1 - p, 3);
            range.value = from + (to - from) * eased;
            apply();
            if (p < 1) { window.requestAnimationFrame(step); }
          };
          window.setTimeout(function () { window.requestAnimationFrame(step); }, 250);
        });
      }, { threshold: 0.4 });
      teaser.observe(ba);
    }
  });

  /* ---------- 8. Sprungnavigation mit aktivem Abschnitt ---------- */
  document.querySelectorAll('.subnav').forEach(function (subnav) {
    if (!('IntersectionObserver' in window)) { return; }
    var links = Array.prototype.slice.call(subnav.querySelectorAll('a[href^="#"]'));
    var targets = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); })
                       .filter(Boolean);
    if (!targets.length) { return; }

    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        links.forEach(function (a) {
          a.setAttribute('aria-current', String(a.getAttribute('href') === '#' + entry.target.id));
        });
      });
    }, { rootMargin: '-140px 0px -65% 0px' });
    targets.forEach(function (t) { spy.observe(t); });
  });

  /* ---------- 9. Jahreszahl und Vorbelegung aus der URL ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  // Verlinkungen wie kontakt.html?leistung=bueroreinigung&objekt=84%20m%C2%B2
  var params = new URLSearchParams(window.location.search);
  ['leistung', 'objekt', 'termin', 'nachricht'].forEach(function (name) {
    var value = params.get(name);
    var field = document.getElementById(name);
    if (!value || !field) { return; }
    if (field.tagName === 'SELECT') {
      Array.prototype.forEach.call(field.options, function (opt) {
        if (opt.value === value) { field.value = value; }
      });
    } else {
      field.value = value;
    }
  });

  /* ---------- 10. Checkliste mit gespeichertem Fortschritt ---------- */
  var checkliste = document.querySelector('[data-checkliste]');
  if (checkliste) {
    var kaesten = Array.prototype.slice.call(checkliste.querySelectorAll('input[type="checkbox"]'));
    var meter = document.querySelector('.cl__meter span');
    var zaehler = document.querySelector('.cl__count');
    var speicher = 'cleeno-checkliste';

    var lesen = function () {
      try { return JSON.parse(window.localStorage.getItem(speicher)) || {}; }
      catch (e) { return {}; }
    };
    var schreiben = function (daten) {
      try { window.localStorage.setItem(speicher, JSON.stringify(daten)); } catch (e) { /* privater Modus */ }
    };

    var aktualisieren = function () {
      var erledigt = kaesten.filter(function (k) { return k.checked; }).length;
      if (meter) { meter.style.width = (erledigt / kaesten.length * 100) + '%'; }
      if (zaehler) { zaehler.textContent = erledigt + ' von ' + kaesten.length + ' erledigt'; }
    };

    var gespeichert = lesen();
    kaesten.forEach(function (k) { if (gespeichert[k.id]) { k.checked = true; } });
    aktualisieren();

    checkliste.addEventListener('change', function (e) {
      if (e.target.type !== 'checkbox') { return; }
      var daten = lesen();
      if (e.target.checked) { daten[e.target.id] = 1; } else { delete daten[e.target.id]; }
      schreiben(daten);
      aktualisieren();
    });

    var zuruecksetzen = document.getElementById('cl-reset');
    if (zuruecksetzen) {
      zuruecksetzen.addEventListener('click', function () {
        kaesten.forEach(function (k) { k.checked = false; });
        schreiben({});
        aktualisieren();
      });
    }

    var drucken = document.getElementById('cl-print');
    if (drucken) { drucken.addEventListener('click', function () { window.print(); }); }
  }

  /* ---------- 11. Offertformular ---------- */
  var form = document.getElementById('offerte-form');
  if (!form) { return; }

  var status = document.getElementById('form-status');
  var submitBtn = form.querySelector('button[type="submit"]');

  var setError = function (field, message) {
    var box = form.querySelector('[data-error-for="' + field.name + '"]');
    if (box) { box.textContent = message || ''; }
    if (message) {
      field.setAttribute('aria-invalid', 'true');
    } else {
      field.removeAttribute('aria-invalid');
    }
  };

  var validateField = function (field) {
    var value = (field.value || '').trim();

    if (field.type === 'checkbox') {
      if (field.required && !field.checked) {
        setError(field, 'Bitte bestätigen, um fortzufahren.');
        return false;
      }
      setError(field, '');
      return true;
    }

    if (field.required && !value) {
      setError(field, 'Dieses Feld wird benötigt.');
      return false;
    }
    if (field.type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
      setError(field, 'Bitte eine gültige E-Mail-Adresse eingeben.');
      return false;
    }
    if (field.type === 'tel' && value && !/^[+0-9\s()/.-]{6,}$/.test(value)) {
      setError(field, 'Bitte eine gültige Telefonnummer eingeben.');
      return false;
    }
    setError(field, '');
    return true;
  };

  var fields = Array.prototype.slice.call(
    form.querySelectorAll('input:not([type="hidden"]):not(.hp input), select, textarea')
  );

  fields.forEach(function (field) {
    field.addEventListener('blur', function () { validateField(field); });
    field.addEventListener('input', function () {
      if (field.getAttribute('aria-invalid') === 'true') { validateField(field); }
    });
  });

  var showStatus = function (message, ok) {
    if (!status) { return; }
    status.textContent = message;
    status.className = 'form__status ' + (ok ? 'form__status--ok' : 'form__status--err');
    status.hidden = false;
  };

  var buildMailto = function (data) {
    var lines = [
      'Name: ' + (data.get('name') || ''),
      'Firma: ' + (data.get('firma') || '—'),
      'E-Mail: ' + (data.get('email') || ''),
      'Telefon: ' + (data.get('telefon') || '—'),
      'Leistung: ' + (data.get('leistung') || '—'),
      'Objekt / Fläche: ' + (data.get('objekt') || '—'),
      'Wunschtermin: ' + (data.get('termin') || '—'),
      '',
      'Nachricht:',
      (data.get('nachricht') || '')
    ];
    return 'mailto:' + FALLBACK_MAIL +
      '?subject=' + encodeURIComponent('Offertanfrage über die Website') +
      '&body=' + encodeURIComponent(lines.join('\n'));
  };

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Honeypot: von Menschen nie ausgefüllt.
    var trap = form.querySelector('input[name="website"]');
    if (trap && trap.value) { return; }

    var valid = true;
    fields.forEach(function (field) {
      if (!validateField(field)) { valid = false; }
    });

    if (!valid) {
      showStatus('Bitte die markierten Felder prüfen.', false);
      var firstBad = form.querySelector('[aria-invalid="true"]');
      if (firstBad) { firstBad.focus(); }
      return;
    }

    var data = new FormData(form);

    if (!FORM_ENDPOINT) {
      showStatus('Ihr E-Mail-Programm öffnet sich mit der fertigen Anfrage. Alternativ erreichen Sie uns telefonisch.', true);
      window.location.href = buildMailto(data);
      // Das mailto beendet die Seite nicht – kurz danach zur Bestätigung wechseln.
      window.setTimeout(function () { window.location.href = 'danke.html'; }, 1200);
      return;
    }

    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Wird gesendet …'; }

    fetch(FORM_ENDPOINT, {
      method: 'POST',
      body: data,
      headers: { Accept: 'application/json' }
    }).then(function (res) {
      if (!res.ok) { throw new Error('HTTP ' + res.status); }
      form.reset();
      showStatus('Vielen Dank! Ihre Anfrage ist eingegangen – wir melden uns innert 24 Stunden.', true);
      window.setTimeout(function () { window.location.href = 'danke.html'; }, 600);
    }).catch(function () {
      showStatus('Der Versand hat nicht geklappt. Bitte rufen Sie uns an oder schreiben Sie an ' + FALLBACK_MAIL + '.', false);
    }).finally(function () {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Offerte anfordern'; }
    });
  });
})();
