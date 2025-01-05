<template>
  <div class="chatbot">
    <div class="header">
      <h2>금융상품 추천 AI 챗봇</h2>
    </div>
    <div class="messages">
      <div
        v-for="message in messages"
        :key="message.id"
        class="message"
        :class="message.sender"
      >
        {{ message.text }}
      </div>
    </div>
    <div class="input-area">
      <input
        v-model="userInput"
        @keyup.enter="sendMessage"
        placeholder="질문을 입력하세요..."
        type="text"
      />
      <button @click="sendMessage">전송</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Chatbot",
  data() {
    return {
      userInput: "",
      messages: [],
      messageId: 0,
    };
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim()) return;

      this.addMessage("user", this.userInput);
      const userMessage = this.userInput;
      this.userInput = "";

      try {
        const aiResponse = await this.getAIResponse(userMessage);
        this.addMessage("ai", aiResponse);
      } catch (error) {
        console.error("AI 응답 오류:", error);
        this.addMessage("ai", "죄송합니다, 오류가 발생했습니다.");
      }
    },

    async getAIResponse(message) {
      try {
        // 사용자 메시지와 데이터를 결합하여 GPT에 요청
        const response = await axios.post(
          import.meta.env.VITE_OPENAI_API_URL,
          {
            model: "gpt-4o-mini",
            messages: [
              {
                role: "system",
                content: `너는 금융 전문가야, 다양한 예적금 정보를 가지고 있고 사용자의 상황에 따라 금융상품을 추천할 수 있어.`
              },
              {
                role: "user",
                content: message,
              },
            ],
            temperature: 0.7,
            max_tokens: 1000,
          },
          {
            headers: {
              Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
              "Content-Type": "application/json",
            },
          }
        );

        return response.data.choices[0].message.content.trim();
      } catch (error) {
        console.error("API Error:", error.response?.data || error.message);
        throw error;
      }
    },

    addMessage(sender, text) {
      this.messages.push({
        id: this.messageId++,
        sender,
        text,
        timestamp: new Date(),
      });

      this.$nextTick(() => {
        const container = document.querySelector(".messages");
        container.scrollTop = container.scrollHeight;
      });
    },
  },
};
</script>

<style scoped>
/* 전체 레이아웃 */
.chatbot {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  height: 90vh;
  display: flex;
  flex-direction: column;
  font-family: "Noto Sans KR", sans-serif;
  border: 1px solid #e3e3e3;
  border-radius: 8px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

/* 헤더 스타일 */
.header {
  text-align: center;
  padding: 10px 0;
  border-bottom: 2px solid #007bff;
  color: #333;
  font-size: 20px;
  font-weight: bold;
}

/* 메시지 영역 */
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #ffffff;
}

/* 메시지 스타일 */
.message {
  margin: 10px 0;
  padding: 10px;
  border-radius: 5px;
  max-width: 80%;
  font-size: 15px;
  line-height: 1.5;
}

/* 사용자 메시지 */
.message.user {
  background-color: #007bff;
  color: white;
  margin-left: auto;
}

/* AI 메시지 */
.message.ai {
  background-color: #f1f1f1;
  color: #333;
  margin-right: auto;
}

/* 입력 영역 */
.input-area {
  display: flex;
  gap: 10px;
}

/* 입력 필드 */
input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
  font-family: inherit;
  background-color: #ffffff;
}

/* 입력 필드 포커스 */
input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* 전송 버튼 */
button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-family: inherit;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

/* 반응형 디자인 */
@media screen and (max-width: 768px) {
  .chatbot {
    max-width: 100%;
    height: 85vh;
    padding: 15px;
  }

  .header {
    font-size: 18px;
  }

  .message {
    font-size: 14px;
  }

  input {
    font-size: 14px;
  }
}
</style>
