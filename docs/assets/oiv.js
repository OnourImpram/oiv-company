// OIV · Two doors: touch support for the door interaction. Progressive: without this file the
// doors still open on pointer hover and on keyboard focus (CSS), and every door is a plain link.
// On touch or pen the first tap on a door opens it (widens it and shows what is inside);
// a second tap on the same door follows its link. Tapping elsewhere or pressing Escape closes it.
// `?door=night` or `?door=day` opens a door on load (deep link, also used for review screenshots).
(() => {
  'use strict';
  const doors = document.querySelector('.doors');
  if (!doors) return;

  const open = (which) => { doors.dataset.open = which || ''; };
  const requested = new URLSearchParams(window.location.search).get('door');
  if (requested === 'night' || requested === 'day') open(requested);

  let viaTouch = false;
  document.addEventListener('pointerdown', (event) => {
    viaTouch = event.pointerType === 'touch' || event.pointerType === 'pen';
    if (viaTouch && !doors.contains(event.target)) open('');
  }, { passive: true });
  document.addEventListener('keydown', (event) => {
    viaTouch = false;
    if (event.key === 'Escape' && doors.dataset.open) open('');
  });

  doors.addEventListener('click', (event) => {
    const door = event.target.closest('[data-door]');
    if (!door || !viaTouch) return;
    const which = door.dataset.door;
    if (doors.dataset.open !== which) {
      event.preventDefault();
      open(which);
    }
  });
})();

// Compact menu (native <details>): Escape closes it and returns focus to its toggle; choosing a link closes it.
(() => {
  'use strict';
  const menu = document.querySelector('details.menu');
  if (!menu) return;
  const toggle = menu.querySelector('summary');
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.open) { menu.open = false; toggle.focus(); }
  });
  menu.addEventListener('click', (event) => { if (event.target.closest('nav a')) menu.open = false; });
})();
