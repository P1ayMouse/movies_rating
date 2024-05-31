<script>
import {useQuasar} from "quasar";

export default {
  name: "ProfileForm",

  data() {
    return {
      user: {
      },
      userLoaded: false,
      formError: null,
    }
  },
  setup() {
    const $q = useQuasar();
    return { $q };
  },
  async mounted() {
    const token = localStorage.getItem('movies_rating-access')
    let user = null

    const response = await fetch('/api/v1/auth/user-info/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.status === 200) {
      user = await response.json()
      document.title = 'Profile of ' + user.username;
    }
    else if (response.status === 403) {
      // try to renew token
      const newTokenResponse = await fetch('/api/v1/auth/refresh/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({'refresh': localStorage.getItem('movies_rating-refresh')})
          }
      )
    }
    else {
      user = {email: 'Error'}
    }

    this.user = user
    this.userLoaded = true
  },
  methods: {
    async onUserEditProfile(e) {
      e.preventDefault();
      this.formError = null;
    },
  }
}
</script>

<template>
  <div class="text-font">
<!--    <div v-if="formError" class="alert alert-danger" role="alert">-->
<!--      {{ formError }}-->
<!--    </div>-->
    <div class="d-flex justify-content-center align-items-center">
      <q-card class="q-pa-md q-ma-md" style="max-width: 400px; width: 100%;">
        <q-card-section class="text-h5 text-center q-mb-md">
          Profile
        </q-card-section>
        <q-form @submit.prevent="onUserEditProfile" class="q-gutter-md">
          <q-input
              outlined
              v-model="user.email"
              placeholder="Input your email"
              type="email"
              label="e-mail"
              readonly
              color="grey"
              class="q-mb-md"
          />
          <q-input
              outlined
              v-model="user.username"
              placeholder="Input your username"
              label="username"
              color="grey"
              class="q-mb-md"
          />
          <q-input
              outlined
              v-model="user.password"
              placeholder="Input your password"
              type="password"
              label="password"
              color="grey"
              class="q-mb-md"
          />
          <q-input
              outlined
              v-model="user.password2"
              placeholder="Repeat your password"
              type="password"
              label="repeat password"
              color="grey"
              class="q-mb-md"
          />
          <div class="text-center">
            <q-btn label="Update" outline type="submit" color="grey" class="form-button q-mb-md"></q-btn>
          </div>
        </q-form>
      </q-card>
    </div>
  </div>
</template>

<style scoped>
.text-font {
  text-decoration: none;
  font-family: 'Comic Sans MS', sans-serif;
}

.form-button {
  border-radius: 5px;
}
</style>