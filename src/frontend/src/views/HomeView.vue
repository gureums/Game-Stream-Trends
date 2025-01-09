<template>
    <div class="home-container">
      <header class="home-header">
        <h1 class="title">Game & Stream Stats Overview</h1>
        <p class="subtitle">Check out the most played & watched games on various platforms!</p>
      </header>
      <main class="home-content">
        <div class="summary-cards">
          <SummaryCard
            title="Most Played Games on Steam"
            :games="steamGames"
          />
          <SummaryCard
            title="Most Watched Games on YouTube"
            :games="youtubeGames"
          />
          <SummaryCard
            title="Most Watched Games on Twitch"
            :games="twitchGames"
          />
        </div>
      </main>
    </div>
  </template>
  
  <script>
  import SummaryCard from "@/components/SummaryCard.vue";
  
  export default {
    name: "HomeView",
    components: {
      SummaryCard,
    },
    data() {
      return {
        steamGames: [
          {
            id: 1,
            title: "Just Chatting",
            image: "https://via.placeholder.com/50",
            hoursWatched: "62,620,974",
            growth: 3.9,
            extraHours: "+2,376,817",
          },
          {
            id: 2,
            title: "Grand Theft Auto V",
            image: "https://via.placeholder.com/50",
            hoursWatched: "20,914,806",
            growth: 34.8,
            extraHours: "+5,399,456",
          },
        ],
        youtubeGames: [
          {
            id: 1,
            title: "League of Legends",
            image: "https://via.placeholder.com/50",
            hoursWatched: "18,668,831",
            growth: 37.7,
            extraHours: "+5,115,895",
          },
          {
            id: 2,
            title: "Marvel Rivals",
            image: "https://via.placeholder.com/50",
            hoursWatched: "15,953,350",
            growth: 16.6,
            extraHours: "+2,265,815",
          },
        ],
        twitchGames: [
          {
            id: 1,
            title: "World of Warcraft",
            image: "https://via.placeholder.com/50",
            hoursWatched: "15,438,553",
            growth: 30.6,
            extraHours: "+3,615,801",
          },
          {
            id: 2,
            title: "Valorant",
            image: "https://via.placeholder.com/50",
            hoursWatched: "14,125,678",
            growth: 12.3,
            extraHours: "+1,725,432",
          },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  .home-container {
    padding: 20px;
    background-color: #121212;
    color: #ffffff;
  }
  
  .home-header {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .title {
    font-size: 3.5rem;
    font-weight: bold;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  /* Summary Cards Container */
  .summary-cards {
    display: flex;
    gap: 20px;
  }
  
  .summary-card {
    flex: 1;
    max-width: 33%;
  }
  </style>
  