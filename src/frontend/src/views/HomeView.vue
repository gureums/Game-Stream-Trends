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
import axios from "axios";

export default {
  name: "HomeView",
  components: {
    SummaryCard,
  },
  data() {
    return {
      steamGames: [], // Steam 게임 데이터
      youtubeGames: [], // YouTube 게임 데이터
      twitchGames: [], // Twitch 게임 데이터
    };
  },
  methods: {
    async fetchData() {
      try {
        // Steam 데이터 요청
        const steamResponse = await axios.get("http://localhost:8000/api/steam/overview");
        this.steamGames = steamResponse.data.map((game, index) => ({
          id: index + 1,
          title: game[0],
          //image: game,
          hoursWatched: game[1].toLocaleString(),
          growth: game[2],
        }));

        // YouTube 데이터 요청
        const youtubeResponse = await axios.get("http://localhost:8000/api/youtube/overview");
        this.youtubeGames = youtubeResponse.data.map((game, index) => ({
          id: index + 1,
          title: game.title,
          image: game.image,
          hoursWatched: game.hoursWatched.toLocaleString(),
          growth: game.growth,
          extraHours: `+${game.extraHours.toLocaleString()}`,
        }));

        // Twitch 데이터 요청
        const twitchResponse = await axios.get("http://localhost:8000/api/twitch/overview");
        this.twitchGames = twitchResponse.data.map((game, index) => ({
          id: index + 1,
          title: game.title,
          image: game.image,
          hoursWatched: game.hoursWatched.toLocaleString(),
          growth: game.growth,
          extraHours: `+${game.extraHours.toLocaleString()}`,
        }));
      } catch (error) {
        console.error("Failed to fetch data:", error);
      }
    },
  },
  created() {
    this.fetchData();
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
  