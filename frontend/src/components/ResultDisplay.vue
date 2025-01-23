<template>
  <div class="absolute top-4 right-4 pointer-events-none">
    <div v-if="results && results.frames" class="flex flex-col gap-2">
      <!-- 只显示最新的检测结果，放在右上角 -->
      <div
        v-for="(detection, idx) in latestResults"
        :key="idx"
        class="text-sm bg-black/50 text-white px-3 py-1.5 rounded-full backdrop-blur-sm"
      >
        Cat {{ detection.cat_id }}: {{ detection.behavior }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResultDisplay',
  props: {
    results: {
      type: Object,
      default: () => null
    }
  },
  computed: {
    latestResults() {
      if (!this.results || !this.results.frames || !this.results.frames.length) {
        return [];
      }
      return this.results.frames[this.results.frames.length - 1];
    }
  }
}
</script>

<style scoped>
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>