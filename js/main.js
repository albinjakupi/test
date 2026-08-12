/* =========================================================
   Glanzwerk Reinigung – main.js
   - Mobile-Navigation
   - Sticky-Header-Schatten
   - Einblende-Animation beim Scrollen
   - Jahreszahl im Footer
   - Validierung & Versand des Offertformulars
   ========================================================= */
(function () {
  'use strict';

  document.documentElement.classList.add('js');

  /* ---------- Konfiguration ----------
     ENDPOINT: URL eines Formular-Dienstes (z. B. Formspree, Getform, eigene
     PHP-/Serverless-Funktion). Solange der Wert leer ist, öffnet das Formular
     stattdessen das E-Mail-Programm mit vorausgefüllter Nachricht.
     Details siehe README.md.                                                */
  var FORM_ENDPOINT = '';
  var FALLBACK_MAIL = 'offerte@glanzwerk-reinigung.ch';

  /* ---------- Mobile-Navigation ---------- */
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

  /* ---------- Sticky-Header ---------- */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Einblenden beim Scrollen ---------- */
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

  /* ---------- Jahreszahl im Footer ---------- */
  var year = document.querySelectorAll('[data-year]');
  year.forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* ---------- Leistung aus der URL vorauswählen ----------
     Verlinkung wie kontakt.html?leistung=bueroreinigung setzt das Auswahlfeld. */
  var params = new URLSearchParams(window.location.search);
  var wanted = params.get('leistung');
  var serviceSelect = document.getElementById('leistung');
  if (wanted && serviceSelect) {
    Array.prototype.forEach.call(serviceSelect.options, function (opt) {
      if (opt.value === wanted) { serviceSelect.value = wanted; }
    });
  }

  /* ---------- Offertformular ---------- */
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
    }).catch(function () {
      showStatus('Der Versand hat nicht geklappt. Bitte rufen Sie uns an oder schreiben Sie an ' + FALLBACK_MAIL + '.', false);
    }).finally(function () {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Offerte anfordern'; }
    });
  });
})();
