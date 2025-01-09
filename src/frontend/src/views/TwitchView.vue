<template>
    <div class="test-container">
      <header class="test-header">
        <h1 class="title">Twitch trends</h1>
        <p class="subtitle">This is a simple test page for debugging and layout tests.</p>
      </header>
      <main class="test-content">
        <p>Welcome to the test page! Add your test components or features here.</p>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: "TestView",
  };
  </script>
  
  <style scoped>
  /* 테스트 페이지 컨테이너 스타일 */
  .test-container {
    padding: 20px;
    background-color: #121212;
    color: #ffffff;
    min-height: 100vh;
  }
  
  /* 헤더 스타일 */
  .test-header {
    text-align: left;
    margin-bottom: 20px;
  }
  
  .title {
    font-size: 4rem;
    font-weight: bold;
    margin: 0;
  }
  
  .subtitle {
    font-size: 1rem;
    margin-top: 5px;
  }
  
  /* 메인 콘텐츠 스타일 */
  .test-content {
    font-size: 1rem;
    line-height: 1.5;
    color: #cccccc;
  }
  </style>
  