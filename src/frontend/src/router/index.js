import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import SteamView from '@/views/SteamView.vue';
import AboutView from '@/views/AboutView.vue';
import NotFoundPage from "@/views/404Page.vue";

const routes = [
  {
    path: "/",
    component: () => import("@/components/Layout.vue"),
    children: [
      {
        path: '/home',
        name: 'Home',
        component: HomeView,
      },
      {
        path: '/steam',
        name: 'Steam',
        component: SteamView,
      },
      {
        path: '/about',
        name: 'About',
        component: AboutView,
      },
    ]
  },
  {
    path: "/:pathMatch(.*)*", // 모든 매칭되지 않는 경로
    name: "not-found",
    component: NotFoundPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
