<script setup>
import { computed, onBeforeUnmount, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { QIcon } from 'quasar';
import PosterImage from './PosterImage.vue';
import { formatRating, yearOf } from '../format.js';

const MIN_LENGTH = 2;
const DEBOUNCE_MS = 250;

const route = useRoute();
const router = useRouter();

const input = ref(null);
const query = ref('');
const suggestions = ref([]);
const loading = ref(false);
const open = ref(false);
const activeIndex = ref(-1);

let timer = null;
let requestId = 0;

const trimmed = computed(() => query.value.trim());
const seeAllIndex = computed(() => suggestions.value.length);
const showList = computed(() => open.value && trimmed.value.length >= MIN_LENGTH);
const activeId = computed(() =>
  showList.value && activeIndex.value >= 0 ? `site-search-option-${activeIndex.value}` : undefined
);

// After any navigation: close the list, keep the query only on search pages
watch(
  () => route.fullPath,
  () => {
    query.value = route.params.search || '';
    close();
  },
  { immediate: true }
);

function onInput() {
  open.value = true;
  activeIndex.value = -1;
  clearTimeout(timer);
  if (trimmed.value.length < MIN_LENGTH) {
    suggestions.value = [];
    loading.value = false;
    return;
  }
  loading.value = true;
  timer = setTimeout(loadSuggestions, DEBOUNCE_MS);
}

async function loadSuggestions() {
  const id = ++requestId;
  const params = new URLSearchParams({
    search: trimmed.value,
    limit: '5',
    ordering: '-rating__num_votes'
  });
  try {
    const response = await fetch(`/api/v1/movies/?${params}`);
    const data = response.ok ? await response.json() : { results: [] };
    if (id === requestId) suggestions.value = data.results;
  } catch {
    if (id === requestId) suggestions.value = [];
  } finally {
    if (id === requestId) loading.value = false;
  }
}

function close() {
  open.value = false;
  activeIndex.value = -1;
}

function clear() {
  query.value = '';
  suggestions.value = [];
  close();
  input.value?.focus();
}

function openMovie(movie) {
  router.push({ name: 'movie', params: { id: movie.id } });
  input.value?.blur();
}

function submit() {
  const movie = suggestions.value[activeIndex.value];
  if (showList.value && movie) {
    openMovie(movie);
    return;
  }
  if (trimmed.value) {
    router.push({ name: 'movies-search', params: { search: trimmed.value } });
    input.value?.blur();
  }
}

function move(step) {
  if (!showList.value) {
    open.value = true;
    return;
  }
  const last = seeAllIndex.value;
  let next = activeIndex.value + step;
  if (next > last) next = -1;
  if (next < -1) next = last;
  activeIndex.value = next;
}

function onEscape() {
  if (showList.value) close();
  else input.value?.blur();
}

function focus() {
  input.value?.focus();
}

onBeforeUnmount(() => clearTimeout(timer));

defineExpose({ focus });
</script>

<template>
  <form class="site-search" role="search" @submit.prevent="submit">
    <input
      ref="input"
      v-model="query"
      type="search"
      placeholder="Search movies"
      aria-label="Search movies"
      autocomplete="off"
      role="combobox"
      aria-autocomplete="list"
      aria-controls="site-search-list"
      :aria-expanded="showList"
      :aria-activedescendant="activeId"
      class="site-search-input"
      @input="onInput"
      @focus="open = true"
      @blur="close"
      @keydown.down.prevent="move(1)"
      @keydown.up.prevent="move(-1)"
      @keydown.esc.prevent="onEscape"
    />

    <button
      v-if="query"
      type="button"
      class="site-search-button"
      aria-label="Clear search"
      @click="clear"
    >
      <q-icon name="close" size="18px" />
    </button>
    <button type="submit" class="site-search-button" aria-label="Search">
      <q-icon name="search" size="20px" />
    </button>

    <ul
      v-show="showList"
      id="site-search-list"
      class="site-search-list"
      role="listbox"
      aria-label="Suggested movies"
      @mousedown.prevent
    >
      <li v-if="loading && !suggestions.length" class="site-search-message">Searching…</li>
      <li v-else-if="!suggestions.length" class="site-search-message">No movies found</li>

      <li
        v-for="(movie, index) in suggestions"
        :id="`site-search-option-${index}`"
        :key="movie.id"
        role="option"
        :aria-selected="index === activeIndex"
        class="site-search-option"
        :class="{ 'is-active': index === activeIndex }"
        @mouseenter="activeIndex = index"
        @click="openMovie(movie)"
      >
        <span class="site-search-poster">
          <poster-image :src="movie.poster" icon-size="16px" />
        </span>
        <span class="site-search-option-text">
          <span class="site-search-option-title">{{ movie.name }}</span>
          <span class="site-search-option-meta">
            {{ yearOf(movie.year) }}
            <template v-if="formatRating(movie.average_rating)">
              · <q-icon name="star" size="13px" class="site-search-star" />
              {{ formatRating(movie.average_rating) }}
            </template>
          </span>
        </span>
      </li>

      <li
        :id="`site-search-option-${seeAllIndex}`"
        role="option"
        :aria-selected="activeIndex === seeAllIndex"
        class="site-search-option site-search-all"
        :class="{ 'is-active': activeIndex === seeAllIndex }"
        @mouseenter="activeIndex = seeAllIndex"
        @click="submit"
      >
        <q-icon name="search" size="18px" />
        See all results for “{{ trimmed }}”
      </li>
    </ul>
  </form>
</template>
