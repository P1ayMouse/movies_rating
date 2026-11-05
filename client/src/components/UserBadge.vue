<script>
import { authState, clearTokens, loadCurrentUser } from '@/auth'

export default {
  name: "UserBadge",
  computed: {
    user() {
      return authState.user
    },
    userLoaded() {
      return authState.loaded
    },
    loadError() {
      return authState.error
    }
  },
  mounted() {
    loadCurrentUser()
  },
  methods: {
    doLogOut() {
      clearTokens()
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
    },
    retryLoad() {
      loadCurrentUser()
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
  <div v-else-if="loadError" class="text-font">
    <q-btn
        flat
        color="negative"
        no-caps
        icon="error_outline"
        label="Retry"
        @click="retryLoad"
    >
      <q-tooltip>{{ loadError }}</q-tooltip>
    </q-btn>
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