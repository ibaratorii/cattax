<template>
  <div class="w-full">
    <div class="bg-gray-200 rounded-full h-2.5 mb-2">
      <div
        class="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
        :style="{ width: `${progress}%` }"
      ></div>
    </div>
    <p class="text-sm text-gray-600">
      Processing: {{ progress.toFixed(1) }}%
    </p>
  </div>
</template>

<script>
export default {
  name: 'ProgressBar',
  props: {
    progress: {
      type: Number,
      required: true,
      default: 0
    }
  }
}
</script> 