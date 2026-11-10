<script setup>
import { pageTitle } from '../brand.js';
import ResetPasswordForm from '../components/ResetPasswordForm.vue';

defineProps({
  token: {
    type: String,
    required: true
  }
});

document.title = pageTitle('New password');
</script>

<template>
  <main>
    <ResetPasswordForm :token="token" />
  </main>
</template>
