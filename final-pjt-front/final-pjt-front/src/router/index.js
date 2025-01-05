import { createRouter, createWebHistory } from 'vue-router'
import SignUpView from '@/views/SignUpView.vue';
import LogInView from '@/views/LoginView.vue';
import ExchangeView from '@/views/ExchangeView.vue';
import DepositSavingView from '@/views/DepositSavingView.vue';
import CardView from '@/views/CardView.vue';
import CommunityView from '@/views/CommunityView.vue';
import HomeView from '@/views/HomeView.vue';

import Deposit from '@/components/Deposit.vue';
import Saving from '@/components/Saving.vue';
import SelectProduct from '@/components/SelectProduct.vue';
import MapView from '@/views/MapView.vue';

import ArticleDetailView from "@/views/ArticleDetailView.vue";
import CreateView from "@/views/CreateView.vue";
import { useUsersStore } from '@/stores/users';
import UserProfileView from '@/views/UserProfileView.vue';

import ChatbotPage from '@/components/ChatbotPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes:[
    {
      path : '/',
      name : 'home',
      component : HomeView
    },
    {
      path : '/exchange',
      name : 'exchange',
      component : ExchangeView
    },
    {
      path : '/depositsaving',
      name : 'depositsaving',
      component : DepositSavingView,
      children: [
        {
          path: 'deposit',
          name: 'deposit',
          component : Deposit
        },
        {
          path: 'saving',
          name: 'saving',
          component : Saving
        },
        {
          path: 'selectproduct',
          name: 'selectproduct',
          component : SelectProduct
        }
      ]
    },
    {
      path: '/map',
      name: 'map',
      component : MapView
    },
    {
      path: '/card',
      name: 'card',
      component : CardView
    },
    {
      path: '/community',
      name: 'community',
      component : CommunityView
    },
    {
      path: "/articles/:id",
      name: "ArticleDetailView",
      component: ArticleDetailView
    },
    {
      path: "/create",
      name: "CreateView",
      component: CreateView
    },
    {
      path: "/signup",
      name: "signupview",
      component: SignUpView
    },
    {
      path: "/login",
      name: "loginview",
      component: LogInView
    },
    {
      path: "/profile",
      name: "userprofileview",
      component: UserProfileView,
      meta: { requiresAuth: true },
    },
    {
      path: '/chatbot',
      name: 'chatbot',
      component: ChatbotPage
    },
  ]
})
router.beforeEach((to, from) => {
  const store = useUsersStore();

  // 인증이 필요한 페이지에 접근할 때 로그인 체크
  if (to.meta.requiresAuth && !store.isLogin) {
    window.alert("로그인이 필요한 페이지입니다.");
    return { name: "loginView" };
  }

  // 게시판 접근 시 로그인 체크
  if (to.name === "ArticleView" && !store.isLogin) {
    window.alert("로그인이 필요합니다.");
    return { name: "LogInView" };
  }

  // 이미 로그인한 사용자가 로그인/회원가입 페이지 접근 시
  if ((to.name === "SignUpView" || to.name === "LogInView") && store.isLogin) {
    window.alert("이미 로그인되어 있습니다.");
    return { name: "ArticleView" };
  }
});
export default router
