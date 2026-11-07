<script setup>
import ResetPasswordForm from '../components/ResetPasswordForm.vue';

defineProps({
  token: {
    type: String,
    required: true
  }
});

document.title = 'New password';
</script>

<template>
  <main>
    <ResetPasswordForm :token="token" />
  </main>
</template>
