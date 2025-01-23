<script>
// ... 其他代码保持不变 ...

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
</script>