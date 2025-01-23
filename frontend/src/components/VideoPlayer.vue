<template>
  <div class="relative pt-[56.25%]">
    <video 
      v-if="url"
      :src="url"
      class="absolute top-0 left-0 w-full h-full"
      controls 
    ></video>
    <!-- 在视频播放器内部添加插槽 -->
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'VideoPlayer',
  props: {
    url: {
      type: String,
      required: true
    }
  }
}
</script>