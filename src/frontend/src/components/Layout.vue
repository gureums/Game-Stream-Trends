<template>
    <div class="layout">
      <AppSidebar />
      <div class="main-content">
        <router-view />
      </div>
    </div>
  </template>
  
  <script>
  import AppSidebar from "@/components/Sidebar.vue";
  
  export default {
    name: "MainLayout",
    components: {
      AppSidebar,
    },
  };
  </script>
  
  <style scoped>
  .layout {
    display: flex;
    height: 100vh;
    background-color: #121212; /* 공통 배경색 */
  }
  
  .main-content {
    flex-grow: 1;
    padding: 20px;
    overflow-y: auto;
    color: #ffffff;
  }
  </style>
  