<script setup>
import { pageTitle } from '../brand.js';
import RegisterForm from '../components/RegisterForm.vue';
document.title = pageTitle('Register');
</script>

<template>
  <main>
    <RegisterForm />
  </main>
</template>
