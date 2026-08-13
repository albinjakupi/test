/* =========================================================
   Cleeno Reinigungen – Preisrechner

   Der Rechner liefert eine Spanne, keine Offerte. Alle Ansätze stehen
   zuoberst in TARIFE und lassen sich dort anpassen, ohne den restlichen
   Code anzufassen. Nach jeder Änderung die Richtpreise auf den
   Leistungsseiten mitziehen, damit beides zusammenpasst.
   ========================================================= */
(function () {
  'use strict';

  var form = document.getElementById('calc');
  if (!form) { return; }

  /* ---------- Tarife (hier anpassen) ---------- */
  var TARIFE = {
    stundensatz: [45, 55],          // CHF pro Stunde, Unterhaltsreinigung
    umzugBasis: {                   // Pauschalen nach Zimmerzahl
      '1.5': 390, '2.5': 490, '3.5': 690, '4.5': 890, '5.5': 1090
    },
    fensterProFluegel: [6, 9],      // beidseitig, inkl. Rahmen
    fensterMinimum: 180,
    bueroProM2: [0.45, 0.65],       // pro Einsatz
    bueroMinimum: 90,
    bauProM2: {                     // pro Etappe
      grob: [4, 6], fein: [6, 9], end: [7, 11]
    },
    bauMinimum: 400,
    liegenschaftProWohnung: [10, 16],
    liegenschaftMinimum: 120
  };

  var MONATE = { woche: 4.33, zwei: 2.17, monat: 1, einmal: 0 };

  /* ---------- Hilfsfunktionen ---------- */
  function chf(value) {
    var rounded = value >= 200 ? Math.round(value / 10) * 10 : Math.round(value / 5) * 5;
    return rounded.toLocaleString('de-CH');
  }

  function zimmerLabel(z) {
    return z >= 6.5 ? '6,5 Zimmer und grösser' : String(z).replace('.', ',') + ' Zimmer';
  }

  function sum(range, factor) {
    return [range[0] * factor, range[1] * factor];
  }

  /* ---------- Leistungen ---------- */
  var LEISTUNGEN = {
    unterhaltsreinigung: {
      name: 'Unterhaltsreinigung',
      felder: [
        { id: 'zimmer', label: 'Wie gross ist die Wohnung?', typ: 'range',
          min: 1.5, max: 6.5, step: 1, wert: 3.5, format: zimmerLabel }
      ],
      auswahl: [
        { id: 'frequenz', label: 'Wie oft sollen wir kommen?', wert: 'zwei', optionen: [
          { id: 'woche', label: 'Jede Woche' },
          { id: 'zwei', label: 'Alle zwei Wochen' },
          { id: 'monat', label: 'Einmal im Monat' },
          { id: 'einmal', label: 'Einmalig' }
        ] }
      ],
      extras: [
        { id: 'fenster', label: 'Fenster innen', zusatz: '+ ca. 0,6 Std.' },
        { id: 'backofen', label: 'Backofen innen', zusatz: '+ ca. 0,5 Std.' },
        { id: 'buegeln', label: 'Wäsche und Bügeln', zusatz: '+ ca. 1 Std.' }
      ],
      rechne: function (v) {
        var stunden = 1.0 + 0.6 * v.zimmer;
        if (v.fenster) { stunden += 0.6; }
        if (v.backofen) { stunden += 0.5; }
        if (v.buegeln) { stunden += 1.0; }

        var proEinsatz = sum(TARIFE.stundensatz, stunden);
        var proMonat = MONATE[v.frequenz];
        var zeile = [
          ['Wohnung', zimmerLabel(v.zimmer)],
          ['Aufwand', stunden.toFixed(1).replace('.', ',') + ' Std. pro Einsatz'],
          ['Rhythmus', this.auswahl[0].optionen.filter(function (o) { return o.id === v.frequenz; })[0].label]
        ];
        return {
          spanne: proEinsatz,
          einheit: 'pro Einsatz, inkl. Material und Anfahrt',
          zusatz: proMonat ? 'Das entspricht rund CHF ' + chf(proEinsatz[0] * proMonat) +
                             ' bis ' + chf(proEinsatz[1] * proMonat) + '.– pro Monat.' : '',
          zeilen: zeile
        };
      }
    },

    umzugsreinigung: {
      name: 'Umzugsreinigung',
      felder: [
        { id: 'zimmer', label: 'Wie gross ist die Wohnung?', typ: 'range',
          min: 1.5, max: 5.5, step: 1, wert: 3.5, format: zimmerLabel }
      ],
      auswahl: [
        { id: 'zustand', label: 'In welchem Zustand ist die Wohnung?', wert: 'normal', optionen: [
          { id: 'normal', label: 'Normal bewohnt' },
          { id: 'stark', label: 'Stark verschmutzt, Raucherwohnung oder Haustiere' }
        ] }
      ],
      extras: [
        { id: 'balkon', label: 'Balkon oder Sitzplatz', zusatz: '+ CHF 70.–' },
        { id: 'keller', label: 'Keller und Estrich', zusatz: '+ CHF 60.–' },
        { id: 'garage', label: 'Garage oder Einstellhallenplatz', zusatz: '+ CHF 50.–' }
      ],
      rechne: function (v) {
        var basis = TARIFE.umzugBasis[String(Math.min(5.5, v.zimmer))] || 1090;
        if (v.zimmer > 5.5) { basis += (v.zimmer - 5.5) * 180; }
        if (v.zustand === 'stark') { basis *= 1.25; }
        if (v.balkon) { basis += 70; }
        if (v.keller) { basis += 60; }
        if (v.garage) { basis += 50; }

        return {
          spanne: [basis * 0.94, basis * 1.08],
          einheit: 'Pauschale inkl. Fenster, Storen und Abnahmegarantie',
          zusatz: 'Wird bei der Abgabe etwas beanstandet, reinigen wir kostenlos nach.',
          zeilen: [
            ['Wohnung', zimmerLabel(v.zimmer)],
            ['Zustand', v.zustand === 'stark' ? 'Stark verschmutzt' : 'Normal bewohnt'],
            ['Fenster und Storen', 'inklusive']
          ]
        };
      }
    },

    fensterreinigung: {
      name: 'Fensterreinigung',
      felder: [
        { id: 'fluegel', label: 'Wie viele Fensterflügel?', typ: 'range',
          min: 4, max: 80, step: 2, wert: 12,
          format: function (n) { return n + ' Flügel'; },
          hinweis: 'Ein Flügel ist ein einzelnes zu öffnendes Fensterelement.' }
      ],
      auswahl: [
        { id: 'seiten', label: 'Welche Seiten?', wert: 'beide', optionen: [
          { id: 'beide', label: 'Innen und aussen' },
          { id: 'innen', label: 'Nur innen' }
        ] }
      ],
      extras: [
        { id: 'storen', label: 'Storen und Lamellen', zusatz: '+ CHF 3.50 pro Flügel' },
        { id: 'hoehe', label: 'Arbeiten in Höhe (Teleskop)', zusatz: '+ CHF 90.–' }
      ],
      rechne: function (v) {
        var satz = TARIFE.fensterProFluegel.slice();
        if (v.seiten === 'innen') { satz = sum(satz, 0.6); }
        var spanne = sum(satz, v.fluegel);
        if (v.storen) { spanne = [spanne[0] + v.fluegel * 3.5, spanne[1] + v.fluegel * 3.5]; }
        if (v.hoehe) { spanne = [spanne[0] + 90, spanne[1] + 90]; }
        spanne = [Math.max(TARIFE.fensterMinimum, spanne[0]), Math.max(TARIFE.fensterMinimum + 40, spanne[1])];

        return {
          spanne: spanne,
          einheit: 'einmalig, inkl. Rahmen, Falze und Simse',
          zusatz: 'Ab drei Reinigungen pro Jahr gewähren wir einen Rabatt auf den Gesamtpreis.',
          zeilen: [
            ['Fensterflügel', v.fluegel],
            ['Seiten', v.seiten === 'innen' ? 'Nur innen' : 'Innen und aussen'],
            ['Storen', v.storen ? 'inklusive' : 'nicht enthalten']
          ]
        };
      }
    },

    bueroreinigung: {
      name: 'Büroreinigung',
      felder: [
        { id: 'flaeche', label: 'Wie gross ist die Fläche?', typ: 'range',
          min: 50, max: 1500, step: 25, wert: 250,
          format: function (n) { return n.toLocaleString('de-CH') + ' m²'; } }
      ],
      auswahl: [
        { id: 'frequenz', label: 'Wie oft pro Woche?', wert: 'zwei', optionen: [
          { id: 'fuenf', label: 'Täglich (5×)' },
          { id: 'drei', label: '3× pro Woche' },
          { id: 'zwei', label: '2× pro Woche' },
          { id: 'eins', label: '1× pro Woche' }
        ] }
      ],
      extras: [
        { id: 'material', label: 'Verbrauchsmaterial (Seife, Papier)', zusatz: '+ CHF 45.– pro Monat' },
        { id: 'fenster', label: 'Fensterreinigung 2× jährlich', zusatz: '+ ca. CHF 40.– pro Monat' }
      ],
      rechne: function (v) {
        var einsaetze = { fuenf: 21.7, drei: 13, zwei: 8.7, eins: 4.33 }[v.frequenz];
        var proEinsatz = sum(TARIFE.bueroProM2, v.flaeche);
        proEinsatz = [Math.max(TARIFE.bueroMinimum, proEinsatz[0]),
                      Math.max(TARIFE.bueroMinimum + 25, proEinsatz[1])];
        var monat = sum(proEinsatz, einsaetze);
        if (v.material) { monat = [monat[0] + 45, monat[1] + 45]; }
        if (v.fenster) { monat = [monat[0] + 35, monat[1] + 50]; }

        return {
          spanne: monat,
          einheit: 'pro Monat, Pauschale',
          zusatz: 'Das entspricht rund CHF ' + chf(proEinsatz[0]) + ' bis ' + chf(proEinsatz[1]) + '.– pro Einsatz.',
          zeilen: [
            ['Fläche', v.flaeche.toLocaleString('de-CH') + ' m²'],
            ['Einsätze', Math.round(einsaetze) + ' pro Monat'],
            ['Zeitfenster', 'ausserhalb der Bürozeiten']
          ]
        };
      }
    },

    bauendreinigung: {
      name: 'Bauendreinigung',
      felder: [
        { id: 'flaeche', label: 'Wie gross ist die Fläche?', typ: 'range',
          min: 50, max: 1200, step: 25, wert: 200,
          format: function (n) { return n.toLocaleString('de-CH') + ' m²'; } }
      ],
      auswahl: [
        { id: 'zustand', label: 'Wie stark verschmutzt?', wert: 'normal', optionen: [
          { id: 'normal', label: 'Üblich für eine Baustelle' },
          { id: 'stark', label: 'Stark (Zement-, Farb-, Kleberreste)' }
        ] }
      ],
      extras: [
        { id: 'grob', label: 'Grobreinigung nach Rohbau', zusatz: 'eigene Etappe' },
        { id: 'fein', label: 'Feinreinigung nach Handwerkern', zusatz: 'eigene Etappe' },
        { id: 'end', label: 'Endreinigung vor Übergabe', zusatz: 'eigene Etappe', standard: true }
      ],
      rechne: function (v) {
        var etappen = [];
        var tief = 0, hoch = 0;
        ['grob', 'fein', 'end'].forEach(function (key) {
          if (!v[key]) { return; }
          tief += TARIFE.bauProM2[key][0] * v.flaeche;
          hoch += TARIFE.bauProM2[key][1] * v.flaeche;
          etappen.push({ grob: 'Grob', fein: 'Fein', end: 'End' }[key]);
        });
        if (!etappen.length) {
          tief = TARIFE.bauProM2.end[0] * v.flaeche;
          hoch = TARIFE.bauProM2.end[1] * v.flaeche;
          etappen.push('End');
        }
        if (v.zustand === 'stark') { tief *= 1.2; hoch *= 1.25; }

        return {
          spanne: [Math.max(TARIFE.bauMinimum, tief), Math.max(TARIFE.bauMinimum + 120, hoch)],
          einheit: 'einmalig, alle gewählten Etappen zusammen',
          zusatz: 'Termine stimmen wir direkt mit der Bauleitung ab – auch abends und samstags.',
          zeilen: [
            ['Fläche', v.flaeche.toLocaleString('de-CH') + ' m²'],
            ['Etappen', etappen.join(', ') + 'reinigung'],
            ['Zustand', v.zustand === 'stark' ? 'Stark verschmutzt' : 'Üblich']
          ]
        };
      }
    },

    liegenschaftsreinigung: {
      name: 'Liegenschaftsreinigung',
      felder: [
        { id: 'wohnungen', label: 'Wie viele Wohnungen hat die Liegenschaft?', typ: 'range',
          min: 4, max: 60, step: 2, wert: 12,
          format: function (n) { return n + ' Wohnungen'; } }
      ],
      auswahl: [
        { id: 'turnus', label: 'In welchem Turnus?', wert: 'zwei', optionen: [
          { id: 'woche', label: 'Wöchentlich' },
          { id: 'zwei', label: 'Alle zwei Wochen' },
          { id: 'monat', label: 'Monatlich' }
        ] }
      ],
      extras: [
        { id: 'umgebung', label: 'Umgebung und Grünpflege', zusatz: '+ ca. 25 %' },
        { id: 'winter', label: 'Winterdienst mit Bereitschaft', zusatz: '+ CHF 180.– pro Monat (Nov–März)' }
      ],
      rechne: function (v) {
        var proEinsatz = sum(TARIFE.liegenschaftProWohnung, v.wohnungen);
        proEinsatz = [Math.max(TARIFE.liegenschaftMinimum, proEinsatz[0]),
                      Math.max(TARIFE.liegenschaftMinimum + 40, proEinsatz[1])];
        var faktor = MONATE[v.turnus];
        var monat = sum(proEinsatz, faktor);
        if (v.umgebung) { monat = sum(monat, 1.25); }
        if (v.winter) { monat = [monat[0] + 180, monat[1] + 180]; }

        return {
          spanne: monat,
          einheit: 'pro Monat, Pauschale',
          zusatz: v.winter ? 'Der Winterdienst wird nur von November bis März verrechnet.'
                           : 'Der Reinigungsplan hängt im Eingang aus – für Mietende nachvollziehbar.',
          zeilen: [
            ['Liegenschaft', v.wohnungen + ' Wohnungen'],
            ['Turnus', this.auswahl[0].optionen.filter(function (o) { return o.id === v.turnus; })[0].label],
            ['Umgebung', v.umgebung ? 'inklusive' : 'nicht enthalten']
          ]
        };
      }
    }
  };

  /* ---------- Zustand ---------- */
  var state = { leistung: 'umzugsreinigung' };
  var schritt = 1;

  var elDetails = document.getElementById('calc-details');
  var elExtras = document.getElementById('calc-extras');
  var elPrice = document.getElementById('calc-price');
  var elUnit = document.getElementById('calc-unit');
  var elList = document.getElementById('calc-list');
  var elNote = document.getElementById('calc-note');
  var elCta = document.getElementById('calc-cta');
  var elSteps = document.querySelectorAll('.calc__steps li');
  var elBack = document.getElementById('calc-back');
  var elNext = document.getElementById('calc-next');
  var elFinish = document.getElementById('calc-finish');
  var steps = document.querySelectorAll('.calc__step');

  function aktuelle() { return LEISTUNGEN[state.leistung]; }

  /* ---------- Schritt 2 und 3 aufbauen ---------- */
  function renderDetails() {
    var l = aktuelle();
    var html = '';

    l.felder.forEach(function (feld) {
      if (state[feld.id] === undefined) { state[feld.id] = feld.wert; }
      html += '<div class="calc__field">' +
        '<label for="f-' + feld.id + '">' + feld.label + '</label>' +
        '<div class="calc__row">' +
        '<input type="range" id="f-' + feld.id + '" data-feld="' + feld.id + '" min="' + feld.min +
        '" max="' + feld.max + '" step="' + feld.step + '" value="' + state[feld.id] + '">' +
        '<output class="calc__value" for="f-' + feld.id + '" id="o-' + feld.id + '">' +
        feld.format(state[feld.id]) + '</output>' +
        '</div>' +
        (feld.hinweis ? '<p class="hint">' + feld.hinweis + '</p>' : '') +
        '</div>';
    });

    l.auswahl.forEach(function (gruppe) {
      if (state[gruppe.id] === undefined) { state[gruppe.id] = gruppe.wert; }
      html += '<div class="calc__field"><label as="legend">' + gruppe.label + '</label><div class="choices">';
      gruppe.optionen.forEach(function (opt) {
        html += '<label class="choice"><input type="radio" name="' + gruppe.id + '" value="' + opt.id +
          '" data-gruppe="' + gruppe.id + '"' + (state[gruppe.id] === opt.id ? ' checked' : '') +
          '><span>' + opt.label + '</span></label>';
      });
      html += '</div></div>';
    });

    elDetails.innerHTML = html;
  }

  function renderExtras() {
    var l = aktuelle();
    var html = '<div class="choices">';
    l.extras.forEach(function (extra) {
      if (state[extra.id] === undefined) { state[extra.id] = !!extra.standard; }
      html += '<label class="choice"><input type="checkbox" data-extra="' + extra.id + '"' +
        (state[extra.id] ? ' checked' : '') + '><span>' + extra.label +
        (extra.zusatz ? '<small>' + extra.zusatz + '</small>' : '') + '</span></label>';
    });
    html += '</div>';
    elExtras.innerHTML = html;
  }

  /* ---------- Ergebnis ---------- */
  function puls() {
    if (!elPrice) { return; }
    elPrice.classList.remove('is-updated');
    void elPrice.offsetWidth;          // Neustart der Animation erzwingen
    elPrice.classList.add('is-updated');
  }

  function rechne() {
    var l = aktuelle();
    var res = l.rechne.call(l, state);

    elPrice.innerHTML = '<small>Richtpreis</small>CHF ' + chf(res.spanne[0]) + ' – ' + chf(res.spanne[1]);
    elUnit.textContent = res.einheit;
    elList.innerHTML = '<li><span>Leistung</span><strong>' + l.name + '</strong></li>' +
      res.zeilen.map(function (z) {
        return '<li><span>' + z[0] + '</span><strong>' + z[1] + '</strong></li>';
      }).join('');
    elNote.textContent = res.zusatz
      ? res.zusatz + ' Unverbindlicher Richtwert – verbindlich ist die schriftliche Offerte.'
      : 'Unverbindlicher Richtwert – verbindlich ist die schriftliche Offerte.';

    var beschreibung = res.zeilen.map(function (z) { return z[0] + ': ' + z[1]; }).join(', ');
    if (elFinish) { elFinish.href = elCta.href; }
    elCta.href = 'kontakt.html?leistung=' + encodeURIComponent(state.leistung) +
      '&objekt=' + encodeURIComponent(res.zeilen[0][1]) +
      '&nachricht=' + encodeURIComponent(
        'Über den Preisrechner ermittelt – ' + l.name + '. ' + beschreibung +
        '. Angezeigter Richtpreis: CHF ' + chf(res.spanne[0]) + ' – ' + chf(res.spanne[1]) + '.');
  }

  /* ---------- Schritte ---------- */
  function zeigeSchritt(n) {
    schritt = Math.min(3, Math.max(1, n));
    Array.prototype.forEach.call(steps, function (fs, i) { fs.hidden = (i + 1) !== schritt; });
    Array.prototype.forEach.call(elSteps, function (li, i) {
      if (i + 1 === schritt) { li.setAttribute('aria-current', 'step'); }
      else { li.removeAttribute('aria-current'); }
      li.setAttribute('data-done', String(i + 1 < schritt));
    });
    elBack.hidden = schritt === 1;
    elNext.hidden = schritt === 3;
    if (elFinish) { elFinish.hidden = schritt !== 3; }

    var legend = steps[schritt - 1].querySelector('legend');
    if (legend && schritt > 1) { legend.setAttribute('tabindex', '-1'); legend.focus(); }
  }

  /* ---------- Ereignisse ---------- */
  form.addEventListener('change', function (e) {
    var t = e.target;

    if (t.name === 'leistung') {
      // Zustand zurücksetzen, damit Felder der neuen Leistung greifen
      state = { leistung: t.value };
      renderDetails();
      renderExtras();
      rechne();
      puls();
      return;
    }
    if (t.dataset.gruppe) { state[t.dataset.gruppe] = t.value; rechne(); puls(); return; }
    if (t.dataset.extra) { state[t.dataset.extra] = t.checked; rechne(); puls(); return; }
  });

  form.addEventListener('input', function (e) {
    var t = e.target;
    if (!t.dataset.feld) { return; }
    var feld = aktuelle().felder.filter(function (f) { return f.id === t.dataset.feld; })[0];
    state[t.dataset.feld] = parseFloat(t.value);
    var out = document.getElementById('o-' + t.dataset.feld);
    if (out && feld) { out.textContent = feld.format(state[t.dataset.feld]); }
    rechne();
  });

  form.addEventListener('submit', function (e) { e.preventDefault(); });

  elNext.addEventListener('click', function () { zeigeSchritt(schritt + 1); });
  elBack.addEventListener('click', function () { zeigeSchritt(schritt - 1); });

  /* ---------- Start ---------- */
  var vorgabe = new URLSearchParams(window.location.search).get('leistung');
  if (vorgabe && LEISTUNGEN[vorgabe]) { state.leistung = vorgabe; }
  var radio = form.querySelector('input[name="leistung"][value="' + state.leistung + '"]');
  if (radio) { radio.checked = true; }

  renderDetails();
  renderExtras();
  rechne();
  zeigeSchritt(1);
})();
