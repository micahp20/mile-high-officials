(function () {
  var form = document.getElementById("apply-form");
  if (!form) return;
  var status = form.querySelector(".form-status");
  var submit = form.querySelector("[type=submit]");
  var started = Date.now();
  form.elements["_t"].value = String(started);

  // ?sport= prefill (accepts basketball, flag-football, youth-basketball, "Flag Football", ...)
  try {
    var raw = (new URLSearchParams(window.location.search).get("sport") || "").toLowerCase().trim();
    var slug = raw.replace(/^youth-/, "").replace(/[\s_]+/g, "-");
    if (slug) {
      var box = form.querySelector('input[name="sports"][data-slug="' + slug.replace(/[^a-z-]/g, "") + '"]');
      if (box) {
        box.checked = true;
        form.elements["source_sport"].value = slug;
      }
    }
  } catch (e) {}

  var trainingBox = document.getElementById("training-box");
  var wants = document.getElementById("wants_training");
  function syncTraining() {
    var exp = form.querySelector('input[name="has_experience"]:checked');
    var show = wants.checked || (exp && exp.value === "no");
    trainingBox.hidden = !show;
  }
  var refsBox = document.getElementById("refs-box");
  function syncRefs() {
    refsBox.hidden = radio("has_references") !== "yes";
  }
  form.addEventListener("change", function (e) {
    var n = e.target && e.target.name;
    if (n === "has_experience" || n === "wants_training") syncTraining();
    if (n === "has_references") syncRefs();
    if (n === "heard_about") document.getElementById("heard-other-field").hidden = e.target.value !== "Other";
  });
  syncTraining();
  syncRefs();

  function show(type, message) {
    status.className = "form-status is-" + type;
    status.textContent = message;
    status.hidden = false;
    status.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function radio(name) {
    var r = form.querySelector('input[name="' + name + '"]:checked');
    return r ? r.value : "";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (form.elements["_honey"].value) { window.location.href = "/apply/thank-you/"; return; }

    var missing = [];
    function need(ok, label) { if (!ok) missing.push(label); }
    need(form.full_name.value.trim(), "full name");
    need(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.value.trim()), "a valid email");
    need(form.phone.value.replace(/\D/g, "").length >= 10, "phone");
    need(form.city_zip.value.trim(), "city or ZIP");
    need(radio("is_18_plus"), "18 or older");
    need(radio("background_check_ok"), "background check");
    need(radio("reliable_transportation"), "transportation");
    need(form.querySelector('input[name="sports"]:checked') || form.sport_other.value.trim(), "at least one sport");
    need(radio("has_experience"), "previous experience");
    need(radio("has_references"), "references");
    if (radio("has_references") === "yes") {
      var f1 = form.ref1_first.value.trim(), l1 = form.ref1_last.value.trim(), p1 = form.ref1_phone.value.trim(), r1 = form.ref1_relationship.value.trim();
      need(f1 && l1 && p1 && r1, "reference 1 (first name, last name, phone, and relationship)");
    }
    if (missing.length) { show("err", "Please complete: " + missing.join(", ") + "."); return; }

    var file = form.resume.files && form.resume.files[0];
    if (file) {
      if (!/\.(pdf|docx?)$/i.test(file.name)) { show("err", "Résumé must be a PDF, DOC, or DOCX file."); return; }
      if (file.size > 4 * 1024 * 1024) { show("err", "Résumé must be 4 MB or smaller."); return; }
    }

    var data = new FormData(form);
    if (!file) data.delete("resume");
    submit.disabled = true;
    submit.textContent = "Submitting…";
    status.hidden = true;

    function fail() {
      submit.disabled = false;
      submit.textContent = "Submit application";
      show("err", "We could not submit your application just now. Please try again, call 720-432-0354, or email admin@milehighofficials.com.");
    }

    fetch("/api/apply", { method: "POST", body: data })
      .then(function (res) { return res.json().catch(function () { return {}; }).then(function (d) { return { ok: res.ok, d: d }; }); })
      .then(function (r) {
        if (!r.ok || !r.d.ok) {
          if (r.d && r.d.error) {
            submit.disabled = false;
            submit.textContent = "Submit application";
            show("err", r.d.error);
          } else fail();
          return;
        }
        var done = function () { window.location.href = "/apply/thank-you/"; };
        if (!r.d.email) return done();
        // The application is saved. Now email it to MHO through FormSubmit (same path as the contact form).
        // keepalive lets the email request finish even if the visitor leaves the page; after 8 seconds we move on anyway.
        var sent = fetch("https://formsubmit.co/ajax/715cffcfd4b9afa81b063f18821de910", {
          method: "POST",
          keepalive: true,
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(r.d.email)
        })
          .then(function (res) { return res.json().catch(function () { return {}; }); })
          .then(function (d) {
            if (d && (d.success === true || d.success === "true")) {
              return fetch("/api/apply?id=" + encodeURIComponent(r.d.id) + "&sig=" + encodeURIComponent(r.d.mark), { method: "PATCH", keepalive: true });
            }
          });
        Promise.race([sent, new Promise(function (res) { setTimeout(res, 8000); })]).then(done, done);
      })
      .catch(fail);
  });
})();
