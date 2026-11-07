<script>
import { useQuasar } from 'quasar';
import { errorMessage } from '@/errors';

export default {
  name: 'ResetPasswordForm',
  props: {
    token: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      user: {},
      sending: false
    };
  },
  setup() {
    const $q = useQuasar();
    return { $q };
  },
  methods: {
    async onResetPassword() {
      this.sending = true;
      try {
        const response = await fetch('/api/v1/auth/password-reset/confirm/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            token: this.token,
            password: this.user.password,
            password2: this.user.password2
          })
        });
        if (response.status === 200) {
          this.notify('Password changed. Log in with your new password.', 'positive');
          this.$router.push('/login/');
        } else {
          this.notify(await errorMessage(response), 'negative');
        }
      } catch {
        this.notify('Network error', 'negative');
      } finally {
        this.sending = false;
      }
    },
    notify(message, color) {
      this.$q.notify({
        message,
        color,
        position: 'top',
        textColor: 'white',
        actions: [{ icon: 'close', color: 'white' }],
        timeout: 3000
      });
    },
    goToForgotPassword() {
      this.$router.push('/password-forgot/');
    }
  }
};
</script>

<template>
  <div class="auth-form text-font">
    <div class="row justify-center items-center">
      <q-card class="q-pa-md q-ma-md" style="max-width: 400px; width: 100%">
        <q-card-section class="text-h5 text-center q-mb-md"> New Password </q-card-section>
        <q-form @submit.prevent="onResetPassword" class="q-gutter-md">
          <q-input
            outlined
            v-model="user.password"
            placeholder="Input your new password"
            type="password"
            label="new password"
            required
            color="grey"
            class="q-mb-md"
          />
          <q-input
            outlined
            v-model="user.password2"
            placeholder="Repeat your new password"
            type="password"
            label="repeat password"
            required
            color="grey"
            class="q-mb-md"
          />
          <div class="text-center">
            <q-btn
              label="Change password"
              outline
              type="submit"
              color="grey"
              :loading="sending"
              class="form-button q-mb-md"
            ></q-btn>
          </div>
          <div class="text-center">
            <q-btn
              flat
              color="primary"
              no-caps
              label="Send a new link"
              @click="goToForgotPassword"
            />
          </div>
        </q-form>
      </q-card>
    </div>
  </div>
</template>
