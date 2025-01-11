<template>
    <aside class="sidebar">
      <div class="top-section">
        <h2 class="sidebar-title">Team Gureum</h2>
      </div>
      <nav class="menu">
        <ul>
          <li>
            <div class="icon-container">
              <i class="fas fa-home"></i>
            </div>
            <a href="/home">Home</a>
          </li>
          <li>
            <div class="icon-container">
              <img src="@/assets/images/steam.png" alt="Steam" class="custom-icon" />
            </div>
            <a href="#">Steam</a>
          </li>
          <ul class="submenu">
            <li class="submenu-item">
              <div class="icon-container-small">
                <i class="fas fa-star"></i>
              </div>
              <a href="/steam-toprated">Top Rated</a>
            </li>
            <li class="submenu-item">
              <div class="icon-container-small">
                <i class="fas fa-fire"></i>
              </div>
              <a href="#">Most Played</a>
            </li>
            <li class="submenu-item">
              <div class="icon-container-small">
                <i class="fas fa-clock"></i>
              </div>
              <a href="#">Recently Updated</a>
            </li>
          </ul>
          <li>
            <div class="icon-container">
              <img src="@/assets/images/youtube.png" alt="Steam" class="custom-icon" />
            </div>
            <a href="/youtube">Youtube</a>
          </li>
          <ul class="submenu">
            <li class="submenu-item">
              <div class="icon-container-small">
                <i class="fas fa-star"></i>
              </div>
              <a href="#">Top Games</a>
            </li>
            <li class="submenu-item">
              <div class="icon-container-small">
                <i class="fas fa-fire"></i>
              </div>
              <a href="#">Most Watched</a>
            </li>
            <li class="submenu-item">
              <div class="icon-container-small">
                <i class="fas fa-clock"></i>
              </div>
              <a href="#">Recently Uploaded</a>
            </li>
          </ul>
          <li>
            <div class="icon-container">
              <img src="@/assets/images/twitch.png" alt="Twitch" class="custom-icon" />
            </div>
            <a href="/twitch">Twitch</a>
          </li>
          <ul class="submenu">
            <li class="submenu-item">
              <div class="icon-container-small">
                <i class="fas fa-star"></i>
              </div>
              <a href="#">Top Games</a>
            </li>
            <li class="submenu-item">
              <div class="icon-container-small">
                <i class="fas fa-fire"></i>
              </div>
              <a href="#">Most watched</a>
            </li>
            <li class="submenu-item">
              <div class="icon-container-small">
                <i class="fas fa-clock"></i>
              </div>
              <a href="#">Recently Watched</a>
            </li>
          </ul>
        </ul>
      </nav>
    </aside>
  </template>
  
  <script>
  export default {
    name: 'AppSidebar',
  };
  </script>
  
  <style scoped>
  /* 기본 사이드바 스타일 */
  .sidebar {
    width: 200px;
    background-color: #1e1e1e;
    color: #ffffff;
    padding: 20px;
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
  
  .sidebar-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 20px;
  }
  
  .menu ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .menu li {
    display: flex;
    align-items: center;
    margin-bottom: 3px;
    padding: 8px;
    border-radius: 8px;
    transition: background-color 0.3s;
  }
  
  .menu li:hover {
    background-color: #333;
  }
  
  /* 아이콘 스타일 */
  .icon-container {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #333;
    border-radius: 8px;
    margin-right: 12px;
  }
  
  .icon-container i {
    font-size: 1.2rem;
    color: #ffffff;
  }
  
  .custom-icon {
    width: 24px;
    height: 24px;
  }
  
  .icon-container-small {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #333;
    border-radius: 6px;
    margin-right: 8px;
  }
  
  /* 서브메뉴 스타일 */
  .submenu {
    list-style: none;
    margin: 0;
    padding-left: 8px !important;
  }
  
  .submenu-item {
    display: flex;
    align-items: center;
    margin-bottom: 3px !important;
  }
  
  .submenu-item .icon-container-small {
    margin-right: 10px;
  }
  
  /* 링크 스타일 */
  .menu a {
    text-decoration: none;
    color: #ffffff;
    font-size: 1rem;
    font-weight: 500;
  }
  
  .menu a:hover {
    color: #ccc;
  }
  </style>
  