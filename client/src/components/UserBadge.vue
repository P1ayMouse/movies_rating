<script>
import { authState, clearTokens, loadCurrentUser } from '@/auth';

export default {
  name: 'UserBadge',
  computed: {
    user() {
      return authState.user;
    },
    userLoaded() {
      return authState.loaded;
    },
    loadError() {
      return authState.error;
    },
    displayName() {
      return this.user.username || this.user.email;
    },
    initial() {
      return (this.displayName || '?').charAt(0).toUpperCase();
    }
  },
  mounted() {
    loadCurrentUser();
  },
  methods: {
    doLogOut() {
      clearTokens();
      this.$router.push({ name: 'login' });
    },
    retryLoad() {
      loadCurrentUser();
    }
  }
};
</script>

<template>
  <!-- Same size as the avatar, so the header does not jump when the user loads -->
  <div v-if="!userLoaded" class="user-badge-loading" role="status" aria-label="Loading account">
    <span class="user-badge-avatar user-badge-avatar--empty" />
  </div>

  <q-btn-dropdown
    v-else-if="user !== null"
    flat
    no-caps
    class="user-badge-button"
    dropdown-icon="expand_more"
    content-class="user-badge-menu"
    :menu-offset="[0, 8]"
    menu-anchor="bottom right"
    menu-self="top right"
    auto-close
  >
    <template #label>
      <span class="user-badge-avatar" aria-hidden="true">{{ initial }}</span>
      <span class="user-badge-name">{{ displayName }}</span>
    </template>

    <q-list>
      <q-item :to="{ name: 'profile' }" clickable>
        <q-item-section avatar>
          <q-icon name="person_outline" size="20px" />
        </q-item-section>
        <q-item-section>Edit account</q-item-section>
      </q-item>
      <q-separator />
      <q-item clickable @click="doLogOut">
        <q-item-section avatar>
          <q-icon name="logout" size="20px" />
        </q-item-section>
        <q-item-section>Log out</q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>

  <q-btn
    v-else-if="loadError"
    flat
    no-caps
    color="negative"
    icon="error_outline"
    label="Retry"
    @click="retryLoad"
  >
    <q-tooltip>{{ loadError }}</q-tooltip>
  </q-btn>

  <div v-else class="user-badge-guest">
    <router-link :to="{ name: 'register' }" class="user-badge-signup">Sign up</router-link>
    <router-link :to="{ name: 'login' }" class="user-badge-login">Log in</router-link>
  </div>
</template>
