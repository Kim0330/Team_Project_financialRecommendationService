<template>
  <div class="filter-container row">
    <h2 class="title">상품 추천 검색</h2>
    <div class="card">
      <!-- 예금/적금 선택 -->
      <div class="filter-section">
        <h3 class="section-title">상품 종류</h3>
        <div class="checkbox-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.deposit" /> 예금
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.saving" /> 적금
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.all" /> 전체
          </label>
        </div>
      </div>

      <!-- 단리/복리/전체 선택 -->
      <div class="filter-section">
        <h3 class="section-title">이자 유형</h3>
        <div class="checkbox-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.simpleInterest" /> 단리
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.compoundInterest" /> 복리
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.allInterest" /> 전체
          </label>
        </div>
      </div>

      <!-- 은행 선택 -->
      <div class="filter-section">
        <h3 class="section-title">은행 선택</h3>
        <div class="checkbox-group bank-options">
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.wooriBank" /> 우리은행
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.scBank" /> 한국스탠다드차타드은행
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.imBank" /> 아이엠뱅크
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.busanBank" /> 부산은행
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.gwangjuBank" /> 광주은행
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.jejuBank" /> 제주은행
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.gyeongnamBank" /> 경남은행
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.smeBank" /> 중소기업은행
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.kdbBank" /> 한국산업은행
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.kbBank" /> 국민은행
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.shinhanBank" /> 신한은행
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.nhfBank" /> 농협은행주식회사
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.hanaBank" /> 하나은행
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.corpBank" /> 주식회사
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.kBank" /> 케이뱅크
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.suhyupBank" /> 수협은행
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.tossBank" /> 토스뱅크
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.allBanks" /> 전체은행
          </label>
        </div>
      </div>

      <!-- 개월 수 선택 -->
      <div class="filter-section">
        <h3 class="section-title">기간 선택</h3>
        <div class="checkbox-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.month1" /> 1개월
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.month3" /> 3개월
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.month6" /> 6개월
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.month12" /> 12개월
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.month24" /> 24개월
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.month36" /> 36개월
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterOptions.allmonth" /> 전체
          </label>
        </div>
      </div>

      <!-- 목표금액 입력 -->
      <div class="filter-section">
        <h3 class="section-title">목표 금액</h3>
        <div class="amount-input">
          <input
            type="text"
            v-model="inputAmount"
            placeholder="목표 금액을 입력하세요"
            class="input-field"
          />
          <p v-show="targetAmount > 0" class="amount-display">
            목표 금액: {{ formattedTargetAmount }}
          </p>
        </div>
      </div>

      <button class="submit-button" @click="filterProductsByTargetAmount">
        추천 상품 보기
      </button>
    </div>

    <!-- 예금 추천 상품 -->
    <div v-if="depositRecommendations.length > 0" class="recommendations">
      <h3 class="recommendations-title">추천 상품</h3>
      <div class="product-grid">
        <div
          v-for="product in depositRecommendations"
          :key="product.fin_prdt_cd"
          class="product-card"
        >
          <h4 class="product-name">{{ product.fin_prdt_nm }}</h4>
          <p class="bank-name">은행: {{ product.kor_co_nm }}</p>
          <div class="amount-details">
            <p>예상 만기금액: {{ formatNumber(product.expectedAmount) }}원</p>
            <p>예상 이자수익: {{ formatNumber(product.interestAmount) }}원</p>
          </div>
          <p v-if="product.mtrt_int" class="interest-rate">
            만기 후 이자율: {{ product.mtrt_int }}
          </p>
        </div>
      </div>
    </div>
    <div v-else class="no-results">
      <p>조건에 맞는 추천 상품이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { useDepositStore } from '@/stores/financialProductsStore';
import {ref, watch, onMounted, computed} from 'vue'

const store = useDepositStore()

const filterOptions = ref({
  deposit : false,
  saving : false,
  all : false,
  simpleInterest : false,
  compoundInterest: false,
  allInterest: false,
  month1: false,
  month3: false,
  month6: false,
  month12: false,
  month24: false,
  month36: false,
  allmonth: false,
  wooriBank: false,
  scBank: false,
  imBank: false,
  shinhanBank: false,
  busanBank: false,
  gwangjuBank: false,
  jejuBank: false,
  gyeongnamBank: false,
  smeBank: false,
  kdbBank: false,
  nhfBank: false,
  corpBank: false,
  hanaBank: false,
  kBank: false,
  suhyupBank: false,
  tossBank: false,
  allBanks: false,
})

// 필터링된 상품리스트
const filteredProducts = ref([])
const depositRecommendations = ref([]) 

    // 입력값
    const inputAmount = ref('');

    const targetAmount = computed(() => {
      const value = Number(inputAmount.value) * 1000;
      return isNaN(value) ? 0 : value;
    });

    const formattedTargetAmount = computed(() => {
      const amount = targetAmount.value;
      if (amount >= 10000) {
        const man = Math.floor(amount / 10000);
        const remainder = amount % 10000;
        return remainder === 0 ? `${man}만원` : `${man}만 ${remainder.toLocaleString()}원`;
      }
      return amount.toLocaleString() + "원";
    });

    // 포멧함수
    const formatNumber = (number) => {
      return number.toLocaleString('ko-KR')
    }


  // 초기 데이터 로딩을 위한 함수 추가
  const loadInitialData = async () => {
    try {
      await store.loadDepositProducts()
      await store.loadSavingProducts()

      // 초기 필터링 실행
      await updateFilteredProducts()
    }
    catch (err){
      console.error(err)
    }
  }

// 만기금액 계산 함수
const calculateExpectedAmount = (product, principal) => {
  const period = product.save_trm
  const rate = product.intr_rate2 > 0 ? product.intr_rate2 : product.intr_rate
  
  // 예금의 경우 (단리)
  if (filterOptions.value.deposit && !filterOptions.value.saving) {
      return principal * (1 + (rate/100) * (period/12))
  }
  // 적금의 경우 (월 납입액 기준)
  else {
    if (product.intr_rate_type_nm === '단리') {
      const monthlyPayment = principal / period
      const totalPrincipal = monthlyPayment * period
      const interest = monthlyPayment * (period * (period + 1) / 2) * (rate/100/12)
      return totalPrincipal + interest
    } else {
      const monthlyPayment = principal / period
      const monthlyRate = rate/100/12
      const compound = (1 + monthlyRate) ** period
      return monthlyPayment * ((compound - 1) / monthlyRate)
    }
  }
}



// 상품 필터링 함수
const updateFilteredProducts = async () => {
  let products = []

    // 예적금 필터링
    if (filterOptions.value.deposit && !filterOptions.value.saving) {
      products = store.depositProducts
    } else if (filterOptions.value.saving && !filterOptions.value.deposit) {
      products = store.savingProducts
    } else if (filterOptions.value.all) {
      products = [
        ...store.depositProducts,
        ...store.savingProducts
      ]
    }

    const filters = {
      interestType: [], 
      months: [],       
      banks: []        
      }

    // 단리,복리 필터링
    if (filterOptions.value.simpleInterest) {filters.interestType.push('단리')}
    if (filterOptions.value.compoundInterest) {filters.interestType.push('복리')}

  
    // 개월수 필터링
    if (!filterOptions.value.allmonth) {
      const monthFilters = {
        month1: '1', month3: '3', month6: '6', month12: '12', month24: '24', month36: '36'
      }

      Object.entries(monthFilters).forEach(([key, value]) => {
        if (filterOptions.value[key]) {
          filters.months.push(value)
        }
      })
    }

      // 필터 적용
      if (filters.interestType.length > 0) {
        products = products.filter(p => filters.interestType.includes(p.intr_rate_type_nm))
      }
      
      if (filters.months.length > 0) {
        products = products.filter(p => filters.months.includes(p.save_trm))
      }


    // 은행 필터링 
    if (!filterOptions.value.allBanks) {
        const selectedBanks = []
        if (filterOptions.value.wooriBank) selectedBanks.push('우리은행')
        if (filterOptions.value.scBank) selectedBanks.push('한국스탠다드차타드은행')
        if (filterOptions.value.imBank) selectedBanks.push('아이엠뱅크')
        if (filterOptions.value.busanBank) selectedBanks.push('부산은행')
        if (filterOptions.value.gwangjuBank) selectedBanks.push('광주은행')
        if (filterOptions.value.jejuBank) selectedBanks.push('제주은행')
        if (filterOptions.value.gyeongnamBank) selectedBanks.push('경남은행')
        if (filterOptions.value.smeBank) selectedBanks.push('중소기업은행')
        if (filterOptions.value.kdbBank) selectedBanks.push('한국산업은행')
        if (filterOptions.value.kbBank) selectedBanks.push('국민은행')
        if (filterOptions.value.nhfBank) selectedBanks.push('농협은행주식회사')
        if (filterOptions.value.shinhanBank) selectedBanks.push('신한은행')
        if (filterOptions.value.hanaBank) selectedBanks.push('하나은행')
        if (filterOptions.value.corpBank) selectedBanks.push('주식회사')
        if (filterOptions.value.kBank) selectedBanks.push('케이뱅크')
        if (filterOptions.value.suhyupBank) selectedBanks.push('수협은행')
        if (filterOptions.value.tossBank) selectedBanks.push('토스뱅크')

      if (selectedBanks.length > 0) {
        
        try {
          const bankPromises = []
          selectedBanks.forEach(bankName => {
            bankPromises.push(store.depositBankData(bankName)),
            bankPromises.push(store.savingBankData(bankName))
          })
          // 모든 함수가 호출될때까지 기다리기
          await Promise.all(bankPromises)
    
          // store에서 가져온 예적금 데이터를 products 배열에 합치기
          products = [
            ...store.deposit_bank,
            ...store.saving_bank
          ]
        }
        catch(err){
          console.error(err)
      }
    }
  }
  filteredProducts.value = products;
}

// 추천 상품 필터링
const filterProductsByTargetAmount = async () => {
  if (targetAmount.value <= 0) {
    console.log('Target amount is invalid');
    return;
  }

  try {
    await updateFilteredProducts();
    console.log(filteredProducts.value)

    const productsWithExpectedAmount = filteredProducts.value.map(product => {
      const expectedAmount = calculateExpectedAmount(product, targetAmount.value);
      const interestAmount = expectedAmount - targetAmount.value;
      return {
        ...product,
        expectedAmount: Math.round(expectedAmount),
        interestAmount: Math.round(interestAmount)
      };
    });

    const sortedProducts = productsWithExpectedAmount.sort(
      (a, b) => b.interestAmount - a.interestAmount
    );

      depositRecommendations.value = sortedProducts.slice(0, 10);
    } catch (error) {
      console.error('Error in filterProductsByTargetAmount:', error);
    }
  };


  // watch 추가
  watch(filterOptions, async () => {
    await updateFilteredProducts()
  }, { deep: true })

  // 컴포넌트 마운트 시 초기 데이터 로드
  onMounted(async () => {
    await loadInitialData()
  })

</script>

<style scoped>
.filter-container {
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

.filter-groups {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.filter-group {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.filter-group h3 {
  color: #1a2b3c;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.checkbox-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
}

.banks-grid {
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
}

.checkbox-label {
  display: inline-flex;  
  align-items: center;
  gap: 0.5rem;
  min-width: fit-content; 
  white-space: nowrap;   
  margin-right: 1rem;    
}

.checkbox-label:hover {
  background-color: #f8f9fa;
}

.checkbox-label input[type="checkbox"] {
  width: 1.2rem;
  height: 1.2rem;
  border: 2px solid #b4446c;
  border-radius: 4px;
  appearance: none;
  background: white;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
}

.checkbox-label input[type="checkbox"]:checked {
  background-color: #b4446c;
}

.checkbox-label input[type="checkbox"]:checked::after {
  content: '✓';
  position: absolute;
  color: white;
  font-size: 0.9rem;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.amount-input {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.amount-input input {
  padding: 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  width: 100%;
  max-width: 400px;
  transition: border-color 0.3s ease;
}

.amount-input input:focus {
  outline: none;
  border-color: #b4446c;
}

.target-amount {
  color: #b4446c;
  font-weight: 600;
  font-size: 1.1rem;
}

.submit-button {
  display: block;
  margin: 2rem auto;
  padding: 14px 28px;
  background-color: #b4446c;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  min-width: 200px;
}

.submit-button:hover {
  background-color: #963c5b;
}

.recommendations {
  margin-top: 3rem;
}

.recommendations h3 {
  color: #1a2b3c;
  font-size: 1.8rem;
  text-align: center;
  margin-bottom: 2rem;
}

.product-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.product-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-card h4 {
  color: #b4446c;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.bank-name {
  color: #666;
  font-weight: 500;
}

.amount-info {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
}

.amount, .interest {
  margin: 0.5rem 0;
  line-height: 1.5;
}

.interest-rate {
  color: #1a2b3c;
  font-weight: 600;
}

.no-products {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  color: #666;
  margin-top: 2rem;
}

.bank-options .checkbox-label {
  min-width: 200px;     
}

.checkbox-group {
  display: flex;
  flex-direction: row;  
  flex-wrap: wrap;      
  gap: 1rem;
  padding: 0.5rem;
}

@media (max-width: 768px) {
  .filter-container {
    padding: 1rem;
  }

  .title {
    font-size: 2rem;
  }

  .checkbox-container {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }

  .banks-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }

  .product-cards {
    grid-template-columns: 1fr;
  }

  .filter-group {
    padding: 1rem;
  }
}
</style>