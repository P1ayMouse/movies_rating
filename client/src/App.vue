<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue';
import SiteSearch from './components/SiteSearch.vue';
import UserBadge from './components/UserBadge.vue';

const searchBox = ref(null);
// Shadow under the header once the page is scrolled
const scrolled = ref(false);

function onScroll() {
  scrolled.value = window.scrollY > 4;
}

// "/" anywhere on the page jumps to the search field
function onKeydown(event) {
  if (event.key !== '/' || event.ctrlKey || event.metaKey || event.altKey) return;
  const target = event.target;
  const typing =
    target.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName);
  if (typing) return;
  event.preventDefault();
  searchBox.value?.focus();
}

onMounted(() => {
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('keydown', onKeydown);
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll);
  window.removeEventListener('keydown', onKeydown);
});
</script>

<template>
  <header class="site-header text-font" :class="{ 'is-scrolled': scrolled }">
    <div class="site-header-inner">
      <router-link :to="{ name: 'movies' }" class="site-logo" aria-label="Diploma MDB home">
        <span class="site-logo-mark" aria-hidden="true">
          <q-icon name="movie" size="20px" />
        </span>
        <span>Diploma <span class="site-logo-accent">MDB</span></span>
      </router-link>

      <SiteSearch ref="searchBox" />

      <div class="site-user">
        <UserBadge />
      </div>
    </div>
  </header>

  <RouterView class="text-font" />
</template>
