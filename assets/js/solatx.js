(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.querySelectorAll('a[href^="http"]').forEach(function (a) {
    try {
      if (a.hostname && a.hostname !== window.location.hostname) {
        a.setAttribute("rel", "noopener noreferrer");
      }
    } catch (e) {}
  });

  function field(form, name) {
    var el = form.elements.namedItem(name);
    return el && typeof el.value === "string" ? el.value.trim() : "";
  }

  function buildMailto(to, subject, body) {
    return "mailto:" + encodeURIComponent(to) +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);
  }

  document.querySelectorAll("[data-mail-form]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var name = field(form, "name");
      var topic = field(form, "topic") || "Austin ISD public record";
      var message = field(form, "message");
      var school = field(form, "school");
      if (!message) {
        form.reportValidity();
        return;
      }
      var lines = [];
      if (name) lines.push("Name: " + name);
      if (school) lines.push("Campus / library: " + school);
      lines.push("Topic: " + topic);
      lines.push("");
      lines.push(message);
      lines.push("");
      lines.push("Sent via SOLATX (solatx.org). SOLATX does not speak for AISD or the State of Texas.");
      window.location.href = buildMailto("board@austinisd.org", topic, lines.join("\n"));
    });
  });

  var draftKey = "solatx-library-drafts";
  var saveBtn = document.querySelector("[data-save-draft]");
  var list = document.querySelector("[data-draft-list]");
  function readDrafts() {
    try {
      var raw = localStorage.getItem(draftKey);
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }
  function writeDrafts(items) {
    localStorage.setItem(draftKey, JSON.stringify(items.slice(0, 20)));
  }
  function renderDrafts() {
    if (!list) return;
    list.replaceChildren();
    var items = readDrafts();
    if (!items.length) {
      var empty = document.createElement("p");
      empty.className = "note";
      empty.textContent = "No drafts on this device.";
      list.appendChild(empty);
      return;
    }
    items.forEach(function (item, i) {
      var p = document.createElement("p");
      p.textContent = (item.school ? item.school + " — " : "") + item.text;
      list.appendChild(p);
      var del = document.createElement("button");
      del.type = "button";
      del.className = "btn ghost";
      del.textContent = "Delete draft";
      del.addEventListener("click", function () {
        var next = readDrafts();
        next.splice(i, 1);
        writeDrafts(next);
        renderDrafts();
      });
      list.appendChild(del);
    });
  }
  if (saveBtn) {
    saveBtn.addEventListener("click", function () {
      var form = saveBtn.closest("form");
      if (!form) return;
      var text = field(form, "message");
      if (!text) return;
      var items = readDrafts();
      items.unshift({ school: field(form, "school"), text: text, t: Date.now() });
      writeDrafts(items);
      renderDrafts();
    });
    renderDrafts();
  }

  var chart = document.querySelector("[data-recapture-chart]");
  if (chart) {
    fetch("data/aisd.json", { credentials: "same-origin" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data || !data.recapture_series) return;
        var max = 0;
        data.recapture_series.forEach(function (row) {
          if (row.recapture > max) max = row.recapture;
        });
        var bars = document.createElement("div");
        bars.className = "bars";
        data.recapture_series.forEach(function (row) {
          var pct = Math.max(2, Math.round((row.recapture / max) * 100));
          var wrap = document.createElement("div");
          wrap.className = "bar-row";
          var y = document.createElement("span");
          y.textContent = row.fy;
          var track = document.createElement("div");
          track.className = "bar-track";
          var fill = document.createElement("div");
          fill.className = "bar-fill";
          fill.style.width = pct + "%";
          track.appendChild(fill);
          var val = document.createElement("b");
          val.textContent = "$" + (row.recapture / 1e6).toFixed(1) + "M";
          wrap.appendChild(y);
          wrap.appendChild(track);
          wrap.appendChild(val);
          bars.appendChild(wrap);
        });
        chart.appendChild(bars);
      })
      .catch(function () {});
  }
})();
