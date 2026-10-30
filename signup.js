// Saves each signup to the site owner's Supabase table (lawyerbenchmarks_signups).
// The key below is Supabase's public "publishable" key: visitors can only add an email, never read the list.
(function () {
  var url = 'https://wikdpzhuymhtkyzqtrak.supabase.co/rest/v1/lawyerbenchmarks_signups';
  var key = 'sb_publishable_XMOGB9Hzv9mFWuz65bQCAg_x3NJeNoM';

  document.querySelectorAll('form.signup').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var button = form.querySelector('button');
      var label = form.querySelector('label');
      var done = function () { form.innerHTML = '<p class="msg">thanks, you’re on the list.</p>'; };

      // Bots fill the hidden field; pretend it worked and save nothing.
      if (form._honey.value) return done();

      button.disabled = true;
      fetch(url, {
        method: 'POST',
        headers: { apikey: key, 'Content-Type': 'application/json', Prefer: 'return=minimal' },
        body: JSON.stringify({ email: form.email.value.trim(), page: location.pathname })
      })
        .then(function (r) {
          // 409 means this email is already signed up, which is fine.
          if (r.ok || r.status === 409) return done();
          throw new Error(r.status);
        })
        .catch(function () {
          button.disabled = false;
          label.textContent = 'that didn’t go through. try again?';
        });
    });
  });
})();
