<template>
  <div class="trending-card">
    <div class="game-rank">{{ rank }}</div>
    <div class="game-info">
      <span class="game-title">{{ title }}</span>
    </div>
    <div class="custom-content">
      <!-- 부모 컴포넌트가 전달한 슬롯을 사용 -->
      <slot />
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
  },
};
</script>

<style scoped>
.trending-card {
  display: grid;
  grid-template-columns: 50px 2fr repeat(auto-fit, minmax(100px, 1fr));
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
  font-size: 1.2rem;
  font-weight: bold;
  color: #4caf50;
  margin-left: 10px;
}

.custom-content {
  display: flex;
  justify-content: space-around;
  font-size: 0.9rem;
  color: #cccccc;
}
</style>
