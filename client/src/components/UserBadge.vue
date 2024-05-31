<script>
export default {
  name: "UserBadge",
  data() {
    return {
      user: null,
      userLoaded: false
    }
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
    }
    else if (response.status === 403) {
      const newTokenResponse = await fetch('/api/v1/auth/refresh/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({'refresh': localStorage.getItem('movies_rating-refresh')})
          }
      )
      if (newTokenResponse.status === 200 ) {
        localStorage.setItem('movies_rating-access', (await newTokenResponse.json()).access)
        const retryResponse = await fetch('/api/v1/auth/user-info/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('movies_rating-access')}`,
            'Content-Type': 'application/json'
          }
        })

        if (retryResponse.status === 200) {
          user = await retryResponse.json()
        }
      } else {
        localStorage.removeItem('movies_rating-access')
        localStorage.removeItem('movies_rating-refresh')
      }
    } else {
      user = { email: 'Error' }
    }

    this.user = user
    this.userLoaded = true
  },
  methods: {
    doLogOut() {
      localStorage.removeItem('movies_rating-access')
      localStorage.removeItem('movies_rating-refresh')
      this.user = null
      this.$router.push('/login')
    },
    doEditAccount() {
      this.$router.push('/profile')
    },
    doMoviesList() {
      this.$router.push('/movies')
    },
    goToLogin() {
      this.$router.push('/login')
    }
  }
}
</script>

<template>
  <div v-if="!userLoaded" class="text-font">
    <q-spinner-dots color="black" size="64px" />
  </div>
  <div v-else-if="user !== null">
    <q-btn-dropdown
        flat
        color="black"
        no-caps
        class="user-dropdown"
    >
      <template v-slot:label>
        <q-icon name="account_circle" size="md" class="q-mr-sm" />
        {{ user.username }}
      </template>
      <q-list style="min-width: 150px; overflow: hidden;">
        <q-item clickable v-ripple @click="doEditAccount">
          <q-item-section> Edit Account </q-item-section>
        </q-item>
        <q-item clickable v-ripple @click="doMoviesList">
          <q-item-section> Movies List </q-item-section>
        </q-item>
        <q-separator color="black" inset></q-separator>
        <q-item clickable v-ripple @click="doLogOut">
          <q-item-section> Log Out </q-item-section>
        </q-item>
      </q-list>
    </q-btn-dropdown>
  </div>
  <div v-else class="text-font">
    <q-btn
        flat
        color="primary"
        no-caps
        label="Login"
        @click="goToLogin"
    />
  </div>
</template>

<style scoped>
.user-dropdown {
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.q-btn-dropdown__menu {
  overflow-x: hidden;
}
</style>