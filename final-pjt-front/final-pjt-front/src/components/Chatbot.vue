// FinancialChatBot.vue
<template>
  <div class="chat-container">
    <!-- 채팅 메시지를 표시하는 영역 -->
    <div class="chat-messages" ref="messageContainer">
      <!-- 각 메시지를 순회하며 표시 -->
      <div v-for="(message, index) in messages" 
           :key="index" 
           :class="[
             'message',
             message.role === 'user' ? 'user-message' : 'assistant-message'
           ]">
        <!-- 메시지 내용 표시 -->
        <div class="message-content">
          <!-- 상품 추천일 경우 -->
          <div v-if="message.type === 'products'" class="product-recommendations">
            <div v-for="product in message.products" 
                 :key="product.id" 
                 class="product-card">
              <h3>{{ product.bankName }}</h3>
              <div class="product-info">
                <p>상품명: {{ product.productName }}</p>
                <p>금리: {{ product.interestRate }}%</p>
                <p>기간: {{ product.term }}개월</p>
              </div>
            </div>
          </div>
          <!-- 일반 텍스트 메시지일 경우 -->
          <div v-else v-html="message.content"></div>
        </div>
      </div>
    </div>

    <!-- 입력 영역 -->
    <div class="input-area">
      <!-- 로딩 표시 -->
      <div v-if="loading" class="loading-bar"></div>
      
      <!-- 메시지 입력 폼 -->
      <div class="input-container">
        <input 
          v-model="userInput" 
          @keyup.enter="sendMessage"
          placeholder="금융 상품 추천을 요청해보세요!"
          :disabled="loading"
        >
        <button @click="sendMessage" :disabled="loading">
          전송
        </button>
        <button @click="resetChat" :disabled="loading">
          초기화
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useDepositStore } from '@/stores/financialProductsStore';
import { ref, onMounted } from 'vue'
import axios from 'axios'

const store = useDepositStore()

// 상태 관리를 위한 ref 선언
const messages = ref([
  { role: 'assistant', content: '안녕하세요! 금융 상품 추천 챗봇입니다. 어떤 상품을 찾으시나요?' }
])

// 사용자 입력값
const userInput = ref('')
const loading = ref(false)
const messageContainer = ref(null)

// 금융 상품 데이터 저장
const depositProducts = ref([])
const savingProducts = ref([])

// 초기 데이터 로드
onMounted(async () => {
  try {
    // 예금/적금 데이터 로드 (실제 환경에서는 API나 파일에서 로드)
    const depositResponse = store.depositProducts
    const savingResponse = store.savingProducts
    
    depositProducts.value = depositResponse.default
    savingProducts.value = savingResponse.default
  } catch (error) {
    console.error('상품 데이터 로드 실패:', error)
  }
})

// 메시지 전송 처리
const sendMessage = async () => {
  if (!userInput.value.trim() || loading.value) return
  
  loading.value = true
  
  try {
    // 사용자 메시지 추가
    messages.value.push({
      role: 'user',
      content: userInput.value
    })
    
    // API 요청 데이터 준비
    const requestData = {
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: `당신은 금융 상품 추천 전문가입니다. 다음 데이터를 기반으로 답변해주세요:
          예금상품: ${JSON.stringify(depositProducts.value)}
          적금상품: ${JSON.stringify(savingProducts.value)}`
        },
        ...messages.value.map(m => ({
          role: m.role,
          content: m.content
        }))
      ]
    }
    
    // API 호출
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      requestData,
      {
        headers: {
          'Authorization': `Bearer ${import.meta.env.VITE_AI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    )
    
    // 응답 처리
    const botResponse = response.data.choices[0].message.content
    messages.value.push({
      role: 'assistant',
      content: botResponse
    })
    
    // 입력창 초기화
    userInput.value = ''
    
  } catch (error) {
    console.error('API 오류:', error)
    messages.value.push({
      role: 'assistant',
      content: '죄송합니다. 오류가 발생했습니다. 다시 시도해주세요.'
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

// 채팅 초기화
const resetChat = () => {
  messages.value = [{
    role: 'assistant',
    content: '안녕하세요! 금융 상품 추천 챗봇입니다. 어떤 상품을 찾으시나요?'
  }]
  userInput.value = ''
}

// 스크롤을 항상 최신 메시지로
const scrollToBottom = () => {
  setTimeout(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  }, 100)
}
</script>

<style scoped>
.chat-container {
  width: 100%;
  max-width: 600px;
  height: 80vh;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f5f5;
}

.message {
  margin-bottom: 15px;
  max-width: 80%;
}

.user-message {
  margin-left: auto;
  background: #fff6ce;
  padding: 10px 15px;
  border-radius: 20px;
}

.assistant-message {
  margin-right: auto;
  background: white;
  padding: 10px 15px;
  border-radius: 20px;
}

.input-area {
  padding: 20px;
  background: white;
  border-top: 1px solid #ddd;
}

.input-container {
  display: flex;
  gap: 10px;
}

.loading-bar {
  height: 2px;
  background: linear-gradient(to right, #f0f0f0, #ddd, #f0f0f0);
  animation: loading 1.5s infinite;
}

.product-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;
}

@keyframes loading {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background: #007bff;
  color: white;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}

button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}
</style>

