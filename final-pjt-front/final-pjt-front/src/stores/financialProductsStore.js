import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'


export const useDepositStore = defineStore('deposit', () => {
  const API_URL = 'http://127.0.0.1:8000/deposits'
  
  // 모든 데이터 저장
  const getFindata = ref([])
  const loadDepositAllData = async function () {
    await axios({
      method : 'get',
      url: `${API_URL}/make_fin_data/`
  
    })
      .then((res)=>{
          console.log(res.data);
          getFindata.value = res.data
        })
      .catch((err)=>{
        console.error(err);
      })
  }
  
  // 예금 상품 데이터
  const depositProducts = ref([])
  const depositDetailProduct = ref({})
  const depositOptionProducts = ref([])
  // const depositOptionDetailProduct = ref({})

  const loadDepositProducts = async function(){
    await axios({
      method: 'get',
      url: `${API_URL}/deposit_data/`
      // headers: {
      //   Authorization: `Token ${userStore.token}`,
      // },
    })
      .then((res)=>{
        console.log(res.data)
        depositProducts.value = res.data
      })
      .catch((err)=>{
        console.error(err)
      })
  }

  // 예금 상품 상세 데이터
  const loadDepositDetailProduct = function(productNumber){
    axios({
      method: 'get',
      url: `${API_URL}/deposit_data/${productNumber}`
    })
      .then((res)=>{
        console.log(res.data)
        depositDetailProduct.value = res.data
      })
      .catch((err)=>{
        console.error(err)
      })
  }

  // 예금 상품 옵션 데이터
  const loadDepositOptionProducts = async function(productNumber) {
    try {
      const res = await axios({
        method: 'get',
        url: `${API_URL}/deposit_option_data/${productNumber}/`
      })
      // 기존 옵션에 새로운 옵션 추가
      depositOptionProducts.value = [
        ...depositOptionProducts.value,
        ...res.data
      ]
    } catch (err) {
      console.error(err)
    }
  }

  
  // 적금 상품 데이터
  const savingProducts = ref([])
  const savingDetailProduct = ref({}) 
  const savingOptionProducts = ref([])
  // const savingOptionDetailProduct = ref({})
  
  const loadSavingProducts = async function(){
    await axios({
      method: 'get',
      url: `${API_URL}/saving_data/`
    })
      .then((res)=>{
        console.log(res.data)
        savingProducts.value = res.data
      })
      .catch((err)=>{
        console.error(err)
      })
  }
  
  // 적금 상품 상세 데이터
  const loadSavingDetailProduct = function(productNumber){
    axios({
      method: 'get',
      url: `${API_URL}/saving_data/${productNumber}/`
    })
      .then((res)=>{
        console.log(res.data)
        savingDetailProduct.value = res.data
      })
      .catch((err)=>{
        console.error(err)
      })
  }

  // 적금 상품 옵션 데이터 
  const loadSavingOptionProducts = async function(productNumber){
    await axios({
      method: 'get',
      url: `${API_URL}/saving_option_data/${productNumber}/`
    })
      .then((res)=>{
        console.log(res.data)
        savingOptionProducts.value = res.data
      })
      .catch((err)=>{
        console.error(err)
      })
  }


  // 필터링 데이터 가져오기 

  // 예금 데이터  (개월수별/ 단리복리)
  // 필터링된 옵션데이터의 상품코드를 뽑아서 예금 상품정보 반환하기
  // http://127.0.0.1:8000/deposits/deposit-options/?save_trm=1

  const filters = ref({
    save_trm: '',
    intr_rate_type_nm: '',
  });
  const depositfilteredSaveTrm = ref([]);
  const depostifilteredIntrRate = ref([])

  // 1. 예금 save_trm 필터링 함수
  const depositSaveTrm = async function (){
    if(!filters.value.save_trm) return [];

    const url = `${API_URL}/deposit-options/?save_trm=${filters.value.save_trm}`
    const res = await axios.get(url);
    return res.data.map(option => option['fin_prdt_cd']);
  }

  // 2. 예금 save_trm 필터링 함수 (옵션데이터(save_trm) + 예금 데이터)
  // 함수실행은 이걸로!! 위에 호출됨
  const depositfilteredSave = async function(){
    try {
      const productCodesSaveTrm = await depositSaveTrm();
      // 예금 상품 데이터 가져오기
      const productRes = await axios.get(`${API_URL}/deposit_data/`)

      // 전체 상품 데이터에서 필터링된 상품 코드들에 해당하는 상품만 필터링
      const filteredBySaveTrm = productRes.data.filter(product => 
        productCodesSaveTrm.includes(product['fin_prdt_cd'])
      );
      depositfilteredSaveTrm.value = filteredBySaveTrm
      console.log(depositfilteredSaveTrm.value)
    }
    catch(err){
      console.error(err)
    }
  }


  // 1. 예금 intr_rate_type_nm 필터링 함수
  const depositIntrRate = async function (){
    if(!filters.value.intr_rate_type_nm) return [];

    const url = `${API_URL}/deposit-options/?intr_rate_type_nm=${filters.value.intr_rate_type_nm}`;
    const res = await axios.get(url)
    return res.data.map(option => option['fin_prdt_cd'])
  }

   // 2. 예금 intr_rate_type_nm 필터링 함수 데이터 결합하기 (옵션데이터(intr_rate_type_nm) + 예금 데이터)
   const depositfilteredIntr = async function (){
    try {
      const productCodesIntr = await depositIntrRate()
      const productRes = await axios.get(`${API_URL}/deposit_data/`)
      const filteredByIntr = productRes.data.filter(product => 
        productCodesIntr.includes(product['fin_prdt_cd'])
      )
      depostifilteredIntrRate.value = filteredByIntr
      console.log(depostifilteredIntrRate.value)
    }
    catch(err){
      console.error(err)
    }
   }

  // const depositfilteredData = async function() {
  //   let url = `${API_URL}/deposit-options/?`;

  //   // 쿼리 파라미터 동적으로 설정
  //   Object.keys(filters.value).forEach((key) => {
  //     if (filters.value[key]) {
  //       url += `${key}=${filters.value[key]}`;
  //     }
  //   });
  //   try {
  //     // 필터링된 옵션 데이터 
  //       const res = await axios.get(url);
  //       const filteredOptions = res.data;

  //     // 옵션 데이터에서 상품코드를 추출
  //     const productCodes = filteredOptions.map(option => option['fin_prdt_cd']);

  //     //예금 상품 데이터를 가져와서 상품코드를 필터링 
  //     const productRes = await axios.get(`${API_URL}/deposits/`);
  //     depositfiltered.value = productRes.data.filter(product => 
  //     productCodes.includes(product['fin_prdt_cd'])
  //     );

  //     console.log(depositfiltered.value); 
  //   } catch (err) {
  //     console.error(err)
  //   }
  // };

// 적금 데이터  (개월수별/ 단리복리)
  const savingfilteredSaveTrm = ref([]);
  const savingfilteredIntrRate = ref([])

  // 1. 적금 save_trm 필터링 함수
  const savingSaveTrm = async function (){
    if(!filters.value.save_trm) return [];

    const url = `${API_URL}/saving-options/?save_trm=${filters.value.save_trm}`
    const res = await axios.get(url);
    return res.data.map(option => option['fin_prdt_cd']);
  }

  // 2. 적금 save_trm 필터링 함수 (옵션데이터(save_trm) + 예금 데이터)
  // 함수실행은 이걸로!! 위에 호출됨
  const savingfilteredSave = async function(){
    try {
      const productCodesSaveTrm = await savingSaveTrm();
      // 예금 상품 데이터 가져오기
      const productRes = await axios.get(`${API_URL}/saving_data/`)

      // 전체 상품 데이터에서 필터링된 상품 코드들에 해당하는 상품만 필터링
      const filteredBySaveTrm = productRes.data.filter(product => 
        productCodesSaveTrm.includes(product['fin_prdt_cd'])
      );
      savingfilteredSaveTrm.value = filteredBySaveTrm
      console.log(savingfilteredSaveTrm.value)
    }
    catch(err){
      console.error(err)
    }
  }

  // 1. 적금 intr_rate_type_nm 필터링 함수
  const savingIntrRate = async function (){
    if(!filters.value.intr_rate_type_nm) return [];

    const url = `${API_URL}/saving-options/?intr_rate_type_nm=${filters.value.intr_rate_type_nm}`;
    const res = await axios.get(url)
    return res.data.map(option => option['fin_prdt_cd'])
  }

   // 2. 예금 intr_rate_type_nm 필터링 함수 데이터 결합하기 (옵션데이터(intr_rate_type_nm) + 예금 데이터)
   const savingfilteredIntr = async function (){
    try {
      const productCodesIntr = await savingIntrRate()
      const productRes = await axios.get(`${API_URL}/saving_data/`)
      const filteredByIntr = productRes.data.filter(product => 
        productCodesIntr.includes(product['fin_prdt_cd'])
      )
      savingfilteredIntrRate.value = filteredByIntr
      console.log(savingfilteredIntrRate.value)
    }
    catch(err){
      console.error(err)
    }
   }




// 예금 데이터 (은행별)
const deposit_bank = ref([])
  const depositBankData = function(name){
    axios({
      method: 'get',
      url: `${API_URL}/deposit-filter/?kor_co_nm=${name}`
    })
    . then((res)=>{
      console.log(res.data)
      deposit_bank.value = res.data
      return res.data
    })
     .catch((err)=>{
      console.error(err)
      return []
     })
  }  

// 적금 데이터 (은행별)
const saving_bank = ref([])
  const savingBankData = function(name){
    const encodedName = encodeURIComponent(name); // URL 인코딩
    const url = `${API_URL}/saving-filter/?kor_co_nm=${encodedName}`
    axios({
      method: 'get',
      url: url
    })
    . then((res)=>{
      console.log(res.data)
      saving_bank.value = res.data
      return res.data
    })
     .catch((err)=>{
      console.error(err)
      return []
     })
  }  



  // 상품 개월수 별로 분류(1, 3, 6, 12, 24, 36)
  // 예금 (1, 3, 6, 12, 24, 36)
    
  // 적금 (1, 3, 6, 12, 24, 36)

  // 상품 단리, 복리별로 분류
  // 예금 (단리, 복리)
  // 적금 (단리, 복리)

  // 은행별로 분류 
  // 우리은행 한국스탠다드차타드은행 아이엠뱅크 부산은행 광주은행 제주은행 경남은행 중소기업은행 한국산업은행
  //국민은행 신한은행 농협은행주식회사 하나은행 주식회사 케이뱅크 수협은행 토스뱅크 주식회사

  // 적금 상품 필터링 함수
  // const filteredSavingProducts = ref([])
  // const filterSavingProducts = function () {
  //   let filteredProducts = [...savingProducts.value]
  //       console.log(filteredProducts)
  //   if (saveTrmFilter.value) {
  //     filteredProducts = filteredProducts.filter(
  //       (product) => product.save_trm === saveTrmFilter.value
  //     )
  //   }
  //   if (intrRateTypeFilter.value) {
  //     filteredProducts = filteredProducts.filter(
  //       (product) => product.intr_rate_type_nm === intrRateTypeFilter.value
  //     )
  //   }
  //   if (korCoNmFilter.value) {
  //     filteredProducts = filteredProducts.filter(
  //       (product) => product.kor_co_nm === korCoNmFilter.value
  //     )
  //   }
  //   filteredSavingProducts.value = filteredProducts
  // }

  // // 예금 필터링 함수
  // const filteredDepositProducts = ref([])
  // const filterDepositProducts = function() {
  //   let filteredProducts = [...depositProducts.value]
  //   if (saveTrmFilter.value) {
  //     filteredProducts = filteredProducts.filter(product => product.save_trm === saveTrmFilter.value)
  //   }
  //   if (intrRateTypeFilter.value) {
  //     filteredProducts = filteredProducts.filter(product => product.intr_rate_type_nm === intrRateTypeFilter.value)
  //   }
  //   if (korCoNmFilter.value) {
  //     filteredProducts = filteredProducts.filter(product => product.kor_co_nm === korCoNmFilter.value)
  //   }
  //   filteredDepositProducts.value = filteredProducts
  // }




  return { getFindata, depositProducts, depositDetailProduct, savingProducts, savingDetailProduct,
          depositOptionProducts, savingOptionProducts,
          loadDepositAllData, loadDepositProducts, loadSavingProducts,loadDepositDetailProduct,
          loadDepositOptionProducts,loadSavingDetailProduct,loadSavingOptionProducts,
          deposit_bank, depositSaveTrm,
          depositBankData,saving_bank,savingBankData,filters, depositfilteredSave, depositfilteredIntr,
          savingfilteredIntr, savingIntrRate, savingfilteredSave,
          savingfilteredSaveTrm, savingfilteredIntrRate,
          depositfilteredSaveTrm, depostifilteredIntrRate 

   }
}, { persist: true })
