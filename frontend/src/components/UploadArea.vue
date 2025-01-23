<template>
  <div
    @drop.prevent="handleDrop"
    @dragover.prevent
    class="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-gray-400 transition-colors cursor-pointer"
    @click="$refs.fileInput.click()"
  >
    <input
      ref="fileInput"
      type="file"
      class="hidden"
      accept="video/*"
      @change="handleFileChange"
    />
    <div class="space-y-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
      </svg>
      <p class="text-lg text-gray-600">
        Drag & drop a video, or click to select
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UploadArea',
  emits: ['upload'],
  methods: {
    handleDrop(e) {
      const file = e.dataTransfer.files[0]
      if (file) this.$emit('upload', file)
    },
    handleFileChange(e) {
      const file = e.target.files[0]
      if (file) this.$emit('upload', file)
    }
  }
}
</script> 