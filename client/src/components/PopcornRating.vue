<script setup>
import { computed, ref } from 'vue';
import { QIcon } from 'quasar';

const props = defineProps({
  modelValue: { type: Number, default: null },
  max: { type: Number, default: 10 },
  disabled: { type: Boolean, default: false },
  labelledby: { type: String, default: undefined }
});
const emit = defineEmits(['update:modelValue']);

const hovered = ref(null);
const shown = computed(() => hovered.value ?? props.modelValue ?? 0);

function pick(score) {
  if (props.disabled || score === props.modelValue) return;
  emit('update:modelValue', score);
}
</script>

<template>
  <div
    class="popcorn-rating"
    :class="{ 'popcorn-rating--disabled': disabled }"
    role="group"
    :aria-labelledby="labelledby"
    @mouseleave="hovered = null"
  >
    <div class="popcorn-rating-buckets">
      <button
        v-for="score in max"
        :key="score"
        type="button"
        class="popcorn-rating-bucket"
        :class="{ 'popcorn-rating-bucket--on': score <= shown }"
        :aria-label="`${score} out of ${max}`"
        :aria-pressed="score === modelValue"
        :disabled="disabled"
        @mouseenter="hovered = score"
        @focus="hovered = score"
        @blur="hovered = null"
        @click="pick(score)"
      >
        <q-icon class="popcorn-icon" aria-hidden="true" />
      </button>
    </div>
    <span v-if="shown" class="popcorn-rating-value" aria-hidden="true">
      <span class="popcorn-rating-number">{{ shown }}</span>
      <span class="popcorn-rating-scale">/ {{ max }}</span>
    </span>
  </div>
</template>
