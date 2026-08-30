(function () {
  "use strict";

  var statusEl = document.querySelector("[data-status]");
  var hitsEl = document.querySelector("[data-hits]");
  var themesEl = document.querySelector("[data-theme-counts]");
  var searchEl = document.querySelector("[data-search]");
  var roleEl = document.querySelector("[data-role]");
  var fileEl = document.querySelector("[data-files]");
  var codebook = { themes: [] };
  var cues = [];

  function setStatus(t) {
    if (statusEl) statusEl.textContent = t;
  }

  function roleOf(line) {
    var s = line.toLowerCase();
    if (/\b(public|parent|teacher|student|community)\b/.test(s) && /comment|my name|i am a/.test(s)) return "public";
    if (/\btrustee\b/.test(s)) return "trustee";
    if (/\bsuperintendent\b/.test(s) || /\bstaff\b/.test(s) || /\bchief\b/.test(s)) return "staff";
    return "unknown";
  }

  function parseTranscript(name, text) {
    var lines = text.replace(/\r\n/g, "\n").split("\n");
    var out = [];
    var time = "";
    var buf = [];
    function flush() {
      var body = buf.join(" ").replace(/\s+/g, " ").trim();
      if (!body) return;
      out.push({
        file: name,
        time: time || "",
        text: body,
        role: roleOf(body)
      });
      buf = [];
    }
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].trim();
      if (!line) continue;
      var m = line.match(/^\[?(\d{1,2}:\d{2}:\d{2})(?:\.\d+)?\]?\s*(.*)$/);
      var srt = line.match(/^(\d{1,2}:\d{2}:\d{2})[.,]\d+\s*-->/);
      if (m) {
        flush();
        time = m[1];
        if (m[2]) buf.push(m[2]);
      } else if (srt) {
        flush();
        time = srt[1];
      } else if (/^\d+$/.test(line) || line === "WEBVTT") {
        continue;
      } else {
        buf.push(line);
      }
    }
    flush();
    return out;
  }

  function addCues(list) {
    cues = cues.concat(list);
    render();
  }

  function countThemes(subset) {
    var counts = codebook.themes.map(function (th) {
      var n = 0;
      for (var i = 0; i < subset.length; i++) {
        var t = subset[i].text.toLowerCase();
        for (var j = 0; j < th.needles.length; j++) {
          if (t.indexOf(th.needles[j]) !== -1) { n++; break; }
        }
      }
      return { label: th.label, n: n };
    });
    counts.sort(function (a, b) { return b.n - a.n; });
    return counts;
  }

  function render() {
    var q = searchEl && searchEl.value ? searchEl.value.trim().toLowerCase() : "";
    var role = roleEl && roleEl.value ? roleEl.value : "all";
    var subset = cues.filter(function (c) {
      if (role !== "all" && c.role !== role) return false;
      if (!q) return true;
      return (c.text + " " + c.file).toLowerCase().indexOf(q) !== -1;
    });
    if (themesEl) {
      themesEl.replaceChildren();
      countThemes(subset.length ? subset : cues).forEach(function (th) {
        var li = document.createElement("li");
        li.textContent = th.label + " — " + th.n;
        themesEl.appendChild(li);
      });
    }
    if (!hitsEl) return;
    hitsEl.replaceChildren();
    var max = Math.min(subset.length, 80);
    if (!cues.length) {
      var empty = document.createElement("p");
      empty.className = "note";
      empty.textContent = "No transcripts loaded yet. Use the file picker, or add files to meetings/manifest.json.";
      hitsEl.appendChild(empty);
      return;
    }
    var meta = document.createElement("p");
    meta.className = "note";
    meta.textContent = subset.length + " matching lines (showing " + max + ") from " + cues.length + " parsed lines. Work stays in this browser.";
    hitsEl.appendChild(meta);
    for (var i = 0; i < max; i++) {
      var c = subset[i];
      var art = document.createElement("article");
      art.className = "card";
      var h = document.createElement("h3");
      h.textContent = (c.time ? c.time + " · " : "") + c.file + " · " + c.role;
      var p = document.createElement("p");
      p.textContent = c.text;
      art.appendChild(h);
      art.appendChild(p);
      hitsEl.appendChild(art);
    }
  }

  if (fileEl) {
    fileEl.addEventListener("change", function () {
      var files = fileEl.files;
      var pending = files.length;
      if (!pending) return;
      setStatus("Reading " + pending + " local file(s)…");
      Array.prototype.forEach.call(files, function (file) {
        var reader = new FileReader();
        reader.onload = function () {
          addCues(parseTranscript(file.name, String(reader.result || "")));
          pending--;
          if (!pending) setStatus("Loaded. Search and theme counts update as you type. Files were not uploaded.");
        };
        reader.readAsText(file);
      });
    });
  }
  if (searchEl) searchEl.addEventListener("input", render);
  if (roleEl) roleEl.addEventListener("change", render);

  fetch("meetings/codebook.json", { credentials: "same-origin" })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (j) { if (j) codebook = j; render(); })
    .catch(function () {});

  fetch("meetings/manifest.json", { credentials: "same-origin" })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (man) {
      if (!man || !man.files || !man.files.length) return;
      man.files.forEach(function (path) {
        fetch("meetings/" + path, { credentials: "same-origin" })
          .then(function (r) { return r.ok ? r.text() : ""; })
          .then(function (t) { if (t) addCues(parseTranscript(path, t)); });
      });
    })
    .catch(function () {});

  render();
})();
