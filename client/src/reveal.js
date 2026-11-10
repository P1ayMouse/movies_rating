import { animate } from 'motion/mini';

// How far an element rises while it fades in, and how long it takes
const OFFSET = 16;
const DURATION = 0.5;
// Gap between items in a list, and the most items that wait for their turn
const STAGGER = 0.05;
const MAX_STAGGER_ITEMS = 12;
// An element starts once its top is above this share of the window height
const START_AT = 0.92;

const prefersReducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const waiting = new Set();
let checkScheduled = false;

function showElement(el) {
  el.revealTimer = setTimeout(() => {
    el.style.removeProperty('opacity');
    el.style.removeProperty('transform');
    animate(
      el,
      { opacity: [0, 1], transform: [`translateY(${OFFSET}px)`, 'translateY(0)'] },
      { duration: DURATION, ease: [0.22, 1, 0.36, 1] }
    ).then(() => {
      // The animation leaves its last values inline. Drop them so hover effects
      // that use transform keep working
      el.style.removeProperty('opacity');
      el.style.removeProperty('transform');
    });
  }, el.revealDelay * 1000);
}

function checkWaiting() {
  checkScheduled = false;
  const limit = window.innerHeight * START_AT;
  for (const el of waiting) {
    if (el.getBoundingClientRect().top < limit) {
      waiting.delete(el);
      showElement(el);
    }
  }
  if (!waiting.size) {
    window.removeEventListener('scroll', scheduleCheck);
    window.removeEventListener('resize', scheduleCheck);
  }
}

function scheduleCheck() {
  if (checkScheduled) return;
  checkScheduled = true;
  requestAnimationFrame(checkWaiting);
}

export const vReveal = {
  mounted(el, binding) {
    if (prefersReducedMotion()) return;

    el.revealDelay = Math.min(Number(binding.value) || 0, MAX_STAGGER_ITEMS) * STAGGER;
    el.style.opacity = '0';
    el.style.transform = `translateY(${OFFSET}px)`;

    if (!waiting.size) {
      window.addEventListener('scroll', scheduleCheck, { passive: true });
      window.addEventListener('resize', scheduleCheck);
    }
    waiting.add(el);
    scheduleCheck();
  },
  unmounted(el) {
    waiting.delete(el);
    clearTimeout(el.revealTimer);
  }
};
