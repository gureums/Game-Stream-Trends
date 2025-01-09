<template>
    <div class="summary-card">
      <h3 class="summary-title">{{ title }}</h3>
      <div class="stats-table">
        <div v-for="game in games" :key="game.id" class="stats-row">
          <div class="game-info">
            <img :src="game.image" alt="Game Image" class="game-image" />
            <span class="game-title">{{ game.title }}</span>
          </div>
          <div class="stats-data">
            <span class="hours-watched">{{ game.hoursWatched }}</span>
            <span :class="getChangeClass(game.growth)">
              {{ game.growth > 0 ? '▲' : '▼' }} {{ game.growth }}%
            </span>
            <span class="extra-hours">{{ game.extraHours }}</span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "SummaryCard",
    props: {
      title: {
        type: String,
        required: true,
      },
      games: {
        type: Array,
        required: true,
      },
    },
    methods: {
      getChangeClass(growth) {
        return growth > 0 ? "positive" : "negative";
      },
    },
  };
  </script>
  
  <style scoped>
  .summary-card {
    background-color: #1e1e1e;
    border-radius: 8px;
    padding: 15px;
    width: 100%;
  }
  
  .summary-title {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 15px;
  }
  
  .stats-table {
    display: flex;
    flex-direction: column;
  }
  
  .stats-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #333;
  }
  
  .stats-row:last-child {
    border-bottom: none;
  }
  
  .game-info {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .game-image {
    width: 50px;
    height: 50px;
    border-radius: 50%;
  }
  
  .game-title {
    font-size: 1rem;
    font-weight: bold;
    color: #4caf50;
  }
  
  .stats-data {
    text-align: right;
  }
  
  .hours-watched {
    font-size: 1rem;
    font-weight: bold;
  }
  
  .positive {
    color: #4caf50; /* Green */
  }
  
  .negative {
    color: #f44336; /* Red */
  }
  
  .extra-hours {
    font-size: 0.8rem;
    color: #cccccc;
  }
  </style>
  