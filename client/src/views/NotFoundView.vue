<script setup>
import { ref } from 'vue';
import { QBtn, QIcon } from 'quasar';
import { LOGO_ICON, pageTitle } from '../brand.js';

document.title = pageTitle('Page not found');

// Kernels that pop all the time
const KERNELS = [
  { dx: -70, peak: -120, rot: -200, delay: 0 },
  { dx: 55, peak: -150, rot: 160, delay: 0.35 },
  { dx: -25, peak: -175, rot: 260, delay: 0.7 },
  { dx: 85, peak: -105, rot: -140, delay: 1.05 },
  { dx: -95, peak: -95, rot: 120, delay: 1.4 },
  { dx: 15, peak: -135, rot: -280, delay: 1.75 }
];

// Extra kernels from a click. Each one removes itself when its animation ends
const burst = ref([]);
const shaking = ref(false);
let nextId = 0;

const random = (min, max) => min + Math.random() * (max - min);

function popMore() {
  const handful = Array.from({ length: 12 }, () => ({
    id: nextId++,
    dx: Math.round(random(-170, 170)),
    peak: Math.round(random(-170, -100)),
    rot: Math.round(random(-360, 360)),
    size: Math.round(random(16, 28))
  }));
  burst.value.push(...handful);

  shaking.value = false;
  requestAnimationFrame(() => {
    shaking.value = true;
  });
}

function removeKernel(id) {
  burst.value = burst.value.filter((kernel) => kernel.id !== id);
}

function kernelStyle({ dx, peak, rot, delay = 0, size }) {
  return {
    '--dx': `${dx}px`,
    '--peak': `${peak}px`,
    '--rot': `${rot}deg`,
    // Top of the arc
    '--mid-x': `${Math.round(dx * 0.6)}px`,
    '--mid-rot': `${Math.round(rot * 0.5)}deg`,
    // Where it sits when animations are turned off
    '--rest-x': `${Math.round(dx * 0.4)}px`,
    '--rest-y': `${Math.round(peak * 0.35)}px`,
    '--delay': `${delay}s`,
    ...(size ? { fontSize: `${size}px` } : {})
  };
}
</script>

<template>
  <main class="not-found-page">
    <div class="not-found-stage" aria-hidden="true">
      <span class="not-found-digit">4</span>

      <button
        type="button"
        class="not-found-bucket"
        :class="{ 'is-shaking': shaking }"
        tabindex="-1"
        @click="popMore"
        @animationend.self="shaking = false"
      >
        <span class="not-found-kernels">
          <span
            v-for="(kernel, index) in KERNELS"
            :key="`loop-${index}`"
            class="popcorn-icon not-found-kernel"
            :style="kernelStyle(kernel)"
          />
          <span
            v-for="kernel in burst"
            :key="kernel.id"
            class="popcorn-icon not-found-kernel not-found-kernel--burst"
            :style="kernelStyle(kernel)"
            @animationend="removeKernel(kernel.id)"
          />
        </span>
        <q-icon :name="LOGO_ICON" class="not-found-bucket-icon" />
      </button>

      <span class="not-found-digit">4</span>
    </div>

    <h1>This scene didn't make the final cut</h1>
    <p class="not-found-text">
      The page you're looking for doesn't exist or has moved. Grab some popcorn and pick another
      movie.
    </p>
    <q-btn
      unelevated
      no-caps
      label="Browse movies"
      class="not-found-button"
      :to="{ name: 'movies' }"
    />
    <p class="not-found-hint">Psst… click the bucket.</p>
  </main>
</template>
