<template>
  <div class="cards-container">
    <h1 class="title">카드 리스트</h1>
    <div class="cards-grid">
      <div
        v-for="(card, index) in cards"
        :key="index"
        class="card-item"
        @click="openModal(card)"
      >
        <div class="card-image">
          <img :src="card.card_img" :alt="card.card_name" v-if="card.card_img" />
          <div v-else class="placeholder-image">이미지 없음</div>
        </div>
        <div class="card-content">
          <h2 class="card-name">{{ card.card_name }}</h2>
          <p class="card-company">{{ card.card_company }}</p>
          <p class="card-type">{{ card.card_type }}</p>
          <p class="benefits-category">카테고리: {{ card.card_benefits_category }}</p>
          <a :href="card.card_url" target="_blank" class="card-link">카드 정보 보기</a>
        </div>
      </div>
    </div>

    <!-- 모달 -->
    <div v-if="selectedCard" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button class="modal-close" @click="closeModal">×</button>
        <h2 class="modal-title">{{ selectedCard.card_name }}</h2>
        <div class="modal-body">
          <img :src="selectedCard.card_img" alt="카드 이미지" class="modal-image" />
          <div>
            <div class="info-group">
              <h4>카드사</h4>
              <p>{{ selectedCard.card_company }}</p>
            </div>
            <div class="info-group">
              <h4>카드 타입</h4>
              <p>{{ selectedCard.card_type }}</p>
            </div>
            <div class="info-group">
              <h4>혜택 카테고리</h4>
              <p>{{ selectedCard.card_benefits_category }}</p>
            </div>
            <div class="info-group">
              <h4>혜택</h4>
              <ul>
                <li
                  v-for="(benefit, benefitIndex) in selectedCard.card_benefits"
                  :key="benefitIndex"
                  class="benefit-item"
                >
                  <strong>{{ benefit.title }}</strong>
                  <ul>
                    <li v-for="(detail, detailIndex) in benefit.benefits" :key="detailIndex">
                      {{ detail }}
                    </li>
                  </ul>
                </li>
              </ul>
            </div>
            <a
              :href="selectedCard.card_url"
              target="_blank"
              class="card-link"
              style="margin-top: 1rem;"
            >
              카드 정보 보기
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import dummyData1 from '@/data/card_details_cafe_1.json'
import dummyData2 from '@/data/card_details_cafe.json'
import dummyData3 from '@/data/card_details_checkcard.json'
import dummyData4 from '@/data/card_details_culture_2.json'
import dummyData5 from '@/data/card_details_culture.json'
import dummyData6 from '@/data/card_details_oil_2.json'
import dummyData7 from '@/data/card_details_oil.json'
import dummyData8 from '@/data/card_details_public_2.json'
import dummyData9 from '@/data/card_details_public.json'
import dummyData10 from '@/data/card_details_shooping_3.json'
import dummyData11 from '@/data/card_details_shopping_2.json'
import dummyData12 from '@/data/card_details_shopping_4.json'
import dummyData13 from '@/data/card_details_shopping.json'
import dummyData14 from '@/data/card_details_trip_2.json'
import dummyData15 from '@/data/card_details_trip.json'
import dummyData16 from '@/data/card_details_trip.json'

const cards = [
  ...dummyData1,
  ...dummyData2,
  ...dummyData3,
  ...dummyData4,
  ...dummyData5,
  ...dummyData6,
  ...dummyData7,
  ...dummyData8,
  ...dummyData9,
  ...dummyData10,
  ...dummyData11,
  ...dummyData12,
  ...dummyData13,
  ...dummyData14,
  ...dummyData15,
  ...dummyData16,
]; 
let selectedCard = null; 

// 모달 열기
const openModal = (card) => {
  selectedCard = card;
};

// 모달 닫기
const closeModal = () => {
  selectedCard = null;
};

</script>

<style scoped>
.cards-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #f5f5f5;
}

.title {
  color: #1a2b3c;
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2rem;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.card-item {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  cursor: pointer;
}

.card-item:hover {
  transform: translateY(-5px);
}

.card-image {
  height: 200px;
  overflow: hidden;
  background: #f8f9fa;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-image {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
}

.card-content {
  padding: 1.5rem;
}

.card-header {
  margin-bottom: 1rem;
}

.card-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a2b3c;
  margin-bottom: 0.5rem;
}

.card-company {
  color: #666;
  font-size: 0.9rem;
}

.card-type {
  background: #f8f9fa;
  padding: 0.5rem;
  border-radius: 8px;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.card-benefits {
  margin-bottom: 1rem;
}

.benefits-category {
  font-size: 0.9rem;
  color: #666;
}

.card-link {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #b4446c;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.card-link:hover {
  background-color: #963c5b;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.modal-title {
  font-size: 1.8rem;
  color: #1a2b3c;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eee;
}

.modal-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.modal-image {
  width: 100%;
  max-height: 300px;
  object-fit: contain;
  border-radius: 8px;
}

.info-group {
  margin-bottom: 1.5rem;
}

.info-group h4 {
  color: #1a2b3c;
  margin-bottom: 0.5rem;
}

.benefit-item {
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .cards-container {
    padding: 1rem;
  }

  .modal-body {
    grid-template-columns: 1fr;
  }
}
</style>