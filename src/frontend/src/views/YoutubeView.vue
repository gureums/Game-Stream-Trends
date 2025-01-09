<template>
    <div class="home-container">
      <header class="home-header">
        <h1 class="title">Youtube trending</h1>
        <p class="subtitle">Latest stats and updates from Youtube</p>
      </header>
      <main class="home-content">
        <div class="trending-header">
          <span>Rank</span>
          <span>Game</span>
          <span>Watch Time</span>
          <span>Stream Time</span>
          <span>Peak Viewers</span>
        </div>
        <div class="trending-list">
          <TrendingCard
            v-for="game in trendingGames"
            :key="game.id"
            :rank="game.rank"
            :title="game.title"
            :image="game.image"
            :watchTime="game.watchTime"
            :watchTimeChange="game.watchTimeChange"
            :streamTime="game.streamTime"
            :streamTimeChange="game.streamTimeChange"
            :peakViewers="game.peakViewers"
            :peakViewersChange="game.peakViewersChange"
          />
        </div>
      </main>
    </div>
  </template>
  
  <script>
  import TrendingCard from "@/components/TrendingCard.vue";
  
  export default {
    name: "HomeView",
    components: {
      TrendingCard,
    },
    data() {
      return {
        trendingGames: [
          {
            id: 1,
            rank: 1,
            title: "Kings League",
            image: "https://via.placeholder.com/50",
            watchTime: "6,020,454",
            watchTimeChange: 153.9,
            streamTime: "1,713",
            streamTimeChange: 217.2,
            peakViewers: "494,778",
            peakViewersChange: 1857.3,
          },
          {
            id: 2,
            rank: 2,
            title: "Escape from Tarkov",
            image: "https://via.placeholder.com/50",
            watchTime: "5,107,211",
            watchTimeChange: -88.5,
            streamTime: "19,553",
            streamTimeChange: -88.5,
            peakViewers: "-4,397",
            peakViewersChange: -102,
          },
          // 추가 데이터...
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  /* 홈 페이지 전체 스타일 */
  .home-container {
    padding: 20px;
    background-color: #121212;
    color: #ffffff;
    min-height: 100vh;
  }
  
  /* 헤더 스타일 */
  .home-header {
    text-align: left; /* 좌측 정렬 */
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
  
  /* 테이블 헤더 스타일 */
  .trending-header {
    display: grid;
    grid-template-columns: 50px 2fr 1fr 1fr 1fr;
    padding: 10px 0;
    border-bottom: 2px solid #333;
    font-weight: bold;
    color: #ffffff;
  }
  
  /* 리스트 스타일 */
  .trending-list {
    display: flex;
    flex-direction: column;
  }
  </style>
  