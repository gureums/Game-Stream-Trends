<template>
  <div class="steam-container">
    <header class="steam-header">
      <h1 class="title">Steam Top Rated Games</h1>
      <p class="subtitle">Explore the latest trends in Game Reviews</p>
    </header>
    <main class="steam-content">
      <table class="stats-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th @click="sortTable('gameName')">
              Game Name
              <span class="sort-icon" :class="getSortIcon('gameName')"></span>
            </th>
            <th @click="sortTable('positiveRatio')">
              Positive Review Ratio
              <span class="sort-icon" :class="getSortIcon('positiveRatio')"></span>
            </th>
            <th @click="sortTable('changePositive')">
              Positives Reviews
              <span class="sort-icon" :class="getSortIcon('changePositive')"></span>
            </th>
            <th @click="sortTable('changeNegative')">
              Negatives Reviews
              <span class="sort-icon" :class="getSortIcon('changeNegative')"></span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(game, index) in sortedGames" :key="game.rank">
            <td>{{ index + 1 }}</td>
            <td class="game-name">{{ game.gameName }}</td>
            <td class="positive-ratio-cell">
              <div class="positive-ratio-container">
                <div
                  class="positive-ratio-bar"
                  :style="{ 
                    width: game.positiveRatio + '%',
                    backgroundColor: getBarColor(game.positiveRatio),
                  }"
                ></div>
              </div>
              <span class="positive-ratio-text">{{ game.positiveRatio }}%</span>
            </td>
            <td :class="getChangeClass(game.changePositive)">
              +{{ game.changePositive }}
            </td>
            <td class="negative-review">
              +{{ game.changeNegative }}
            </td>
          </tr>
        </tbody>
      </table>
    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SteamTopratedView",
  data() {
    return {
      games: [], // Original games data
      sortKey: "positiveRatio", // Default column for sorting
      sortOrder: -1, // Default sort order (-1 for descending)
    };
  },
  computed: {
    sortedGames() {
      if (this.sortKey) {
        return [...this.games].sort((a, b) => {
          if (typeof a[this.sortKey] === "string") {
            return (
              this.sortOrder *
              a[this.sortKey].localeCompare(b[this.sortKey], undefined, {
                numeric: true,
              })
            );
          } else {
            return this.sortOrder * (a[this.sortKey] - b[this.sortKey]);
          }
        });
      }
      return this.games;
    },
  },
  methods: {
    getBarColor(positiveRatio) {
      if (positiveRatio >= 85) {
        return "#2196f3"; // Blue
      } else if (positiveRatio >= 60) {
        return "#4caf50"; // Green
      } else {
        return "#ffeb3b"; // Yellow
      }
    },
    async fetchSteamData() {
      try {
        const response = await axios.get("http://localhost:8000/api/steam/recommend");
        const rawData = response.data.result;

        this.games = rawData.map((game, index) => ({
          rank: index + 1,
          gameName: game[0],
          positiveRatio: parseFloat(game[1]).toFixed(2),
          changePositive: game[2],
          changeNegative: game[3],
        }));
      } catch (error) {
        console.error("Failed to fetch data:", error);
      }
    },
    sortTable(column) {
      if (this.sortKey === column) {
        this.sortOrder *= -1; // Reverse sort order
      } else {
        this.sortKey = column;
        this.sortOrder = 1; // Default to ascending
      }
    },
    getSortIcon(column) {
      if (this.sortKey === column) {
        return this.sortOrder === 1 ? "sort-asc" : "sort-desc";
      }
      return "sort-default";
    },
    getChangeClass(change) {
      return change > 0 ? "positive" : "negative";
    },
  },
  created() {
    this.fetchSteamData();
  },
};
</script>

<style scoped>
.title {
  font-size: 4rem;
}

/* Table styles */
.stats-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.stats-table th,
.stats-table td {
  text-align: center;
  padding: 10px 15px;
  border-bottom: 1px solid #333;
  position: relative;
  white-space: nowrap; /* Prevent text wrapping */
}

.stats-table th {
  cursor: pointer;
}

.stats-table th:hover {
  background-color: #1e1e1e;
}

.stats-table tbody tr:hover {
  background-color: #2a2a2a;
}

/* Sort icons */
.sort-icon {
  margin-left: 8px; /* Adds spacing between column name and icon */
  font-size: 0.8rem;
  vertical-align: middle;
  display: inline-block; /* Ensures proper alignment */
}

.sort-asc::after {
  content: "▲";
  color: #ffffff;
}

.sort-desc::after {
  content: "▼";
  color: #ffffff;
}

.sort-default::after {
  content: "⇅";
  color: #666666;
}

/* Positive Ratio styles */
.positive-ratio-cell {
  display: flex;
  align-items: center;
  gap: 10px; /* Space between bar and text */
}

.positive-ratio-container {
  position: relative;
  
  width: 100%;
  height: 10px;
  background-color: #333;
  border-radius: 5px;
  overflow: hidden;
}

.positive-ratio-bar {
  height: 100%;
  background-color: #4caf50;
  transition: width 0.3s ease; /* Smooth transition for bar width */
  position: absolute;
  right: 0; /* Align the bar to the right */
}

.positive-ratio-text {
  font-size: 0.9rem;
  color: #ffffff;
}

/* Change classes */
.positive {
  color: #4caf50; /* Green for positive change */
}

.negative-review {
  color: #f44336; /* Red for all negative reviews */
}
</style>
