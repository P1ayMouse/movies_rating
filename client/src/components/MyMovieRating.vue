<script setup>
import { computed, onBeforeUnmount, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { authFetch, authState, ensureUserLoaded } from '../auth.js';
import { errorMessage } from '../errors.js';
import PopcornRating from './PopcornRating.vue';

const props = defineProps({
  movieId: { type: [Number, String], required: true }
});
const emit = defineEmits(['totals']);

const route = useRoute();
const user = computed(() => authState.user);
const loginLink = computed(() => ({ name: 'login', query: { next: route.fullPath } }));

// 1-10, or null when the user has not rated the movie
const score = ref(null);
const loading = ref(false);
const saving = ref(false);
const error = ref('');

// Answers that arrive after the movie changed or the page closed are ignored
let requestId = 0;
const url = () => `/api/v1/movies/${props.movieId}/my-rating/`;

function apply(data) {
  score.value = data.score;
  emit('totals', { average_rating: data.average_rating, num_votes: data.num_votes });
}

async function load() {
  const id = ++requestId;
  score.value = null;
  error.value = '';
  if (!(await ensureUserLoaded()) || id !== requestId) return;

  loading.value = true;
  try {
    const response = await authFetch(url());
    if (!response.ok) throw new Error('Rating request failed');
    const data = await response.json();
    if (id === requestId) apply(data);
  } catch {
    if (id === requestId) error.value = 'Your rating could not be loaded.';
  } finally {
    if (id === requestId) loading.value = false;
  }
}

// A score of null removes the rating. The new score shows at once and is put back if saving fails
async function save(newScore) {
  const id = requestId;
  const previous = score.value;
  score.value = newScore;
  saving.value = true;
  error.value = '';
  try {
    const response = await authFetch(url(), {
      method: newScore ? 'PUT' : 'DELETE',
      body: newScore ? JSON.stringify({ score: newScore }) : undefined
    });
    if (id !== requestId) return;
    if (response.ok) {
      apply(await response.json());
      return;
    }
    score.value = previous;
    error.value =
      response.status === 403
        ? 'Your session has ended. Please log in again to rate.'
        : await errorMessage(response);
  } catch {
    if (id !== requestId) return;
    score.value = previous;
    error.value = 'Your rating could not be saved. Please try again.';
  } finally {
    if (id === requestId) saving.value = false;
  }
}

watch(() => props.movieId, load, { immediate: true });
// Logging out (or an expired session) hides the score
watch(user, (current) => {
  if (!current) score.value = null;
});
onBeforeUnmount(() => {
  requestId += 1;
});
</script>

<template>
  <div class="movie-my-rating">
    <p id="my-rating-label" class="movie-score-label">Your rating</p>
    <template v-if="user">
      <popcorn-rating
        :model-value="score"
        :disabled="loading || saving"
        labelledby="my-rating-label"
        @update:model-value="save"
      />
      <p class="movie-my-rating-hint" role="status">
        <template v-if="loading">Loading your rating…</template>
        <template v-else-if="saving">Saving…</template>
        <template v-else-if="score">
          Thanks for rating!
          <button type="button" class="movie-my-rating-remove" @click="save(null)">
            Remove rating
          </button>
        </template>
        <template v-else>Pick from 1 to 10 popcorn buckets.</template>
      </p>
      <p v-if="error" class="movie-my-rating-error" role="alert">{{ error }}</p>
    </template>
    <p v-else class="movie-my-rating-hint">
      <router-link :to="loginLink">Log in</router-link> to rate this movie.
    </p>
  </div>
</template>
