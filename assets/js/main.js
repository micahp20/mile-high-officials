(function () {
  var STORAGE_KEY = "mho-theme";
  var root = document.documentElement;
  var toggle = document.querySelector(".theme-toggle");
  var media = window.matchMedia("(prefers-color-scheme: dark)");

  function systemTheme() {
    return media.matches ? "dark" : "light";
  }

  function currentTheme() {
    var value = root.getAttribute("data-theme");
    return value === "dark" || value === "light" ? value : systemTheme();
  }

  function syncToggle(theme) {
    if (!toggle) return;
    var next = theme === "dark" ? "light" : "dark";
    toggle.setAttribute("aria-label", "Switch to " + next + " theme");
    toggle.setAttribute("title", "Switch to " + next + " theme");
    toggle.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
  }

  function applyTheme(theme, persist) {
    root.setAttribute("data-theme", theme);
    if (persist) {
      try { localStorage.setItem(STORAGE_KEY, theme); } catch (e) {}
    }
    syncToggle(theme);
  }

  syncToggle(currentTheme());

  if (toggle) {
    toggle.addEventListener("click", function () {
      applyTheme(currentTheme() === "dark" ? "light" : "dark", true);
    });
  }

  if (typeof media.addEventListener === "function") {
    media.addEventListener("change", function () {
      var saved = null;
      try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) {}
      if (saved !== "light" && saved !== "dark") applyTheme(systemTheme(), false);
    });
  }

  var navToggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");

  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var dropBtn = document.querySelector(".drop-btn");
  var drop = document.querySelector(".drop");
  if (dropBtn && drop) {
    dropBtn.addEventListener("click", function (e) {
      if (window.matchMedia("(max-width: 880px)").matches) {
        e.preventDefault();
        drop.classList.toggle("is-open");
        dropBtn.setAttribute("aria-expanded", drop.classList.contains("is-open") ? "true" : "false");
      }
    });
  }

  var form = document.querySelector("#contact-form");
  if (!form) return;

  var status = form.querySelector(".form-status");
  var topic = "general";
  try {
    topic = new URLSearchParams(window.location.search).get("topic") === "donation" ? "donation" : "general";
  } catch (e) {}
  if (topic === "donation") {
    var title = document.getElementById("form-title");
    if (title) title.textContent = "Send a donation inquiry";
    var topicField = form.querySelector('[name="topic"]');
    if (topicField) topicField.value = "donation";
    if (form.message && !form.message.value) {
      form.message.value = "I would like to learn more about making a donation to support Mile High Officials.";
    }
  }
  var submit = form.querySelector("[type=submit]");

  function show(type, message) {
    status.className = "form-status is-" + type;
    status.textContent = message;
    status.hidden = false;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var honey = form.querySelector('[name="_honey"]');
    if (honey && honey.value) {
      window.location.href = "/thank-you/";
      return;
    }

    var payload = {
      name: (form.name.value || "").trim(),
      email: (form.email.value || "").trim(),
      phone: (form.phone.value || "").trim(),
      message: (form.message.value || "").trim(),
      topic: topic === "donation" ? "Donation inquiry" : "General inquiry",
      _subject: (topic === "donation" ? "Donation inquiry from " : "Website contact from ") + (form.name.value || "").trim(),
      _template: "table",
      _captcha: "false"
    };

    if (!payload.name || !payload.email || !payload.message) {
      show("err", "Please enter your name, email, and a message.");
      return;
    }

    submit.disabled = true;
    submit.textContent = "Sending…";
    status.className = "form-status";
    status.hidden = true;

    fetch("https://formsubmit.co/ajax/715cffcfd4b9afa81b063f18821de910", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (res) {
        return res.json().then(function (data) {
          return { httpOk: res.ok, data: data };
        }).catch(function () {
          return { httpOk: res.ok, data: {} };
        });
      })
      .then(function (result) {
        var data = result.data || {};
        var ok = data.success === true || data.success === "true";
        var msg = String(data.message || "");
        if (ok || /confirm|activat|verification/i.test(msg)) {
          window.location.href = "/thank-you/";
          return;
        } else {
          show(
            "err",
            "We could not send your message just now. Please call 720-432-0354 or email admin@milehighofficials.com."
          );
        }
      })
      .catch(function () {
        show(
          "err",
          "We could not send your message just now. Please call 720-432-0354 or email admin@milehighofficials.com."
        );
      })
      .finally(function () {
        submit.disabled = false;
        submit.textContent = "Send message";
      });
  });
})();
