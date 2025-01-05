```vue
<template>
  <div class="exchange-container">
    <!-- 왼쪽: 환율 계산기 -->
    <div class="calculator-section">
      <div class="exchange-card">
        <div class="input-group box1">
          <div class="amount-input">
            <label>금액</label>
            <input
              v-model.number="amount"
              @input="calculatedExchange_up"
              type="number"
              placeholder="금액을 입력하세요"
            >
          </div>
          <div class="currency-select">
            <label>통화 선택</label>
            <select 
              v-model.number="currencyOne"
              @change="calculatedExchange_up"
            >
              <option
                v-for="country in depositsList"
                :key="country.cur_unit"
                :value="country.cur_unit"
              >
                {{ country.cur_nm }} {{ country.cur_unit }}
              </option>
            </select>
          </div>
        </div>

        <!-- 환율 비교 표시 -->
        <div class="exchange-rate" v-if="currencyOneName && currencyTwoName">
          <p class="rate-text">1 {{ currencyOneName }} = </p>
          <h4 class="rate-value">{{ calculatedperresult }} {{ currencyTwoName }}</h4>
        </div>

        <div class="input-group box2">
          <div class="currency-select">
            <label>통화 선택</label>
            <select 
              v-model="currencyTwo"
              @change="calculatedExchange_down"
            >
              <option 
                v-for="country in depositsList"
                :key="country.cur_unit"
                :value="country.cur_unit"
              >
                {{ country.cur_nm }} {{ country.cur_unit }}
              </option>
            </select>
          </div>
          <div class="amount-input">
            <label>환전 금액</label>
            <input 
              v-model="calculatedAmount"
              @change="calculatedExchange_down"
              type="number"
              placeholder="환전 금액"
            >
          </div>
        </div>
      </div>
    </div>

    <!-- 오른쪽: 날짜 및 차트 -->
    <div class="info-section">
      <div class="date-display">
        <h3>오늘 날짜</h3>
        <p>{{ today }}</p>
      </div>
      <div class="chart-container">
        <!-- 차트 영역 -->
      </div>
    </div>

    <!-- 환율 테이블 -->
    <div class="exchange-table-container">
      <table class="exchange-table">
        <thead>
          <tr>
            <th>국가/통화명</th>
            <th>받으실 때(송금)</th>
            <th>보내실때(송금)</th>
            <th>매매 기준율</th>
            <th>년환가료율</th>
            <th>서울외국환중개<br> 매매기준율</th>
            <th>서울외국환중개<br> 장부가격</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="country in depositsList" :key="country.cur_unit">
            <td>{{ country.cur_nm }}</td>
            <td>{{ country.ttb }}</td>
            <td>{{ country.tts }}</td>
            <td>{{ country.deal_bas_r }}</td>
            <td>{{ country.yy_efee_r }}</td>
            <td>{{ country.kftc_deal_bas_r }}</td>
            <td>{{ country.kftc_bkpr }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref, computed } from 'vue';
import axios from 'axios';

// 리스트 1. 전체리스트 받아오기
const depositsList = ref([]);
// 오늘 날짜
const today = ref('')

const findata= function(){
    try{

        axios.get('http://127.0.0.1:8000/exchange/')
        .then((res)=>{
            // console.log(res.data)
            depositsList.value = res.data
            setInitialCurrency()
            today.value = new Date().toLocaleDateString();
        })
    }catch(err){
        console.error(err)
    }
};


    // 환율 1. 초기값 세팅
    // 기본 환율 대한민국 deal_bas_r원 currency_one
    // 기본 환율 미국 환율 deal_bas_r원 currency_two 
    const currencyOne = ref("KRW");
    const currencyTwo = ref("USD");
    
    // 사용자가 입력할 금액 이면서 결과값이 될 수도 있음
    const amount = ref(1)
    const calculatedAmount = ref(0)

    // 초기 처음 환율이 로드되었을 때 데이터 가져오기
    const setInitialCurrency = async () => {
        console.log('초기값 설정 시작')
    const fromCurrency = depositsList.value.find(item => item['cur_unit'] === "KRW");
    const toCurrency = depositsList.value.find(item => item['cur_unit'] === "USD");
    console.log('초기통화', {fromCurrency, toCurrency})

    if (fromCurrency && toCurrency) {
        currencyOne.value = 'KRW';
        currencyTwo.value = 'USD';
        amount.value = 1


        // 함수호출을 했는데 값이 바로 안나와서 초기 환율 계산하기
        const fromRate = parseFloat(fromCurrency.deal_bas_r.replace(/,/g, '')) || 1;
        const toRate = parseFloat(toCurrency.deal_bas_r.replace(/,/g, '')) || 1;
        console.log('초기환율' ,{fromRate, toRate})
        const rate = fromRate/toRate
        const result = parseFloat(amount.value * rate)
        console.log(rate)
        calculatedAmount.value = result.toFixed(5)
        console.log(calculatedAmount.value)
    }
}


// 환율 2. 환율 계산 함수
    
    // computed, watch 를 사용했을경우 함수가 무한루프를 돌아서! 일반 함수로 실행!
    // box1에 입력했을 경우
    const calculatedExchange_up = function(){

        // item == 객체
        const fromCurrency = depositsList.value.find(item => item['cur_unit'] === currencyOne.value)
        // console.log(fromCurrency)
        // console.log(fromCurrency?.cur_unit)
        // 선택한 두번째 통화
        const toCurrency = depositsList.value.find(item => item['cur_unit'] === currencyTwo.value)
        // 계산 

        // console.log(toCurrency)
        // console.log(toCurrency?.cur_unit)
        if (fromCurrency && toCurrency){
            // parseFloat 문자열을 실수로 바꾸기
            // 대한민국 tts가 0 이기 때문에 deal_bas_r(매매기준율) 사용하기!
            const fromRate = parseFloat(fromCurrency.deal_bas_r.replace(/,/g, '')) || 1;
            const toRate =  parseFloat(toCurrency.deal_bas_r.replace(/,/g, '')) || 1;
            const rate = fromRate/toRate
            const result = parseFloat(amount.value * rate)
            // 소숫점 두번째까지 반올림해서 결과 도출
            calculatedAmount.value = result.toFixed(2)
        }
    }

    // Box2에 입력했을 경우 
    const calculatedExchange_down = function(){

        const fromCurrency = depositsList.value.find(item => item['cur_unit'] === currencyTwo.value)
        const toCurrency = depositsList.value.find(item => item['cur_unit'] === currencyOne.value)

        if (fromCurrency && toCurrency){
            // parseFloat 문자열을 실수로 바꾸기
            const fromRate = parseFloat(fromCurrency.deal_bas_r.replace(/,/g, '')) || 1;
            const toRate = parseFloat(toCurrency.deal_bas_r.replace(/,/g, '')) || 1;

            const rate = fromRate/toRate
            const result = calculatedAmount.value * rate
            // 소숫점 두번째까지 반올림해서 결과 도출
            amount.value = result.toFixed(2)
        }
    }
    

// 환율 3. box1 나라 1원당 box2 나라의 통화
const calculatedperresult = computed(()=> {
const fromCurrency = depositsList.value.find(item => item['cur_unit']===currencyOne.value)
const toCurrency = depositsList.value.find(item => item['cur_unit']===currencyTwo.value)

if (fromCurrency && toCurrency) {
    const fromRate = parseFloat(fromCurrency.deal_bas_r.replace(/,/g, '')) || 1;
    const toRate = parseFloat(toCurrency.deal_bas_r.replace(/,/g, '')) || 1;
    const rate = fromRate / toRate
    return rate.toFixed(5) // 1원 당 다른 통화의 가격
    }
    //데이터가 없는경우
    return 0
    })

const currencyOneName = computed(()=>{
    const currency = depositsList.value.find(item => item['cur_unit'] == currencyOne.value)
    return currency ? currency.cur_nm : '';
    })

const currencyTwoName = computed(()=> {
    const currency = depositsList.value.find(item => item['cur_unit'] == currencyTwo.value)
    return currency ? currency.cur_nm : '';
    })

onMounted(findata);

</script>

<style scoped>
.exchange-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  gap: 2rem;
  background-color: #f5f5f5;
}

.calculator-section {
  display: flex;
  justify-content: center;
}

.exchange-card {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
}

.input-group {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  align-items: flex-end;
}

.amount-input, .currency-select {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

input[type="number"] {
  padding: 0.8rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  width: 100%;
}

input[type="number"]:focus {
  outline: none;
  border-color: #b4446c;
}

select {
  padding: 0.8rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  background-color: white;
  cursor: pointer;
  width: 100%;
}

select:focus {
  outline: none;
  border-color: #b4446c;
}

.exchange-rate {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin: 1.5rem 0;
  text-align: center;
}

.rate-text {
  color: #666;
  margin-bottom: 0.5rem;
}

.rate-value {
  color: #b4446c;
  font-size: 1.5rem;
  margin: 0;
}

.info-section {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.date-display {
  text-align: center;
  margin-bottom: 1.5rem;
}

.date-display h3 {
  color: #1a2b3c;
  margin-bottom: 0.5rem;
}

.exchange-table-container {
  background: white;
  padding: 1.5rem;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.exchange-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.exchange-table th {
  background-color: #f8f9fa;
  color: #1a2b3c;
  padding: 1rem;
  font-weight: 600;
  text-align: center;
  border-bottom: 2px solid #eee;
}

.exchange-table td {
  padding: 1rem;
  text-align: center;
  border-bottom: 1px solid #eee;
}

.exchange-table tbody tr:hover {
  background-color: #f8f9fa;
}

@media (max-width: 768px) {
  .exchange-container {
    padding: 1rem;
  }

  .input-group {
    flex-direction: column;
    gap: 1rem;
  }

  .exchange-card {
    padding: 1rem;
  }

  .exchange-table th,
  .exchange-table td {
    padding: 0.5rem;
    font-size: 0.9rem;
  }
}

/* 숫자 input의 화살표 제거 */
input[type="number"]::-webkit-inner-spin-button, 
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}
</style>
```

주요 변경사항:
1. 전체적인 레이아웃 개선
2. 카드 형태의 디자인 적용
3. 입력 필드와 선택 필드 스타일링
4. 환율 비교 표시 강조
5. 테이블 디자인 개선
6. 반응형 디자인 적용
7. 일관된 색상 테마 사용
8. 그림자 효과와 hover 효과 추가

이제 환율 계산기가 더 현대적이고 사용하기 편한 디자인으로 변경되었습니다. 수정이 필요한 부분이 있다면 말씀해 주세요!