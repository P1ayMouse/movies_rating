<script>
import { QBtn, QIcon, QInput } from 'quasar';
import { errorMessage } from '@/errors';

export default {
  name: 'ForgotPasswordForm',
  components: { QBtn, QIcon, QInput },
  data() {
    return {
      email: '',
      loading: false,
      formError: '',
      sentTo: ''
    };
  },
  methods: {
    async onSend() {
      this.formError = '';
      const email = this.email.trim();
      if (!email.includes('@')) {
        this.formError = 'Enter the email you signed up with.';
        return;
      }

      this.loading = true;
      try {
        const response = await fetch('/api/v1/auth/password-reset/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email })
        });
        if (response.ok) this.sentTo = email;
        else this.formError = await errorMessage(response);
      } catch {
        this.formError = 'Network error. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    tryAgain() {
      this.sentTo = '';
      this.formError = '';
    }
  }
};
</script>

<template>
  <div class="auth-page">
    <div v-if="sentTo" v-reveal class="auth-card" role="status">
      <span class="auth-state-icon" aria-hidden="true">
        <q-icon name="mark_email_read" size="28px" />
      </span>
      <h1 class="auth-title">Check your email</h1>
      <p class="auth-subtitle">
        If an account exists for <strong>{{ sentTo }}</strong
        >, we sent it a link to set a new password.
      </p>
      <q-btn
        unelevated
        no-caps
        label="Back to log in"
        class="auth-submit auth-submit--block"
        :to="{ name: 'login' }"
      />
      <p class="auth-footer">
        No email?
        <a href="#" @click.prevent="tryAgain">Try a different address</a>
      </p>
    </div>

    <div v-else v-reveal class="auth-card">
      <h1 class="auth-title">Forgot your password?</h1>
      <p class="auth-subtitle">Enter your email and we'll send you a link to set a new one.</p>

      <form class="auth-fields" novalidate @submit.prevent="onSend">
        <q-input
          v-model="email"
          outlined
          type="email"
          label="Email"
          autocomplete="email"
          autofocus
        />

        <p v-if="formError" class="auth-error" role="alert">
          <q-icon name="error_outline" size="18px" aria-hidden="true" />
          {{ formError }}
        </p>

        <q-btn
          type="submit"
          unelevated
          no-caps
          label="Send link"
          class="auth-submit"
          :loading="loading"
        />
      </form>

      <p class="auth-footer">
        Remembered it?
        <router-link :to="{ name: 'login' }">Log in</router-link>
      </p>
    </div>
  </div>
</template>
