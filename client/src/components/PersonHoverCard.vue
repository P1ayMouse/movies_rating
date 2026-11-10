<script setup>
import { computed, ref } from 'vue';
import { QTooltip } from 'quasar';
import PosterImage from './PosterImage.vue';
import { yearOf } from '../format.js';

const props = defineProps({
  person: { type: Object, required: true },
  role: { type: String, default: '' },
  movieId: { type: [Number, String], default: null }
});

const knownFor = ref([]);
const knownForLoading = ref(false);

const lifeYears = computed(() => {
  const born = yearOf(props.person.birth_year);
  const died = yearOf(props.person.death_year);
  if (born && died) return `${born}–${died}`;
  if (born) return `Born ${born}`;
  return died ? `Died ${died}` : '';
});

async function loadKnownFor() {
  if (knownFor.value.length || knownForLoading.value) return;
  knownForLoading.value = true;
  const movies = await Promise.all((props.person.known_for_titles || []).map(findMovie));
  knownFor.value = movies
    .filter((movie) => movie && String(movie.id) !== String(props.movieId))
    .slice(0, 3);
  knownForLoading.value = false;
}
</script>

<script>
// Shared by every card on the page, so each title is fetched only once
const movieCache = new Map();

function findMovie(imdbId) {
  if (!movieCache.has(imdbId)) {
    const request = fetch(`/api/v1/movies/?imdb_id=${encodeURIComponent(imdbId)}`)
      .then((response) => (response.ok ? response.json() : null))
      .then((data) => data?.results[0] || null)
      .catch(() => null);
    movieCache.set(imdbId, request);
  }
  return movieCache.get(imdbId);
}
</script>

<template>
  <q-tooltip
    class="person-hover-card"
    anchor="bottom left"
    self="top left"
    :offset="[0, 8]"
    :delay="350"
    transition-show="fade"
    transition-hide="fade"
    @before-show="loadKnownFor"
  >
    <div class="person-hover-card-header">
      <div class="person-hover-card-photo">
        <poster-image :src="person.photo" icon="person" icon-size="24px" />
      </div>
      <div class="person-hover-card-info">
        <p class="person-hover-card-name">{{ person.name }}</p>
        <p v-if="lifeYears" class="person-hover-card-muted">{{ lifeYears }}</p>
        <p v-if="role" class="person-hover-card-role">{{ role }}</p>
      </div>
    </div>

    <div v-if="person.known_for_titles?.length" class="person-hover-card-known">
      <p class="person-hover-card-label">Known for</p>
      <p v-if="knownForLoading" class="person-hover-card-muted">Loading…</p>
      <ul v-else-if="knownFor.length">
        <li v-for="movie in knownFor" :key="movie.id">
          {{ movie.name }}
          <span v-if="movie.year" class="person-hover-card-muted">{{ yearOf(movie.year) }}</span>
        </li>
      </ul>
      <p v-else class="person-hover-card-muted">No other titles in the catalog</p>
    </div>
  </q-tooltip>
</template>
