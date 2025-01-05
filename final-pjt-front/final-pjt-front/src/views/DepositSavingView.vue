<template>
  <div class="page-container">
    <nav class="nav-container">
      <div class="nav-links">
        <RouterLink :to="{name: 'deposit'}" class="nav-link">정기 예금</RouterLink> 
        <RouterLink :to="{name: 'saving'}" class="nav-link">정기 적금</RouterLink>  
        <RouterLink :to="{name: 'selectproduct'}" class="nav-link">상품 검색</RouterLink>
      </div>
    </nav>
    <div class="content-container">
      <RouterView/>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  position: relative;
}

.nav-container {
  position: sticky;
  top: 0;
  background-color: transparent;
  border: none;
  box-shadow: none;
  z-index: 100;
  padding: 15px 0;
}

.nav-links {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding-right: 40px;
  gap: 15px;
}

.nav-link {
  text-decoration: none;
  color: #333;
  padding: 5px 10px;
  position: relative;
  transition: all 0.2s ease;
  white-space: nowrap;
  font-weight: 500;
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

.nav-link:hover::after,
.router-link-active::after {
  width: 100%;
}

.nav-link:hover,
.router-link-active {
  color: #a33a62;
}

.content-container {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .nav-links {
    padding-right: 20px;
    gap: 10px;
  }

  .nav-link {
    padding: 5px;
    font-size: 0.9rem;
  }

  .content-container {
    padding: 1rem;
  }
}
</style>