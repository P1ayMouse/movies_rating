<script setup>
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import UserBadge from './components/UserBadge.vue';

const route = useRoute();
const router = useRouter();
const search = ref('');

// Keep the current query in the box on search pages, clear it everywhere else
watch(
  () => route.params.search,
  (value) => {
    search.value = value || '';
  },
  { immediate: true }
);

function onMovieSearch() {
  const query = search.value.trim();
  if (query) router.push({ name: 'movies-search', params: { search: query } });
}
</script>

<template>
  <header class="site-header text-font">
    <div class="site-header-inner">
      <router-link :to="{ name: 'movies' }" class="site-logo" aria-label="Diploma MDB home">
        <span class="site-logo-mark" aria-hidden="true">
          <q-icon name="movie" size="20px" />
        </span>
        <span>Diploma <span class="site-logo-accent">MDB</span></span>
      </router-link>

      <form class="site-search" role="search" @submit.prevent="onMovieSearch">
        <input
          v-model="search"
          type="search"
          placeholder="Search movies"
          aria-label="Search movies"
          class="site-search-input"
        />
        <button type="submit" class="site-search-button" aria-label="Search">
          <q-icon name="search" size="20px" />
        </button>
      </form>

      <div class="site-user">
        <UserBadge />
      </div>
    </div>
  </header>

  <RouterView class="text-font" />
</template>
