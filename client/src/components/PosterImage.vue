<script setup>
// A 2:3 poster or photo. Shows a grey placeholder when there is no image or it fails to load
import { computed } from 'vue';
import { QIcon, QImg } from 'quasar';
import { imageUrl } from '../format.js';

const props = defineProps({
  src: { type: String, default: '' },
  alt: { type: String, default: '' },
  icon: { type: String, default: 'image_not_supported' },
  iconSize: { type: String, default: '36px' },
  label: { type: String, default: '' }
});

const url = computed(() => imageUrl(props.src));
</script>

<template>
  <q-img v-if="url" :src="url" :alt="alt" :ratio="2 / 3" spinner-color="grey-6">
    <template #error>
      <div class="poster-placeholder">
        <q-icon :name="icon" :size="iconSize" aria-hidden="true" />
        <span v-if="label">{{ label }}</span>
      </div>
    </template>
  </q-img>
  <div v-else class="poster-placeholder">
    <q-icon :name="icon" :size="iconSize" aria-hidden="true" />
    <span v-if="label">{{ label }}</span>
  </div>
</template>
