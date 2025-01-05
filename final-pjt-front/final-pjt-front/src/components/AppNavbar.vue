<template>
  <header class="navbar">
      <div class="logo">
          <RouterLink :to="{name:'home'}" class="nav-link">Card Salad</RouterLink>
      </div>
      <nav class="nav-menu">
          <RouterLink :to="{name:'depositsaving'}" class="nav-link">예적금</RouterLink>
          <RouterLink :to="{name:'card'}" class="nav-link">카드</RouterLink> 
          <RouterLink :to="{name:'exchange'}" class="nav-link">환율</RouterLink> 
          <RouterLink :to="{name:'map'}" class="nav-link">주변은행</RouterLink> 
          <RouterLink :to="{name:'community'}" class="nav-link">커뮤니티</RouterLink>
          <RouterLink :to="{ name: 'chatbot' }" class="nav-link">챗봇</RouterLink>
          
          <div v-if="!store.isLogin" class="auth-links">
            <RouterLink :to="{name:'loginview'}" class="nav-link">로그인</RouterLink>
            <RouterLink :to="{name:'signupview'}" class="nav-link">회원가입</RouterLink>
          </div>
          <div v-else class="auth-links">
            <RouterLink :to="{name:'userprofileview'}" class="nav-link">마이페이지</RouterLink>
            <span @click="store.logOut" class="nav-link">로그아웃</span>
          </div>
      </nav>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useUsersStore } from '@/stores/users';
const store = useUsersStore()
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: transparent;
  border: none;
  box-shadow: none;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  padding-left: 20px;
}

.nav-menu {
  display: flex;
  align-items: center; /* 모든 항목을 세로 중앙 정렬 */
  font-size: 1rem;
  padding-right: 40px;
}

.auth-links {
  display: flex;
  align-items: center;
  margin-left: 15px; /* 다른 네비게이션 항목과의 간격 */
}

.nav-link {
  text-decoration: none;
  color: #333;
  padding: 5px 10px; /* 상하/좌우 패딩 추가 */
  margin: 0 3px;
  transition: all 0.2s ease;
  position: relative;
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
}

.nav-link::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 40%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background-color: #a33a62;
  transition: all 0.5s ease-out;
}

.nav-link:hover::after {
  width: 100%;
}

.nav-link:hover {
  color: #a33a62;
}

/* 마지막 nav-link의 오른쪽 마진 제거 */
.auth-links .nav-link:last-child {
  margin-right: 0;
}
</style>