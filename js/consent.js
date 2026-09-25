/* Cookie / analytics consent for loyaltyprogramguy.com
   Google Analytics loads ONLY after the visitor accepts. First-party, privacy-friendly
   site analytics (no third party) continue to run so the site keeps working.
   Choice is stored in localStorage and can be changed from the footer link. */
(function () {
  var KEY = 'lpg-consent';           // 'accepted' | 'declined'
  var GA_ID = 'G-N7JTY70D7C';

  function read() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function save(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  var loaded = false;
  function loadGA() {
    if (loaded) return;
    loaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, window.LPG_GA_PARAMS || {});
  }

  var banner;
  function closeBanner() { if (banner) { banner.remove(); banner = null; } }

  function showBanner() {
    if (banner) return;
    banner = document.createElement('div');
    banner.className = 'consent-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie choices');
    banner.innerHTML =
      '<div class="consent-inner">' +
        '<p>We use cookies to see how visitors use our site so we can improve it. ' +
        'Nothing loads until you choose. <a href="/privacy/">Privacy Policy</a></p>' +
        '<div class="consent-actions">' +
          '<button type="button" class="consent-btn ghost" data-consent="declined">Decline</button>' +
          '<button type="button" class="consent-btn solid" data-consent="accepted">Accept</button>' +
        '</div>' +
      '</div>';
    banner.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-consent]');
      if (!btn) return;
      var choice = btn.getAttribute('data-consent');
      save(choice);
      closeBanner();
      if (choice === 'accepted') loadGA();
    });
    document.body.appendChild(banner);
    // Do NOT focus the Accept button. This banner is static at the END of the document,
    // not a modal overlay, so focusing it scrolls the visitor to the bottom of the page
    // and they never see the hero. (Caught 2026-09-24 on /hakumaru: fresh loads landed at
    // 3044px of 3812.) Keyboard users reach it in normal document order, which is correct
    // for a non-modal element.
  }

  function init() {
    var choice = read();
    if (choice === 'accepted') loadGA();
    else if (choice !== 'declined') showBanner();

    document.addEventListener('click', function (e) {
      var el = e.target.closest('[data-privacy-choices]');
      if (!el) return;
      e.preventDefault();
      showBanner();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
