'use strict';

const sidebar = document.querySelector('#sidebar');
const toggle = document.querySelector('.menu-toggle');
const backdrop = document.querySelector('.menu-backdrop');
const mobile = window.matchMedia('(max-width: 768px)');
const sectionLinks = [...document.querySelectorAll('.sidebar-nav a')];
const sections = [...document.querySelectorAll('main > section')];

function setMenu(open, restoreFocus = false) {
  sidebar.classList.toggle('is-open', open);
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  backdrop.hidden = !open;
  document.body.classList.toggle('menu-is-open', open);
  sidebar.inert = mobile.matches && !open;
  if (restoreFocus) toggle.focus();
}

toggle.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  setMenu(open);
});
backdrop.addEventListener('click', () => setMenu(false, true));
mobile.addEventListener('change', () => setMenu(false));
setMenu(false);

document.addEventListener('keydown', (event) => {
  if (!mobile.matches || toggle.getAttribute('aria-expanded') !== 'true') return;
  if (event.key === 'Escape') {
    setMenu(false, true);
    return;
  }
  if (event.key !== 'Tab') return;
  const focusable = [toggle, ...sidebar.querySelectorAll('a[href], button:not([disabled])')];
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
});

// Native fragment links still work without JavaScript. Add focus management
// when a mobile drawer closes, so keyboard users arrive at the chosen section.
document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', () => {
    const target = document.getElementById(link.hash.slice(1));
    if (mobile.matches && toggle.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      if (target) {
        target.setAttribute('tabindex', '-1');
        target.focus({ preventScroll: true });
        target.addEventListener('blur', () => target.removeAttribute('tabindex'), { once: true });
      }
    }
  });
});

let scheduled = false;
function updateActiveSection() {
  const threshold = mobile.matches ? 140 : 125;
  let current = sections[0];
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= threshold) current = section;
  }
  if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 5) {
    current = sections[sections.length - 1];
  }
  for (const link of sectionLinks) {
    if (link.hash === `#${current.id}`) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  }
  scheduled = false;
}
window.addEventListener('scroll', () => {
  if (!scheduled) {
    scheduled = true;
    window.requestAnimationFrame(updateActiveSection);
  }
}, { passive: true });
window.addEventListener('resize', updateActiveSection);
window.addEventListener('load', updateActiveSection);
updateActiveSection();
