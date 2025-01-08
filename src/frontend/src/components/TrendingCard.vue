<template>
    <div class="trending-card">
      <div class="game-rank">{{ rank }}</div>
      <div class="game-info">
        <img :src="image" alt="Game Image" class="game-image" />
        <span class="game-title">{{ title }}</span>
      </div>
      <div class="game-stats">
        <div class="stat-item">
          <span>{{ watchTime }}</span>
          <span :class="getChangeClass(watchTimeChange)">
            ({{ watchTimeChange }}%)
          </span>
        </div>
        <div class="stat-item">
          <span>{{ streamTime }}</span>
          <span :class="getChangeClass(streamTimeChange)">
            ({{ streamTimeChange }}%)
          </span>
        </div>
        <div class="stat-item">
          <span>{{ peakViewers }}</span>
          <span :class="getChangeClass(peakViewersChange)">
            ({{ peakViewersChange }}%)
          </span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "TrendingCard",
    props: {
      rank: {
        type: Number,
        required: true,
      },
      title: {
        type: String,
        required: true,
      },
      image: {
        type: String,
        required: true,
      },
      watchTime: {
        type: String,
        required: true,
      },
      watchTimeChange: {
        type: Number,
        required: true,
      },
      streamTime: {
        type: String,
        required: true,
      },
      streamTimeChange: {
        type: Number,
        required: true,
      },
      peakViewers: {
        type: String,
        required: true,
      },
      peakViewersChange: {
        type: Number,
        required: true,
      },
    },
    methods: {
      getChangeClass(change) {
        return change > 0 ? "positive" : "negative";
      },
    },
  };
  </script>
  
  <style scoped>
  .trending-card {
    display: grid;
    grid-template-columns: 50px 2fr 1fr 1fr 1fr;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #333;
    color: #ffffff;
  }
  
  .game-rank {
    font-size: 1rem;
    font-weight: bold;
    text-align: center;
  }
  
  .game-info {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .game-image {
    width: 50px;
    height: 50px;
    border-radius: 8px;
  }
  
  .game-title {
    font-size: 1rem;
    font-weight: bold;
    color: #4caf50;
  }
  
  .game-stats {
    display: flex;
    gap: 20px;
    justify-content: space-between;
  }
  
  .stat-item {
    text-align: center;
  }
  
  .positive {
    color: #4caf50; /* Green for positive */
  }
  
  .negative {
    color: #f44336; /* Red for negative */
  }
  </style>
  