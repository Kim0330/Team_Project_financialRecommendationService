<template>
  <header>
      <div id="app">
        <AppNavbar/>
      </div>
  </header>
  <RouterView/>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { ref } from 'vue'  // ref import 추가
import AppNavbar from './components/AppNavbar.vue';


</script>

<style scoped>

@font-face {
  font-family:'squidFont';
 /* font-family:'다른컴포넌트가서 불일 이름'; */
  src: url('assets/fonts/GameOfSquids.ttf') format('truetype');
 /* src: url('폰트가 저장 되어 있는 공간') format('truetype');*/
 
  font-weight: 400;
 /* 폰트 굵기*/
}

</style>
