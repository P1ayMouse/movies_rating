<script>
import { QBtn, QIcon } from 'quasar';
import PasswordInput from './PasswordInput.vue';
import { errorMessage } from '@/errors';

const MIN_LENGTH = 6;

export default {
  name: 'ResetPasswordForm',
  components: { PasswordInput, QBtn, QIcon },
  props: {
    token: { type: String, required: true }
  },
  data() {
    return {
      password: '',
      password2: '',
      loading: false,
      formError: ''
    };
  },
  methods: {
    async onReset() {
      this.formError = '';
      if (this.password.length < MIN_LENGTH) {
        this.formError = `Password must be at least ${MIN_LENGTH} characters.`;
        return;
      }
      if (this.password !== this.password2) {
        this.formError = 'Passwords do not match.';
        return;
      }

      this.loading = true;
      try {
        const response = await fetch('/api/v1/auth/password-reset/confirm/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            token: this.token,
            password: this.password,
            password2: this.password2
          })
        });
        if (!response.ok) {
          this.formError = await errorMessage(response);
          return;
        }
        this.$q.notify({
          message: 'Password changed. Log in with your new password.',
          color: 'positive',
          position: 'top',
          timeout: 3000
        });
        this.$router.push({ name: 'login' });
      } catch {
        this.formError = 'Network error. Please try again.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-title">Set a new password</h1>
      <p class="auth-subtitle">Pick a password you don't use anywhere else.</p>

      <form class="auth-fields" novalidate @submit.prevent="onReset">
        <password-input
          v-model="password"
          label="New password"
          autocomplete="new-password"
          autofocus
        />
        <password-input
          v-model="password2"
          label="Repeat new password"
          autocomplete="new-password"
        />

        <p v-if="formError" class="auth-error" role="alert">
          <q-icon name="error_outline" size="18px" aria-hidden="true" />
          {{ formError }}
        </p>

        <q-btn
          type="submit"
          unelevated
          no-caps
          label="Change password"
          class="auth-submit"
          :loading="loading"
        />
      </form>

      <p class="auth-footer">
        Link expired?
        <router-link :to="{ name: 'password-forgot' }">Send a new one</router-link>
      </p>
    </div>
  </div>
</template>
