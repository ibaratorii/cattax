<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Cat Behavior Analysis</h1>
    
    <UploadArea @upload="handleUpload" />
    
    <div v-if="videoUrl" class="mt-4">
      <!-- 使用 flex 布局，视频占 2/3，进度占 1/3 -->
      <div class="flex gap-4">
        <!-- 左侧视频区域 -->
        <div class="w-2/3 relative">
          <VideoPlayer :url="videoUrl">
            <ResultDisplay v-if="results" :results="results" />
          </VideoPlayer>
        </div>

        <!-- 右侧进度区域 -->
        <div class="w-1/3">
          <div v-if="progress" class="mb-4">
            <p>Processing: {{ progress.toFixed(1) }}%</p>
            <div class="w-full bg-gray-200 rounded">
              <div 
                class="bg-blue-600 text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded" 
                :style="{ width: progress + '%' }"
              >
                {{ progress.toFixed(1) }}%
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { uploadVideo, getAnalysisStatus } from './services/api';
import UploadArea from './components/UploadArea.vue';
import VideoPlayer from './components/VideoPlayer.vue';
import ResultDisplay from './components/ResultDisplay.vue';

export default {
  name: 'App',
  components: {
    UploadArea,
    VideoPlayer,
    ResultDisplay
  },
  data() {
    return {
      videoUrl: null,
      progress: 0,
      results: null,
      analysisId: null
    };
  },
  methods: {
    async handleUpload(file) {
      try {
        console.log('Starting upload...', file)  // 添加日志
        const response = await uploadVideo(file)
        console.log('Upload response:', response)  // 添加日志
        this.videoUrl = URL.createObjectURL(file)
        this.analysisId = response.id
        this.startPolling()
      } catch (error) {
        console.error('Upload failed:', error)
        alert('Upload failed: ' + error.message)  // 显示具体错误信息
      }
    },
    startPolling() {
      console.log('Start polling with ID:', this.analysisId)  // 添加日志
      const pollInterval = setInterval(async () => {
        try {
          const status = await getAnalysisStatus(this.analysisId)
          console.log('Poll status:', status)  // 添加日志
          this.progress = status.progress
          this.results = status.results

          if (status.status === 'completed' || status.status === 'failed') {
            clearInterval(pollInterval)
          }
        } catch (error) {
          console.error('Error fetching status:', error)
          clearInterval(pollInterval)
        }
      }, 1000)
    }
  }
};
</script>

<style>
@import './index.css';
</style>