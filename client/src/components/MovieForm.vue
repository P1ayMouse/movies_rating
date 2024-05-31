<script>
import router from '../router'
import StarRating from 'vue-star-rating'
import {
  QCard,
  QCardSection,
  QImg,
  QBtn,
  QTable,
  QTd,
  QChip,
  QSpinnerDots,
  QToolbar,
  QToolbarTitle,
  QSpace,
  QIcon
} from 'quasar'

export default {
  name: 'MovieForm',
  components: {
    StarRating,
    QCard,
    QCardSection,
    QImg,
    QBtn,
    QTable,
    QTd,
    QChip,
    QSpinnerDots,
    QToolbar,
    QToolbarTitle,
    QSpace,
    QIcon
  },
  data() {
    return {
      dataLoaded: false,
      formError: false,
      fullMovie: {},
      movie: {},
      persons: [],
      rating: {},
      isRatingCardOpen: false,
      isTopThreeVisible: false,
      topThree: [],
      columns: [
        { name: 'name', required: true, label: 'Name', align: 'left', field: row => row.person_id.name, format: val => `${val}`, sortable: true },
        { name: 'age', align: 'left', label: 'Age', field: row => row.person_id.birth_year ? row.person_id.birth_year.slice(0, 4) : '', sortable: true },
        { name: 'job', align: 'left', label: 'Job', field: 'category', format: val => this.formatJob(val), sortable: true },
        { name: 'roles', align: 'left', label: 'Roles', field: 'characters', format: val => val.join('; '), sortable: true }
      ]
    }
  },
  async mounted() {
    await this.fetchData()
  },
  watch: {
    '$route'() {
      this.fetchData()
    }
  },
  methods: {
    async fetchData() {
      this.dataLoaded = false
      const urlMovies = `/api/v1/movies/${this.$route.params.id}/`
      const urlPersonMovie = `/api/v1/movies/personmovies/?limit=100&search=${this.$route.params.id}`
      const urlRating = `/api/v1/movies/ratings/${this.$route.params.id}`

      Promise.all([
        fetch(urlMovies).then(response => response.json()),
        fetch(urlPersonMovie).then(response => response.json()),
        fetch(urlRating).then(response => response.json())
      ]).then(data => {
        const genres = data[0].genres.join(',')

        const urlTopThree = `/api/v1/movies/?limit=3&genres=${genres}&ordering=-rating__num_votes`

        fetch(urlTopThree).then(response => response.json())
            .then(topThreeData => {
              this.movie = data[0]
              this.persons = data[1].results
              this.rating = data[2]
              this.topThree = topThreeData.results

              document.title = `${this.movie.name} (${this.movie.imdb_id})`

              this.dataLoaded = true
            })
            .catch(error => {
              console.error(error)
            })
      }).catch(error => {
        console.error(error)
      })
    },
    onPersonPush(person) {
      router.push({ name: 'person', params: { id: person.person_id.id } })
    },
    toggleRatingCard() {
      this.isRatingCardOpen = !this.isRatingCardOpen
    },
    goToMovie(id) {
      router.push({ name: 'movie', params: { id } })
    },
    formatJob(job) {
      return job.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
    },
    viewOnIMDb() {
      window.open(`https://www.imdb.com/title/${this.movie.imdb_id}`, '_blank')
    }
  }
}
</script>

<template>
  <div class="q-pa-md">
    <div v-if="!dataLoaded">
      <div class="text-center q-my-xl">
        <q-spinner-dots color="black" size="64px" />
      </div>
    </div>
    <div v-else>
      <q-card class="q-ma-md">
        <q-card-section class="movie-header">
          <div class="row">
            <div class="col-12 col-md-4 text-center">
              <q-img
                  :src="(movie.poster && movie.poster !== 'None') ? movie.poster : '/src/components/icons/none_image.png'"
                  class="movie-poster rounded-borders"
                  :ratio="0.67"
                  :img-class="'high-quality'"
              />
              <div class="d-flex align-items-center justify-content-center" style="padding-top: 10px">
                <q-rating
                    v-model="movie.average_rating"
                    max="10"
                    size="2em"
                    color="yellow"
                    icon="star_border"
                    icon-selected="star"
                    icon-half="star_half"
                    readonly
                    class="rating"
                ></q-rating>
              </div>
              <p class="q-mt-sm text-caption" v-if="rating">based on {{ rating.num_votes }} rates</p>
            </div>
            <div class="col-md-8 movie-details">
              <div class="q-mt-md">
                <div class="movie-title-container">
                  <p class="movie-title">{{ movie.name }}</p>
                  <p class="movie-year">({{ movie.year ? movie.year.substring(0, 4) : '' }})</p>
                </div>
                <div class="movie-genres">
                  <span v-for="(genre, index) in movie.genres" :key="index">{{ genre }}{{ index === movie.genres.length - 1 ? '' : ', ' }}</span>
                </div>
                <p class="q-mt-md directors"><strong v-if="movie.directors.length !== 0">Directors:</strong> <span v-for="(director, index) in movie.directors" :key="index">{{ director }}{{ index === movie.directors.length - 1 ? '' : ', ' }}</span></p>
                <div class="button-container">
                  <q-btn @click="toggleRatingCard" class="styled-button q-mr-sm" icon="menu" />
                  <q-btn @click="viewOnIMDb" class="styled-button" icon="movie" />
                </div>
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <q-card flat class="q-ma-md" v-if="persons.length !== 0">
        <q-card-section>
          <q-table :rows="persons" :columns="columns" row-key="name" flat bordered hide-pagination>
            <template v-slot:body-cell-name="props">
              <q-td :props="props" data-label="Name">
                <q-btn flat @click="onPersonPush(props.row)" class="q-ml-sm" style="text-transform: none;">{{ props.row.person_id.name }}</q-btn>
              </q-td>
            </template>
            <template v-slot:body-cell-age="props">
              <q-td :props="props" data-label="Age">
                {{ props.row.person_id.birth_year ? props.row.person_id.birth_year.slice(0, 4) : '' }}
              </q-td>
            </template>
            <template v-slot:body-cell-job="props">
              <q-td :props="props" data-label="Job">
                {{ formatJob(props.row.category) }}
              </q-td>
            </template>
            <template v-slot:body-cell-roles="props">
              <q-td :props="props" data-label="Roles">
                {{ props.row.characters.join('; ') }}
              </q-td>
            </template>
          </q-table>
        </q-card-section>
      </q-card>

      <div v-if="isRatingCardOpen" :class="['rating-card', { open: isRatingCardOpen }]">
        <q-card-section>
          <h5 class="text-center">Top Rated Like This</h5>
          <div :class="['top-rated-container', { open: isTopThreeVisible }]">
            <q-card flat v-for="(movie, index) in topThree" :key="index" class="q-my-sm top-rated-card" @click="goToMovie(movie.id)" style="cursor: pointer;">
              <q-card-section>
                <p class="text-subtitle1"> Number #{{ index + 1}}</p>
                <q-img :src="movie.poster ? movie.poster : '/src/components/icons/none_image.png'" class="rounded-borders q-my-md movie-poster" :alt="movie.name" />
                <p class="text-subtitle1">{{ movie.name }}</p>
                <div class="text-caption">
                  <span v-if="movie.year">{{ movie.year.substring(0, 4) }}</span>
                  <span v-if="movie.year && movie.directors.length !== 0">, </span>
                  <span v-for="(director, index) in movie.directors" :key="index">{{ director }}{{ index === movie.directors.length - 1 ? '' : ', ' }}</span>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </q-card-section>
      </div>

    </div>
  </div>
</template>


<style scoped>
.movie-header {
  background-color: #f5f5f5;
  padding: 16px;
  border-bottom: 1px solid #ddd;
}

.movie-title-container {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.movie-title {
  font-size: 2.5em;
  margin: 0;
}

.movie-year {
  font-size: 1.25em;
  color: rgb(128, 128, 128);
  margin: 0;
}

.movie-genres {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  font-size: 1.2em;
  color: rgb(70, 70, 70);
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}

.directors {
  font-size: 1em;
}

.movie-poster {
  width: 100%;
  max-width: 300px;
  height: auto;
  object-fit: cover;
}

.details p {
  margin: 0.5em 0;
  padding: 0;
}

.details strong {
  font-weight: bold;
}

.rating-card {
  position: fixed;
  top: 60px;
  right: -300px;
  width: 300px;
  height: calc(100% - 50px);
  background-color: white;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  transition: right 0.3s ease;
  z-index: 999;
  overflow-y: auto;
  padding-bottom: 20px;
}

.rating-card.open {
  right: 0;
}

.rating {
  width: 0;
  justify-content: center;
  gap: 0.25rem;
  margin-top: 10px;
  flex-wrap: nowrap;
}

.rounded-borders {
  border-radius: 10px;
}

.button-container {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
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

.top-rated-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 10px;
}

.top-rated-card {
  display: flex;
  flex-direction: column;
  text-align: center;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  width: 100%;
  background-color: #f9f9f9;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.top-rated-card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.top-rated-card .text-subtitle1 {
  font-size: 1.1em;
  margin: 5px 0;
}

.top-rated-card .text-caption {
  font-size: 0.9em;
  color: #555;
}

@media screen and (max-width: 1023.2px) {
  .movie-title-container {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .movie-genres {
    justify-content: center;
  }

  .directors {
    text-align: center;
  }

  .button-container {
    justify-content: center;
  }

  .rating-card {
    width: 100%;
    height: auto;
    position: static;
    transform: none;
    box-shadow: none;
    margin-top: 20px;
  }

  .top-rated-container {
    align-items: center;
  }

  .top-rated-card {
    max-width: 80%;
    margin-bottom: 10px;
  }

  .movie-details {
    width: 100%;
  }

  .rating {
    gap: 0.1rem;
  }
}
</style>
