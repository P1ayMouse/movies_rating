<script>
import { useQuasar } from 'quasar';
import { authFetch, authState } from '@/auth';
import { errorMessage } from '@/errors';

export default {
  name: 'ProfileForm',

  data() {
    return {
      user: {},
      userLoaded: false,
      formError: null
    };
  },
  setup() {
    const $q = useQuasar();
    return { $q };
  },
  async mounted() {
    let response;
    try {
      response = await authFetch('/api/v1/auth/user-info/');
    } catch {
      this.showError('Network error');
      return;
    }

    if (response.status === 200) {
      this.user = await response.json();
      document.title = 'Profile of ' + (this.user.username || this.user.email);
      this.userLoaded = true;
    } else if (response.status === 403) {
      // the session could not be renewed, so log in again
      this.$router.push('/login');
    } else {
      this.showError(`Server error ${response.status}`);
    }
  },
  methods: {
    async onUserEditProfile() {
      this.formError = null;
      const body = { username: this.user.username };
      if (this.user.password || this.user.password2) {
        body.password = this.user.password;
        body.password2 = this.user.password2;
      }

      let response;
      try {
        response = await authFetch('/api/v1/auth/user-info/', {
          method: 'PATCH',
          body: JSON.stringify(body)
        });
      } catch {
        this.showError('Network error');
        return;
      }

      if (response.status === 200) {
        this.user = await response.json();
        authState.user = { ...this.user };
        document.title = 'Profile of ' + (this.user.username || this.user.email);
        this.$q.notify({
          message: 'Profile updated',
          color: 'positive',
          position: 'top',
          timeout: 2000
        });
      } else if (response.status === 403) {
        this.$router.push('/login');
      } else {
        this.showError(await errorMessage(response));
      }
    },
    showError(message) {
      this.formError = message;
      this.$q.notify({
        message,
        color: 'negative',
        position: 'top',
        textColor: 'white',
        actions: [{ icon: 'close', color: 'white' }],
        timeout: 2000
      });
    }
  }
};
</script>

<template>
  <div class="profile-form text-font">
    <div class="row justify-center items-center">
      <q-card class="q-pa-md q-ma-md" style="max-width: 400px; width: 100%">
        <q-card-section class="text-h5 text-center q-mb-md"> Profile </q-card-section>
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
            <q-btn
              label="Update"
              outline
              type="submit"
              color="grey"
              class="form-button q-mb-md"
            ></q-btn>
          </div>
        </q-form>
      </q-card>
    </div>
  </div>
</template>
