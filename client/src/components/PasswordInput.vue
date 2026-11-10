<script setup>
import { ref } from 'vue';
import { QBtn, QInput } from 'quasar';

const model = defineModel({ type: String, default: '' });

defineProps({
  label: { type: String, default: 'Password' },
  autocomplete: { type: String, default: 'current-password' }
});

const visible = ref(false);
</script>

<template>
  <q-input
    v-model="model"
    outlined
    :label="label"
    :type="visible ? 'text' : 'password'"
    :autocomplete="autocomplete"
  >
    <template #append>
      <q-btn
        flat
        round
        dense
        :icon="visible ? 'visibility_off' : 'visibility'"
        :aria-label="visible ? 'Hide password' : 'Show password'"
        @click="visible = !visible"
      />
    </template>
  </q-input>
</template>
