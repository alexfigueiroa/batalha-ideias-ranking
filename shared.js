/* shared.js — Batalha de Ideias 2026 */

function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

function fmtNum(v) { if (v==null) return '—'; return String(v).replace('.',','); }

function dotPct(total) { return 2 + (total - 5) / 20 * 96; }

function firstInitial(name) {
  if (!name) return '?';
  var p = name.trim().split(/ +/);
  var ini = p[0].charAt(0).toUpperCase();
  if (p.length >= 3) ini += p[1].charAt(0).toUpperCase() + p[p.length-1].charAt(0).toUpperCase();
  else if (p.length === 2) ini += p[1].charAt(0).toUpperCase();
  return ini;
}

function shortName(name) {
  if (!name) return 'Avaliador';
  var parts = name.trim().split(/ +/);
  return parts.length === 1 ? parts[0] : parts[0] + ' ' + parts[parts.length-1];
}

function hlText(s, q) {
  if (!q) return esc(s);
  var idx = s.toLowerCase().indexOf(q.toLowerCase());
  if (idx < 0) return esc(s);
  return esc(s.slice(0,idx)) + '<mark style="background:#fef08a;border-radius:2px">' + esc(s.slice(idx,idx+q.length)) + '</mark>' + esc(s.slice(idx+q.length));
}

function renderDotplot(sets, avsa) {
  var MAX_SLOTS=3; var TRACK_H=25; var DOT_H=25;
  var scoredAvs = (sets||[]).map(function(s){return s.av;});
  var pendingAvs = (avsa||[]).filter(function(av){return scoredAvs.indexOf(av)<0;});
  var axisRow = '<div class="dp-axis-labels-row"><div class="dp-axis-labels-spacer"></div><div class="dp-axis-labels"><span>5</span><span>15</span><span>25</span></div></div>';
  var trackRows=''; var pendingIdx=0;
  for (var si=0;si<MAX_SLOTS;si++) {
    var tColor=DOT_COLORS[si]; var tSet=sets&&sets[si]?sets[si]:null; var avLabel='A'+(si+1);
    if (tSet) {
      var pct=dotPct(tSet.total); var init=firstInitial(tSet.av);
      var avAvgs=AV_CRIT_AVGS[tSet.av]||{};
      var critLine='Média Avaliação/Critério: '+CRITS.map(function(c){var v=avAvgs[c];return c+'('+(v!=null?v:'—')+')'}).join(' · ');
      var tip=(tSet.av||'')+(tSet.dept?' · '+tSet.dept:'')+'\n'+critLine;
      trackRows+='<div class="dp-track-row"><div class="dp-track-av-label" style="color:'+tColor+'">'+avLabel+'</div><div class="dp-track" style="height:'+TRACK_H+'px"><div class="dp-mid-mark"></div><div class="dp-dot" style="left:'+pct.toFixed(1)+'%;background:'+tColor+';width:'+DOT_H+'px;height:'+DOT_H+'px" title="'+esc(tip)+'">'+init+'</div></div></div>';
    } else {
      var pendingAv=pendingAvs[pendingIdx++]||null;
      if (pendingAv) {
        var pInit=firstInitial(pendingAv); var pTip=shortName(pendingAv)+' — Pendente';
        trackRows+='<div class="dp-track-row"><div class="dp-track-av-label" style="color:#94a3b8">'+avLabel+'</div><div class="dp-track" style="height:'+TRACK_H+'px"><div class="dp-mid-mark"></div><div class="dp-dot" style="left:2%;background:#bfbfbf;width:'+DOT_H+'px;height:'+DOT_H+'px" title="'+esc(pTip)+'">'+pInit+'</div></div></div>';
      } else {
        trackRows+='<div class="dp-track-row"><div class="dp-track-av-label" style="color:#e2e8f0">'+avLabel+'</div><div class="dp-track-empty"></div></div>';
      }
    }
  }
  return axisRow+trackRows;
}

function renderCrits(sets) {
  var MAX_SLOTS=3; var html='<div class="dp-crits">';
  for (var ci=0;ci<MAX_SLOTS;ci++) {
    var cSet=sets&&sets[ci]?sets[ci]:null; var cColor=DOT_COLORS[ci]||'#94a3b8'; var isFirst=ci===0;
    var totalLbl=isFirst?'<span class="dp-crit-total-lbl">P</span>':'<span class="dp-crit-total-lbl" style="visibility:hidden;display:none">P</span>';
    if (cSet) {
      var totalBadge='<div class="dp-crit-item">'+totalLbl+'<span class="dp-crit-total" style="background:'+cColor+';color:#fff">'+cSet.total+'</span></div>';
      var items=CRITS.map(function(c) {
        var v=(cSet[c]!==undefined&&cSet[c]!==null)?cSet[c]:null;
        var lbl=isFirst?'<span class="dp-crit-lbl">'+c+'</span>':'<span class="dp-crit-lbl" style="visibility:hidden;display:none">'+c+'</span>';
        return '<div class="dp-crit-item">'+lbl+'<span class="sc" style="background:'+cColor+'22;color:'+cColor+'">'+(v!==null?v:'–')+'</span></div>';
      }).join('');
      html+='<div class="dp-crit-row">'+totalBadge+items+'</div>';
    } else {
      var lbl=isFirst?'<span class="dp-crit-lbl">?</span>':'';
      html+='<div class="dp-crit-row"><div class="dp-crit-item">'+totalLbl+'<span class="dp-crit-total" style="background:#e2e8f0;color:#94a3b8">?</span></div>'+CRITS.map(function(c){var l=isFirst?'<span class="dp-crit-lbl">'+c+'</span>':'';return '<div class="dp-crit-item">'+l+'<span class="sc" style="background:#f1f5f9;color:#cbd5e1">–</span></div>';}).join('')+'</div>';
    }
  }
  return html+'</div>';
}

function chipArenas(arenas) {
  return (arenas||[]).map(function(a) {
    var short=a.indexOf('Efici')>=0?'EOA':a.indexOf('Neg')>=0?'NDE':a.indexOf('Seg')>=0?'SI':a.slice(0,8);
    return '<span class="dp-chip dp-chip-arena" title="'+esc(a)+'">'+short+'</span>';
  }).join('');
}

function chipTecs(tecs) {
  return (tecs||[]).filter(function(t){return t.toLowerCase().indexOf('não sei')<0;}).map(function(t) {
    var short=t.indexOf('Blockchain')>=0?'BLK':t.indexOf('Dados')>=0?'DA':t.indexOf('Hiper')>=0?'RPA':t.indexOf('IA')>=0?'IA':t.indexOf('Cloud')>=0?'CLOUD':t.indexOf('Segu')>=0?'SEG':t.slice(0,6).toUpperCase();
    return '<span class="dp-chip dp-chip-tec" title="'+esc(t)+'">'+short+'</span>';
  }).join('');
}

function trlChip(trl) {
  if (!trl) return '';
  var num = parseInt(trl.replace('TRL','').trim(), 10);
  var color = num <= 3 ? '#6b7280' : num <= 6 ? '#2563eb' : '#059669';
  var bg    = num <= 3 ? '#f3f4f6' : num <= 6 ? '#dbeafe' : '#d1fae5';
  var bord  = num <= 3 ? '#d1d5db' : num <= 6 ? '#93c5fd' : '#6ee7b7';
  return '<span class="dp-chip" style="border-color:'+bord+';color:'+color+';background:'+bg+'" title="Grau de maturidade percebido">'+esc(trl)+'</span>';
}

function tipoChip(tipo) {
  if (!tipo || tipo === 'CLT/BBTS') return '';
  var color = tipo.indexOf('Posto') >= 0 ? '#d97706' : '#dc2626';
  var bg    = tipo.indexOf('Posto') >= 0 ? '#fef3c7' : '#fee2e2';
  var border= tipo.indexOf('Posto') >= 0 ? '#fde68a' : '#fca5a5';
  return ' <span style="font-size:0.62rem;font-weight:600;color:'+color+';background:'+bg+';border:1px solid '+border+';border-radius:3px;padding:1px 5px;white-space:nowrap">'+esc(tipo)+'</span>';
}

