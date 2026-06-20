// ── NAVIGATION ──
function toggleNav() {
  const links = document.getElementById('nav-links');
  links.classList.toggle('open');
}

// Close mobile nav on link click
document.querySelectorAll('.nav-links a').forEach(a => {
  a.addEventListener('click', () => {
    document.getElementById('nav-links').classList.remove('open');
  });
});

// ── GALLERY TABS ──
function switchTab(tabName, btn) {
  // Hide all sections
  document.querySelectorAll('.gallery-section').forEach(s => s.classList.remove('active'));
  // Deactivate all tabs
  document.querySelectorAll('.gallery-tab').forEach(t => t.classList.remove('active'));
  // Show target section
  const target = document.getElementById('tab-' + tabName);
  if (target) target.classList.add('active');
  // Activate clicked tab
  if (btn) btn.classList.add('active');
}

// On gallery page, check URL param to open correct tab on load
(function() {
  const params = new URLSearchParams(window.location.search);
  const tab = params.get('tab');
  if (tab) {
    const btn = Array.from(document.querySelectorAll('.gallery-tab'))
      .find(b => b.textContent.toLowerCase().replace(/\s+/g,'') === tab.toLowerCase().replace(/\s+/g,''));
    if (btn) switchTab(tab, btn);
  }
})();

// ── LIGHTBOX ──
function openLightbox(item) {
  const img = item.querySelector('img');
  if (!img) return;
  const lightbox = document.getElementById('lightbox');
  const lbImg = document.getElementById('lightbox-img');
  const lbCap = document.getElementById('lightbox-caption');
  lbImg.src = img.src;
  lbImg.alt = img.alt;
  lbCap.textContent = img.dataset.title || '';
  lightbox.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeLightbox(e) {
  if (e && e.target !== e.currentTarget && e.target.id !== 'lightbox') return;
  const lightbox = document.getElementById('lightbox');
  if (lightbox) lightbox.classList.remove('open');
  document.body.style.overflow = '';
}

// Close lightbox with Escape key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeLightbox();
});
