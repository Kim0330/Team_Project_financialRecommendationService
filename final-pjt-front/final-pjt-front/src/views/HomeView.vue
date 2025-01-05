<template>
  <div class="center-container">
    <h1 id="title"></h1>
  </div>

  <div class="body">
    <div class="cover">
      <p class="first-parallel"></p>
    </div>
  </div>
  <div></div>


</template>

<script setup>
import { onMounted } from 'vue';


  document.addEventListener('DOMContentLoaded', ()=>{
    new TypeIt('#title',{
      speed: 120,
      loop: true,
      loopDelay : 2000,
    })
      .type('무궁화 꽃이 피었습니다.')
      .pause(1000)
      .delete(13, {delay: 1000})
      .type('<span style="color: #052939; font-size: 120px ">welcome </span><br>')
      .pause(500)
      .type('<span style="color: #ae3f6a; font-size: 150px">Card</span>')
      .type('<span style="color: #052939; font-size: 120px ">-</span>')
      .type('<span style="color: #ae3f6a; font-size: 150px">Salad</span>')
      .pause(2000)
      .go()
  })

let count = 0;
let firstParallel;

const initImage = (element, imageSrc) => {
  const img = document.createElement('img');
  img.src = imageSrc;
  img.alt = 'Moving Image';
  img.style.marginRight = '20px'; // 이미지 간 간격
  element.appendChild(img);

  // 이미지 반복을 위해 한 번 더 추가
  const duplicateImg = img.cloneNode(true);
  element.appendChild(duplicateImg);
};

const marqueeImage = (count, element, direction) => {
  if (count > element.scrollWidth / 2) {
    element.style.transform = `translate3d(0, 0, 0)`;
    count = 0;
  }
  element.style.transform = `translate3d(${direction * count}px, 0, 0)`;

  return count;
};

const animate = () => {
  count += 3;
  count = marqueeImage(count, firstParallel, -1);

  window.requestAnimationFrame(animate);
};

onMounted(() => {
  firstParallel = document.querySelector('.first-parallel');

  const imageSrc = 'src/assets/images/cadlong.png'; // 이미지 경로
  initImage(firstParallel, imageSrc);

  animate();
});
</script>


<style scoped>
.center-container {
  display: flex; /* 플렉스 박스 사용 */
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  height: 70vh; /* 화면 전체 높이 */
  text-align: center;
  margin: 0;
  padding: 0;
}

#title{
  font-family: 'squidFont';
  font-size: 70px;
}

.type {
  color: #ae3f6a; /* 원하는 색상 코드 */
}


.cover {
  width: 100%;
  overflow: hidden; /* 화면 넘어가는 부분 숨김 */
  display: flex;
  justify-content: flex-start; /* 컨텐츠가 왼쪽에서 시작 */
  position: relative;
  height: 150px; /* 적절히 높이 설정 */
  margin-bottom: 20px;
}

.first-parallel {
  display: flex;
  flex-wrap: nowrap; /* 이미지가 한 줄로 이어지도록 */
  white-space: nowrap; /* 줄바꿈 방지 */
  transform: translate3d(0, 0, 0);
}

img {
  height: 120px; /* 이미지 높이 */
  object-fit: cover; /* 비율 유지 */
}


</style>