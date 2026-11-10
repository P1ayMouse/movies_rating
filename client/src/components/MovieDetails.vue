<script>
import { pageTitle } from '../brand.js';
import { QBtn, QIcon, QSpinnerDots, QTable, QTd } from 'quasar';
import MovieTile from './MovieTile.vue';
import PersonHoverCard from './PersonHoverCard.vue';
import PosterImage from './PosterImage.vue';
import { creditRole, formatJob, formatRating, yearOf } from '../format.js';

export default {
  name: 'MovieDetails',
  components: {
    MovieTile,
    PersonHoverCard,
    PosterImage,
    QBtn,
    QIcon,
    QSpinnerDots,
    QTable,
    QTd
  },
  data() {
    return {
      loading: true,
      errorMessage: '',
      movieNotFound: false,
      movie: {},
      people: [],
      peopleLoading: false,
      peopleError: false,
      similarMovies: [],
      similarLoading: false,
      similarError: false,
      requestId: 0,
      // Person cards on hover only make sense with a mouse, not on touch screens
      canHover: window.matchMedia('(hover: hover) and (pointer: fine)').matches,
      columns: [
        {
          name: 'name',
          label: 'Name',
          align: 'left',
          field: (row) => row.person_id.name,
          sortable: true
        },
        {
          name: 'job',
          label: 'Contribution',
          align: 'left',
          field: 'category',
          format: formatJob,
          sortable: true
        },
        {
          name: 'roles',
          label: 'Character',
          align: 'left',
          field: 'characters',
          format: (value) => value?.join(', ') || '—'
        }
      ]
    };
  },
  computed: {
    releaseYear() {
      return yearOf(this.movie.year);
    },
    voteCount() {
      return new Intl.NumberFormat('en').format(this.movie.num_votes || 0);
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
      this.movieNotFound = false;
      this.people = [];
      this.similarMovies = [];
      this.peopleError = false;
      this.similarError = false;
      document.title = pageTitle('Movie details');

      try {
        const response = await fetch(`/api/v1/movies/${this.$route.params.id}/`);
        if (requestId !== this.requestId) return;
        if (!response.ok) {
          this.movieNotFound = response.status === 404;
          throw new Error('Movie request failed');
        }

        const movie = await response.json();
        if (requestId !== this.requestId) return;
        this.movie = movie;
        document.title = pageTitle(
          this.releaseYear ? `${movie.name} (${this.releaseYear})` : movie.name
        );
        this.loading = false;

        await Promise.all([this.loadPeople(requestId), this.loadSimilarMovies(requestId)]);
      } catch {
        if (requestId !== this.requestId) return;
        this.errorMessage = this.movieNotFound
          ? 'This movie could not be found. Browse the catalog to find another film.'
          : 'We could not load this movie. Please try again.';
      } finally {
        if (requestId === this.requestId) this.loading = false;
      }
    },
    async loadPeople(requestId = this.requestId) {
      this.peopleLoading = true;
      this.peopleError = false;

      try {
        const response = await fetch(
          `/api/v1/movies/personmovies/?limit=100&movie_id__id=${this.movie.id}`
        );
        if (!response.ok) throw new Error('Cast request failed');
        const data = await response.json();
        if (requestId === this.requestId) this.people = data.results;
      } catch {
        if (requestId === this.requestId) this.peopleError = true;
      } finally {
        if (requestId === this.requestId) this.peopleLoading = false;
      }
    },
    async loadSimilarMovies(requestId = this.requestId) {
      this.similarLoading = true;
      this.similarError = false;

      try {
        if (!this.movie.genres?.length) return;
        const movieId = this.movie.id;
        const params = new URLSearchParams({
          limit: '4',
          genres: this.movie.genres.join(','),
          ordering: '-rating__num_votes'
        });
        const response = await fetch(`/api/v1/movies/?${params}`);
        if (!response.ok) throw new Error('Similar movies request failed');
        const data = await response.json();
        if (requestId === this.requestId) {
          this.similarMovies = data.results
            .filter((movie) => String(movie.id) !== String(movieId))
            .slice(0, 3);
        }
      } catch {
        if (requestId === this.requestId) this.similarError = true;
      } finally {
        if (requestId === this.requestId) this.similarLoading = false;
      }
    },
    creditRole,
    formatRating
  }
};
</script>

<template>
  <div class="detail-page movie-page">
    <router-link :to="{ name: 'movies' }" class="detail-back-link">
      <q-icon name="arrow_back" size="18px" aria-hidden="true" />
      Back to movies
    </router-link>

    <div v-if="loading" class="detail-status" role="status">
      <q-spinner-dots color="grey-8" size="40px" aria-hidden="true" />
      <p>Loading movie details…</p>
    </div>

    <div v-else-if="errorMessage" class="detail-status" role="alert">
      <h1>{{ movieNotFound ? 'Movie not found' : 'Unable to load movie' }}</h1>
      <p>{{ errorMessage }}</p>
      <q-btn v-if="!movieNotFound" outline no-caps label="Try again" @click="fetchData" />
    </div>

    <template v-else>
      <section class="detail-overview" aria-labelledby="movie-title">
        <div class="detail-summary">
          <div class="detail-heading">
            <p v-if="releaseYear" class="detail-overline">{{ releaseYear }}</p>
            <h1 id="movie-title" class="detail-title">{{ movie.name }}</h1>
          </div>

          <div class="detail-meta">
            <ul v-if="movie.genres?.length" class="movie-genres" aria-label="Genres">
              <li v-for="genre in movie.genres" :key="genre">{{ genre }}</li>
            </ul>

            <div class="movie-score">
              <p class="movie-score-label">Rating</p>
              <div v-if="formatRating(movie.average_rating)" class="movie-score-value">
                <q-icon class="popcorn-icon" aria-hidden="true" />
                <span class="movie-score-number">{{ formatRating(movie.average_rating) }}</span>
                <span class="movie-score-scale">/ 10</span>
              </div>
              <p v-else class="movie-unrated">Not yet rated</p>
              <p class="movie-votes">
                {{ Number(movie.num_votes) > 0 ? `${voteCount} votes` : 'No votes yet' }}
              </p>
            </div>
          </div>

          <dl v-if="movie.directors?.length" class="detail-facts">
            <dt>{{ movie.directors.length === 1 ? 'Director' : 'Directors' }}</dt>
            <dd>{{ movie.directors.join(', ') }}</dd>
          </dl>

          <div v-if="movie.imdb_id" class="detail-actions">
            <q-btn
              class="detail-imdb-button"
              unelevated
              no-caps
              label="View on IMDb"
              icon-right="open_in_new"
              :href="`https://www.imdb.com/title/${movie.imdb_id}/`"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="View on IMDb (opens in a new tab)"
            />
          </div>
        </div>

        <div class="detail-media">
          <poster-image
            :src="movie.poster"
            :alt="`Poster for ${movie.name}`"
            label="Poster unavailable"
          />
        </div>
      </section>

      <section
        v-if="peopleLoading || peopleError || people.length"
        class="detail-section"
        aria-labelledby="movie-credits-title"
      >
        <h2 id="movie-credits-title">Cast &amp; crew</h2>
        <p v-if="peopleLoading" class="detail-section-message" role="status">
          Loading cast &amp; crew…
        </p>
        <div v-else-if="peopleError" class="detail-section-message" role="status">
          <p>Cast &amp; crew could not be loaded.</p>
          <q-btn flat no-caps label="Try again" @click="loadPeople()" />
        </div>
        <q-table
          v-else
          class="movie-credits"
          :rows="people"
          :columns="columns"
          :pagination="{ rowsPerPage: 10 }"
          :rows-per-page-options="[10, 25, 50]"
          :hide-pagination="people.length <= 10"
          row-key="id"
          flat
          bordered
          wrap-cells
        >
          <template #body-cell-name="props">
            <q-td :props="props">
              <router-link
                :to="{ name: 'person', params: { id: props.row.person_id.id } }"
                class="movie-person-link"
              >
                {{ props.row.person_id.name }}
                <person-hover-card
                  v-if="canHover"
                  :person="props.row.person_id"
                  :role="creditRole(props.row)"
                  :movie-id="movie.id"
                />
              </router-link>
            </q-td>
          </template>
        </q-table>
      </section>

      <section id="similar-movies" class="detail-section" aria-labelledby="similar-movies-title">
        <h2 id="similar-movies-title">Similar movies</h2>
        <p class="detail-section-description">Popular picks in the same genres.</p>

        <p v-if="similarLoading" class="detail-section-message" role="status">
          Finding similar movies…
        </p>
        <div v-else-if="similarError" class="detail-section-message" role="status">
          <p>Similar movies could not be loaded.</p>
          <q-btn flat no-caps label="Try again" @click="loadSimilarMovies()" />
        </div>
        <div v-else-if="similarMovies.length" class="movie-tiles">
          <movie-tile
            v-for="similarMovie in similarMovies"
            :key="similarMovie.id"
            :movie="similarMovie"
          />
        </div>
        <p v-else class="detail-section-message">No similar movies are available yet.</p>
      </section>
    </template>
  </div>
</template>
