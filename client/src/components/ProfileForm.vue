<script>
import { QBtn, QIcon, QInput, QSpinnerDots, useQuasar } from 'quasar';
import PasswordInput from './PasswordInput.vue';
import { pageTitle } from '../brand.js';
import { authFetch, authState, clearTokens } from '@/auth';
import { errorMessage } from '@/errors';

const MIN_LENGTH = 6;

export default {
  name: 'ProfileForm',
  components: { PasswordInput, QBtn, QIcon, QInput, QSpinnerDots },
  setup() {
    return { $q: useQuasar() };
  },
  data() {
    return {
      loading: true,
      loadError: '',
      user: {},
      // Account details form
      username: '',
      savingDetails: false,
      detailsError: '',
      // Password form
      password: '',
      password2: '',
      savingPassword: false,
      passwordError: ''
    };
  },
  computed: {
    displayName() {
      return this.user.username || this.user.email || '';
    },
    initial() {
      return (this.displayName || '?').charAt(0).toUpperCase();
    },
    detailsChanged() {
      return this.username.trim() !== (this.user.username || '');
    },
    passwordReady() {
      return Boolean(this.password && this.password2);
    }
  },
  mounted() {
    this.loadUser();
  },
  methods: {
    async loadUser() {
      this.loading = true;
      this.loadError = '';
      try {
        const response = await authFetch('/api/v1/auth/user-info/');
        if (response.status === 403) {
          // The session could not be renewed, so log in again
          this.$router.push({ name: 'login', query: { next: '/profile/' } });
          return;
        }
        if (!response.ok) throw new Error(`Server error ${response.status}`);
        this.setUser(await response.json());
      } catch {
        this.loadError = 'We could not load your profile. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    setUser(user) {
      this.user = user;
      this.username = user.username || '';
      authState.user = { ...user };
      document.title = pageTitle(this.displayName ? `Profile of ${this.displayName}` : 'Profile');
    },
    // Sends a PATCH and returns the error text, or '' on success
    async patchUser(body) {
      let response;
      try {
        response = await authFetch('/api/v1/auth/user-info/', {
          method: 'PATCH',
          body: JSON.stringify(body)
        });
      } catch {
        return 'Network error. Please try again.';
      }
      if (response.status === 403) {
        this.$router.push({ name: 'login', query: { next: '/profile/' } });
        return '';
      }
      if (!response.ok) return errorMessage(response);
      this.setUser(await response.json());
      return '';
    },
    resetDetails() {
      this.username = this.user.username || '';
      this.detailsError = '';
    },
    async saveDetails() {
      this.detailsError = '';
      if (this.username.trim().length < MIN_LENGTH) {
        this.detailsError = `Username must be at least ${MIN_LENGTH} characters.`;
        return;
      }
      this.savingDetails = true;
      this.detailsError = await this.patchUser({ username: this.username.trim() });
      this.savingDetails = false;
      if (!this.detailsError) this.notifySaved('Profile updated');
    },
    async savePassword() {
      this.passwordError = '';
      if (this.password.length < MIN_LENGTH) {
        this.passwordError = `Password must be at least ${MIN_LENGTH} characters.`;
        return;
      }
      if (this.password !== this.password2) {
        this.passwordError = 'Passwords do not match.';
        return;
      }
      this.savingPassword = true;
      this.passwordError = await this.patchUser({
        password: this.password,
        password2: this.password2
      });
      this.savingPassword = false;
      if (!this.passwordError) {
        this.password = '';
        this.password2 = '';
        this.notifySaved('Password changed');
      }
    },
    notifySaved(message) {
      this.$q.notify({ message, color: 'positive', position: 'top', timeout: 2000 });
    },
    logOut() {
      clearTokens();
      this.$router.push({ name: 'login' });
    }
  }
};
</script>

<template>
  <div class="profile-page">
    <div v-if="loading" class="profile-status" role="status">
      <q-spinner-dots color="grey-8" size="40px" aria-hidden="true" />
      <p>Loading your profile…</p>
    </div>

    <div v-else-if="loadError" class="profile-status" role="alert">
      <h1>Unable to load profile</h1>
      <p>{{ loadError }}</p>
      <q-btn outline no-caps label="Try again" @click="loadUser" />
    </div>

    <template v-else>
      <header class="profile-header">
        <span class="profile-avatar" aria-hidden="true">{{ initial }}</span>
        <div class="profile-identity">
          <h1>{{ displayName }}</h1>
          <p v-if="user.username">{{ user.email }}</p>
        </div>
        <q-btn class="profile-logout" flat no-caps icon="logout" label="Log out" @click="logOut" />
      </header>

      <section class="profile-card" aria-labelledby="profile-details-title">
        <div class="profile-card-intro">
          <h2 id="profile-details-title">Account details</h2>
          <p>Your username is shown in the header.</p>
        </div>

        <form class="profile-fields" novalidate @submit.prevent="saveDetails">
          <q-input :model-value="user.email" outlined readonly label="Email">
            <template #append>
              <q-icon name="lock_outline" size="18px" />
            </template>
          </q-input>

          <q-input
            v-model="username"
            outlined
            label="Username"
            autocomplete="username"
            maxlength="150"
          />

          <p v-if="detailsError" class="profile-error" role="alert">
            <q-icon name="error_outline" size="18px" aria-hidden="true" />
            {{ detailsError }}
          </p>

          <div class="profile-actions">
            <q-btn
              v-if="detailsChanged"
              flat
              no-caps
              label="Cancel"
              class="profile-button-secondary"
              @click="resetDetails"
            />
            <q-btn
              type="submit"
              unelevated
              no-caps
              label="Save changes"
              class="profile-button"
              :disable="!detailsChanged"
              :loading="savingDetails"
            />
          </div>
        </form>
      </section>

      <section class="profile-card" aria-labelledby="profile-password-title">
        <div class="profile-card-intro">
          <h2 id="profile-password-title">Change password</h2>
          <p>Pick a new password you don't use anywhere else.</p>
        </div>

        <form class="profile-fields" novalidate @submit.prevent="savePassword">
          <!-- Lets password managers link the new password to this account -->
          <input
            :value="user.email"
            type="email"
            autocomplete="username"
            class="profile-hidden-username"
            tabindex="-1"
            aria-hidden="true"
            readonly
          />

          <password-input v-model="password" label="New password" autocomplete="new-password" />
          <password-input
            v-model="password2"
            label="Repeat new password"
            autocomplete="new-password"
          />

          <p v-if="passwordError" class="profile-error" role="alert">
            <q-icon name="error_outline" size="18px" aria-hidden="true" />
            {{ passwordError }}
          </p>

          <div class="profile-actions">
            <q-btn
              type="submit"
              unelevated
              no-caps
              label="Update password"
              class="profile-button"
              :disable="!passwordReady"
              :loading="savingPassword"
            />
          </div>
        </form>
      </section>
    </template>
  </div>
</template>
