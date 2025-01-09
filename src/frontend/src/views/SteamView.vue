<template>
    <div class="home-container">
      <div class="content-container">
        <header class="header">
          <h1 class="title">Steam trending</h1>
          <p class="subtitle">Based on player counts and release date</p>
          <div class="filter-options">
            <div class="order-button" @click="toggleDropdown">
              <span>Order by:</span>
              <span class="selected-option">{{ selectedOption }}</span>
              <i class="fas fa-chevron-down"></i>
            </div>
            <div v-if="dropdownOpen" class="dropdown-menu">
              <div
                class="dropdown-item"
                v-for="option in filterOptions"
                :key="option"
                @click="selectOption(option)"
              >
                <span>{{ option }}</span>
                <i v-if="option === selectedOption" class="fas fa-check"></i>
              </div>
            </div>
          </div>
        </header>
        <main class="content">
          <GameCard
            v-for="game in filteredGames"
            :key="game.title"
            :title="game.title"
            :likes="game.likes"
            :image="game.image"
          />
        </main>
      </div>
    </div>
  </template>
  
  <script>
  import GameCard from "@/components/GameCard.vue";
  
  export default {
    name: "SteamView",
    components: {
      GameCard,
    },
    data() {
      return {
        dropdownOpen: false,
        selectedOption: "Popularity",
        filterOptions: [
          "Popularity",
          "Date added",
          "Name",
          "Release date",
          "Average rating",
        ],
        games: [
          { title: "Satisfactory", likes: 2641, image: require("@/assets/images/placeholder.png") },
          { title: "V Rising", likes: 1852, image: require("@/assets/images/placeholder.png") },
          { title: "STALKER 2", likes: 941, image: require("@/assets/images/placeholder.png") },
          { title: "TEST 1", likes: 503, image: require("@/assets/images/placeholder.png") },
          { title: "TEST 2", likes: 37, image: require("@/assets/images/placeholder.png") },
          { title: "TEST 3", likes: 1, image: require("@/assets/images/placeholder.png") },
        ],
      };
    },
    computed: {
      filteredGames() {
        // 간단한 필터링 로직 (선택된 옵션에 따라 동작 추가 가능)
        if (this.selectedOption === "Relevance") {
          return this.games;
        }
        if (this.selectedOption === "Popularity") {
          return [...this.games].sort((a, b) => b.likes - a.likes);
        }
        return this.games; // 기본 반환
      },
    },
    methods: {
      toggleDropdown() {
        this.dropdownOpen = !this.dropdownOpen;
      },
      selectOption(option) {
        this.selectedOption = option;
        this.dropdownOpen = false;
      },
    },
  };
  </script>
  
  <style scoped>
  /* 전체 컨테이너 */
  .home-container {
    display: flex;
  }
  
  /* 콘텐츠 컨테이너 */
  .content-container {
    flex-grow: 1;
    padding: 20px;
  }
  
  /* 헤더 스타일 */
  .header {
    text-align: left;
    margin-bottom: 20px;
  }
  
  .title {
    font-size: 4rem;
    font-weight: bold;
  }
  
  .subtitle {
    font-size: 1rem;
    margin-top: 5px;
  }
  
  /* 필터 옵션 스타일 */
  .filter-options {
    margin-top: 10px;
    position: relative;
  }
  
  .order-button {
    display: inline-flex;
    align-items: center;
    background-color: #212121;
    color: #ffffff;
    padding: 10px 16px;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
  }
  
  .order-button span:first-child {
    margin-right: 8px;
    color: #dfdfdf;
  }
  
  .selected-option {
    font-weight: bold;
  }
  
  .order-button i {
    font-size: 0.8rem;
    margin-left: 8px;
  }
  
  /* 드롭다운 메뉴 */
  .dropdown-menu {
    position: absolute;
    top: 50px;
    left: 0;
    background-color: #fff;
    color: #1e1e1e;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(91, 89, 89, 0.2);
    padding: 8px 0;
    z-index: 1000;
  }
  
  .dropdown-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 16px;
    cursor: pointer;
  }
  
  .dropdown-item:hover {
    background-color: #c3c3c3;
  }
  
  .dropdown-item i {
    color: #00c853; /* 체크 아이콘 색상 (녹색) */
  }

  /* 콘텐츠 그리드 스타일 */
.content {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 한 줄에 4개씩 */
  gap: 20px; /* 카드 간격 */
}

/* 게임 카드 스타일 */
.game-card {
  background-color: #1e1e1e;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.game-card img {
  width: 100%;
  height: auto;
  border-radius: 12px;
  margin-bottom: 10px;
}
  </style>
  