<script setup>
import { computed, ref, watch } from 'vue';
import { QIcon } from 'quasar';

const props = defineProps({
  totalPages: { type: Number, required: true }
});

const currentPage = defineModel({ type: Number, required: true });
const pageDraft = ref(String(currentPage.value));

const isFirstPage = computed(() => currentPage.value <= 1);
const isLastPage = computed(() => currentPage.value >= props.totalPages);
const pageDigits = computed(() => Math.max(2, String(props.totalPages).length));

watch(currentPage, resetPageDraft);

function resetPageDraft() {
  pageDraft.value = String(currentPage.value);
}

function goToPage(requestedPage) {
  const nextPage = Math.min(props.totalPages, Math.max(1, requestedPage));
  pageDraft.value = String(nextPage);
  currentPage.value = nextPage;
}

function submitPage() {
  const value = pageDraft.value.trim();
  const page = Number(value);

  if (!/^\d+$/.test(value) || !Number.isSafeInteger(page)) {
    resetPageDraft();
    return;
  }

  goToPage(page);
}
</script>

<template>
  <nav class="movie-pagination" aria-label="Movie pages">
    <button
      type="button"
      class="movie-pagination__button"
      aria-label="First page"
      :disabled="isFirstPage"
      @click="goToPage(1)"
    >
      <q-icon name="keyboard_double_arrow_left" size="22px" aria-hidden="true" />
    </button>

    <button
      type="button"
      class="movie-pagination__button"
      aria-label="Previous page"
      :disabled="isFirstPage"
      @click="goToPage(currentPage - 1)"
    >
      <q-icon name="chevron_left" size="22px" aria-hidden="true" />
    </button>

    <form class="movie-pagination__jump" @submit.prevent="submitPage">
      <input
        v-model="pageDraft"
        class="movie-pagination__input"
        :style="{ '--page-digits': pageDigits }"
        type="text"
        inputmode="numeric"
        enterkeyhint="go"
        autocomplete="off"
        :aria-label="`Page number, ${totalPages} pages total. Press Enter to go.`"
        title="Enter a page number and press Enter"
        @focus="$event.target.select()"
        @blur="resetPageDraft"
        @keydown.esc.prevent="resetPageDraft"
      />
      <span class="movie-pagination__total" aria-hidden="true">/ {{ totalPages }}</span>
    </form>

    <button
      type="button"
      class="movie-pagination__button"
      aria-label="Next page"
      :disabled="isLastPage"
      @click="goToPage(currentPage + 1)"
    >
      <q-icon name="chevron_right" size="22px" aria-hidden="true" />
    </button>

    <button
      type="button"
      class="movie-pagination__button"
      aria-label="Last page"
      :disabled="isLastPage"
      @click="goToPage(totalPages)"
    >
      <q-icon name="keyboard_double_arrow_right" size="22px" aria-hidden="true" />
    </button>
  </nav>
</template>
