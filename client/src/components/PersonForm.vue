<script>
import router from '../router'
import {
  QCard,
  QCardSection,
  QImg,
  QBtn,
  QTable,
  QTd,
  QSpinnerDots
} from 'quasar'

export default {
  name: 'PersonForm',
  components: {
    QCard,
    QCardSection,
    QImg,
    QBtn,
    QTable,
    QTd,
    QSpinnerDots
  },
  data () {
    return {
      personLoaded: false,
      person: {},
      columns: [
        { name: 'name', required: true, label: 'Name', align: 'left', field: 'name', format: val => `${val}`, sortable: true },
        { name: 'average_rating', align: 'left', label: 'Average Rating', field: 'average_rating', sortable: true },
        { name: 'genres', align: 'left', label: 'Genres', field: 'genres', format: val => val.join('; '), sortable: true }
      ]
    }
  },
  async mounted () {
    this.fetchData()
  },
  watch: {
    '$route'() {
      this.fetchData()
    }
  },
  methods: {
    async fetchData () {
      this.personLoaded = false
      const urlPersonMovie = `/api/v1/movies/persons/${this.$route.params.id}`;

      try {
        const response = await fetch(urlPersonMovie);
        const data = await response.json();

        this.person = data;

        if (this.person.known_for_titles.length > 0) {
          await Promise.all(this.person.known_for_titles.map(async (imdb_id) => {
            const movieUrl = `/api/v1/movies/?search=${imdb_id}`;
            const movieResponse = await fetch(movieUrl);
            const movieData = await movieResponse.json();
            if (movieData.results.length > 0) {
              if (!this.person.knownForMovies) {
                this.person.knownForMovies = [];
              }
              this.person.knownForMovies.push(movieData.results[0]);
            }
          }));
        }

        document.title = `${this.person.name} (${this.person.imdb_id})`;
        this.personLoaded = true;
      } catch (error) {
        console.error(error);
      }
    },
    goToMoviePage(movieId) {
      router.push({ name: 'movie', params: { id: movieId } });
    },
    viewOnIMDb() {
      window.open(`https://www.imdb.com/name/${this.person.imdb_id}`, '_blank');
    },
    formatJob(job) {
      return job.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
    }
  }
};
</script>

<template>
  <div class="q-pa-md">
    <div v-if="!personLoaded">
      <div class="text-center q-my-xl">
        <q-spinner-dots color="black" size="64px" />
      </div>
    </div>
    <div v-else>
      <q-card class="q-ma-md">
        <q-card-section class="person-header">
          <div class="row">
            <div class="col-md-4 person-photo-center text-center">
              <q-img
                  :src="person.photo ? person.photo : '/src/components/icons/none_image.png'"
                  class="person-photo rounded-borders"
                  :ratio="0.67"
                  :img-class="'high-quality'"
              />
            </div>
            <div class="col-md-8 person-details">
              <div class=" text-left q-ml-lg q-mt-md q-mt-none-md">
                <div class="person-title-container">
                  <p class="person-title">{{ person.name }}</p>
                </div>
                <p class="person-year">
                  <span v-if="person.birth_year">{{ person.birth_year ? person.birth_year.slice(0, 4) : '' }}</span>
                  <span v-if="person.death_year && person.birth_year"> - {{ person.death_year.slice(0, 4) }}</span>
                </p>
                <div class="button-container">
                  <q-btn @click="viewOnIMDb" class="styled-button" icon="person" />
                </div>
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <q-card flat class="q-ma-md" v-if="person.knownForMovies && person.knownForMovies.length > 0">
        <q-card-section>
          <q-table :rows="person.knownForMovies" :columns="columns" row-key="name" flat bordered hide-pagination>
            <template v-slot:body-cell-name="props">
              <q-td :props="props" data-label="Name">
                <q-btn flat @click="goToMoviePage(props.row.id)" class="q-ml-sm" style="text-transform: none;">{{ props.row.name }}</q-btn>
              </q-td>
            </template>
            <template v-slot:body-cell-genres="props">
              <q-td :props="props" data-label="Genres">
                {{ props.row.genres.join('; ') }}
              </q-td>
            </template>
          </q-table>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<style scoped>
.person-header {
  background-color: #f5f5f5;
  padding: 16px;
  border-bottom: 1px solid #ddd;
}

.person-title-container {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.person-title {
  font-size: 2.5em;
  margin: 0;
}

.person-year {
  font-size: 1.25em;
  color: rgb(128, 128, 128);
  margin: 0;
}

.person-photo {
  width: 100%;
  max-width: 300px;
  height: auto;
  object-fit: cover;
  border-radius: 10px;
}

.styled-button {
  margin-top: 10px;
  background-color: #6c757d;
  color: white;
  border-radius: 50px;
  padding: 5px 15px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
}

.styled-button:hover {
  background-color: #5a6268;
}

.button-container {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

@media screen and (max-width: 1023.2px) {
  .person-title-container {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .person-title {
    font-size: 28px;
  }

  .person-year {
    text-align: center;
  }

  .button-container {
    justify-content: center;
  }

  .person-photo-center, .person-details {
    width: 100%;
  }
}
</style>
