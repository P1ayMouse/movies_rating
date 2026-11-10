<script>
import { pageTitle } from '../brand.js';
import { QBtn, QIcon, QSpinnerDots } from 'quasar';
import MovieTile from './MovieTile.vue';
import PosterImage from './PosterImage.vue';
import { yearOf } from '../format.js';

export default {
  name: 'PersonDetails',
  components: { MovieTile, PosterImage, QBtn, QIcon, QSpinnerDots },
  data() {
    return {
      loading: true,
      errorMessage: '',
      personNotFound: false,
      person: {},
      knownFor: [],
      knownForLoading: false,
      knownForError: false,
      requestId: 0
    };
  },
  computed: {
    birthYear() {
      return yearOf(this.person.birth_year);
    },
    deathYear() {
      return yearOf(this.person.death_year);
    }
  },
  mounted() {
    this.fetchData();
  },
  watch: {
    '$route.params.id'(id) {
      if (id) this.fetchData();
    }
  },
  beforeUnmount() {
    this.requestId += 1;
  },
  methods: {
    async fetchData() {
      const requestId = ++this.requestId;
      this.loading = true;
      this.errorMessage = '';
      this.personNotFound = false;
      this.knownFor = [];
      this.knownForError = false;
      document.title = pageTitle('Person');

      try {
        const response = await fetch(`/api/v1/movies/persons/${this.$route.params.id}/`);
        if (requestId !== this.requestId) return;
        if (!response.ok) {
          this.personNotFound = response.status === 404;
          throw new Error('Person request failed');
        }

        const person = await response.json();
        if (requestId !== this.requestId) return;
        this.person = person;
        document.title = pageTitle(person.name);
        this.loading = false;

        await this.loadKnownFor(requestId);
      } catch {
        if (requestId !== this.requestId) return;
        this.errorMessage = this.personNotFound
          ? 'This person could not be found. Browse the catalog to find another one.'
          : 'We could not load this person. Please try again.';
      } finally {
        if (requestId === this.requestId) this.loading = false;
      }
    },
    async loadKnownFor(requestId = this.requestId) {
      this.knownForLoading = true;
      this.knownForError = false;

      try {
        const results = await Promise.all(
          (this.person.known_for_titles || []).map(async (imdbId) => {
            const response = await fetch(`/api/v1/movies/?imdb_id=${encodeURIComponent(imdbId)}`);
            if (!response.ok) throw new Error('Known for request failed');
            const data = await response.json();
            return data.results[0];
          })
        );
        if (requestId === this.requestId) this.knownFor = results.filter(Boolean);
      } catch {
        if (requestId === this.requestId) this.knownForError = true;
      } finally {
        if (requestId === this.requestId) this.knownForLoading = false;
      }
    }
  }
};
</script>

<template>
  <div class="detail-page person-page">
    <router-link :to="{ name: 'movies' }" class="detail-back-link">
      <q-icon name="arrow_back" size="18px" aria-hidden="true" />
      Back to movies
    </router-link>

    <div v-if="loading" class="detail-status" role="status">
      <q-spinner-dots color="grey-8" size="40px" aria-hidden="true" />
      <p>Loading person details…</p>
    </div>

    <div v-else-if="errorMessage" class="detail-status" role="alert">
      <h1>{{ personNotFound ? 'Person not found' : 'Unable to load person' }}</h1>
      <p>{{ errorMessage }}</p>
      <q-btn v-if="!personNotFound" outline no-caps label="Try again" @click="fetchData" />
    </div>

    <template v-else>
      <section v-reveal class="detail-overview" aria-labelledby="person-name">
        <div class="detail-summary">
          <div class="detail-heading">
            <h1 id="person-name" class="detail-title">{{ person.name }}</h1>
          </div>

          <div class="detail-meta">
            <dl v-if="birthYear || deathYear" class="detail-facts person-facts">
              <div v-if="birthYear">
                <dt>Born</dt>
                <dd>{{ birthYear }}</dd>
              </div>
              <div v-if="deathYear">
                <dt>Died</dt>
                <dd>{{ deathYear }}</dd>
              </div>
            </dl>
          </div>

          <div v-if="person.imdb_id" class="detail-actions">
            <q-btn
              class="detail-imdb-button"
              unelevated
              no-caps
              label="View on IMDb"
              icon-right="open_in_new"
              :href="`https://www.imdb.com/name/${person.imdb_id}/`"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="View on IMDb (opens in a new tab)"
            />
          </div>
        </div>

        <div class="detail-media">
          <poster-image
            :src="person.photo"
            :alt="`Photo of ${person.name}`"
            icon="person"
            label="Photo unavailable"
          />
        </div>
      </section>

      <section v-reveal class="detail-section" aria-labelledby="known-for-title">
        <h2 id="known-for-title">Known for</h2>
        <p class="detail-section-description">Best-known titles that are in this catalog.</p>

        <p v-if="knownForLoading" class="detail-section-message" role="status">Loading movies…</p>
        <div v-else-if="knownForError" class="detail-section-message" role="status">
          <p>Movies could not be loaded.</p>
          <q-btn flat no-caps label="Try again" @click="loadKnownFor()" />
        </div>
        <div v-else-if="knownFor.length" class="movie-tiles">
          <movie-tile
            v-for="(movie, index) in knownFor"
            :key="movie.id"
            v-reveal="index"
            :movie="movie"
          />
        </div>
        <p v-else class="detail-section-message">
          None of {{ person.name }}'s best-known titles are in the catalog yet.
        </p>
      </section>
    </template>
  </div>
</template>
