<template>
  <div class="deposit-container">
    <h2 class="title">전체 적금상품 리스트</h2>

    <button class="load-button" @click="savingList">전체/적금 데이터가져오기</button>

    <div v-if="savingProducts.length > 0" class="table-container">
      <table class="product-table">
        <thead>
          <tr>
            <th>상품명</th>
            <th>금융회사</th>
            <th>3개월</th>
            <th>6개월</th>
            <th>12개월</th>
            <th>24개월</th>
            <th>36개월</th>
            <th>최고 저축금리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in savingProducts" :key="product.fin_prdt_cd">
            <td class="product-name">
              <button @click="openModal(product)" class="product-button">
                {{ product.fin_prdt_nm }}
              </button>
            </td>
            <td>{{ product.kor_co_nm }}</td>
            <td>
              <div class="checkbox-wrapper">
                <input type="checkbox" :checked="hasOption(product, 3)" disabled />
              </div>
            </td>
            <td>
              <div class="checkbox-wrapper">
                <input type="checkbox" :checked="hasOption(product, 6)" disabled />
              </div>
            </td>
            <td>
              <div class="checkbox-wrapper">
                <input type="checkbox" :checked="hasOption(product, 12)" disabled />
              </div>
            </td>
            <td>
              <div class="checkbox-wrapper">
                <input type="checkbox" :checked="hasOption(product, 24)" disabled />
              </div>
            </td>
            <td>
              <div class="checkbox-wrapper">
                <input type="checkbox" :checked="hasOption(product, 36)" disabled />
              </div>
            </td>
            <td class="interest-rate">{{ getMaxInterestRate(product) }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="no-data">
      <p>조회된 상품이 없습니다.</p>
    </div>

    <!-- 모달 컴포넌트 -->
    <div v-if="selectedProduct" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeModal">&times;</button>
        <h3>{{ selectedProduct.fin_prdt_nm }}</h3>
        
        <div class="modal-info">
          <div class="info-row">
            <span class="label">금융회사</span>
            <span>{{ selectedProduct.kor_co_nm }}</span>
          </div>
          <div class="info-row">
            <span class="label">가입방법</span>
            <span>{{ selectedProduct.join_way }}</span>
          </div>
          <div class="info-row">
            <span class="label">가입대상</span>
            <span>{{ selectedProduct.join_member }}</span>
          </div>
          <div class="info-row">
            <span class="label">만기 후 이자율</span>
            <span>{{ selectedProduct.mtrt_int }}</span>
          </div>
          <div class="info-row">
            <span class="label">최고 금리</span>
            <span>{{ getMaxInterestRate(selectedProduct) }}%</span>
          </div>
          <div class="info-row">
            <span class="label">우대조건</span>
            <span>{{ selectedProduct.spcl_cnd }}</span>
          </div>
          <div class="info-row">
            <span class="label">특이사항</span>
            <span>{{ selectedProduct.etc_note || '없음' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useDepositStore } from '@/stores/financialProductsStore';
import { ref } from 'vue';
const store = useDepositStore()

const savingProducts = ref([])
const savingOptions = ref([])
const selectedProduct = ref(null)

// 모달 관련 함수
const openModal = (product) => {
  selectedProduct.value = product
}

const closeModal = () => {
  selectedProduct.value = null
}

// 데이터를 가져오는 함수 실행
const savingList = async function (){
  try {
    savingProducts.value = []
    savingOptions.value = []

    await store.loadSavingProducts()
    savingProducts.value = store.savingProducts
    store.savingOptionProducts = []

    let allOptions = []
    for(const product of savingProducts.value){
      await store.loadSavingOptionProducts(product.fin_prdt_cd)
      allOptions = [...allOptions, ...store.savingOptionProducts]
    }
    savingOptions.value = allOptions
  } catch(err) {
    console.error(err)
  }
}

const hasOption = (product, month) => {
  const options = savingOptions.value.filter(option => 
    option.fin_prdt_cd === product.fin_prdt_cd
  )
  return options.some(option => option.save_trm === month)
}

const getMaxInterestRate = (product) => {
  const options = savingOptions.value.filter(option => 
    option.fin_prdt_cd === product.fin_prdt_cd
  )
  if (options.length === 0) return 0.00
  const maxRate = Math.max(...options.map(option => 
    parseFloat(option.intr_rate2) || 0
  ))
  return maxRate.toFixed(2)
}
</script>

<style scoped>
.deposit-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.title {
  color: #1a2b3c;
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2rem;
  letter-spacing: 2px;
}

.load-button {
  display: block;
  margin: 0 auto 2rem;
  padding: 14px 28px;
  background-color: #b4446c;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.load-button:hover {
  background-color: #963c5b;
}

.table-container {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  margin: 2rem auto;
  max-width: 90%;
  overflow-x: auto;
}

.product-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.product-table th {
  background-color: #f8f9fa;
  color: #1a2b3c;
  padding: 1.2rem;
  font-weight: 600;
  font-size: 1rem;
  text-align: center;
  border-bottom: 2px solid #eee;
}

.product-table td {
  padding: 1.2rem;
  text-align: center;
  border-bottom: 1px solid #eee;
  font-size: 0.95rem;
}

.product-button {
  background: none;
  border: none;
  color: #b4446c;
  cursor: pointer;
  font-weight: 500;
  padding: 8px 16px;
  text-align: left;
  width: 100%;
  transition: all 0.3s ease;
  border-radius: 4px;
}

.product-button:hover {
  background-color: #f8f9fa;
  color: #963c5b;
}

.checkbox-wrapper input[type="checkbox"] {
  width: 1.3rem;
  height: 1.3rem;
  border: 2px solid #b4446c;
  border-radius: 4px;
  appearance: none;
  background: white;
  cursor: not-allowed;
  position: relative;
  transition: all 0.3s ease;
}

.checkbox-wrapper input[type="checkbox"]:checked {
  background-color: #b4446c;
}

.checkbox-wrapper input[type="checkbox"]:checked::after {
  content: '✓';
  position: absolute;
  color: white;
  font-size: 0.9rem;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

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
  padding: 2.5rem;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.modal-content h3 {
  color: #1a2b3c;
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
  padding-right: 40px;
}

.modal-close {
  position: absolute;
  top: 2rem;
  right: 2rem;
  background: none;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  color: #666;
  transition: color 0.3s ease;
  padding: 5px;
  line-height: 1;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.modal-close:hover {
  background-color: #f8f9fa;
  color: #b4446c;
}

.info-row {
  margin: 1.2rem 0;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.label {
  font-weight: 600;
  color: #1a2b3c;
  min-width: 120px;
}

.interest-rate {
  color: #b4446c;
  font-weight: 600;
  font-size: 1.1rem;
}

.no-data {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  color: #666;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .deposit-container {
    padding: 1rem;
  }
  
  .title {
    font-size: 2rem;
  }
  
  .table-container {
    padding: 1rem;
    margin: 1rem auto;
    max-width: 95%;
  }
  
  .product-table th,
  .product-table td {
    padding: 0.8rem;
    font-size: 0.9rem;
  }
  
  .modal-content {
    padding: 1.5rem;
  }
  
  .info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}

.product-table tbody tr {
  transition: background-color 0.3s ease;
}

.product-table tbody tr:hover {
  background-color: #f8f9fa;
}

.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: #b4446c;
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: #963c5b;
}
</style>