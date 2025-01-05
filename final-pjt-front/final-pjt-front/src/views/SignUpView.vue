<template>
  <div class="signup-container">
    <div class="signup-card">
      <h1 class="title">회원가입</h1>
      <form @submit.prevent="signUp" class="signup-form">
        
        <div class="input-group">
          <label for="username" class="input-label">아이디</label>
          <input 
            type="text" 
            id="username" 
            v-model.trim="formData.username" 
            required
            class="input-field"
          >
        </div>
        
        <div class="input-group">
          <label for="nickname" class="input-label">닉네임</label>
          <input 
            type="text" 
            id="nickname" 
            v-model.trim="formData.nickname" 
            required
            class="input-field"
          >
        </div>
 
        <div class="input-group">
          <label for="email" class="input-label">이메일</label>
          <input 
            type="email" 
            id="email" 
            v-model.trim="formData.email" 
            required
            class="input-field"
          >
        </div>
 
        <div class="input-group">
          <label for="password1" class="input-label">비밀번호</label>
          <input 
            type="password" 
            id="password1" 
            v-model.trim="formData.password1" 
            required
            class="input-field"
          >
        </div>
 
        <div class="input-group">
          <label for="password2" class="input-label">비밀번호 확인</label>
          <input 
            type="password" 
            id="password2" 
            v-model.trim="formData.password2" 
            required
            class="input-field"
          >
        </div>
 
        <div class="input-group">
          <label class="input-label">성별</label>
          <select 
            v-model="formData.gender" 
            required 
            class="select-field"
          >
            <option value="M">남성</option>
            <option value="F">여성</option>
          </select>
        </div>
 
        <div class="input-group">
          <label class="input-label">직업</label>
          <select 
            v-model="formData.occupation" 
            required 
            class="select-field"
          >
            <option value="S">학생</option>
            <option value="D">개발자</option>
          </select>
        </div>
 
        <button type="submit" class="submit-button">
          회원가입
        </button>
      </form>
    </div>
  </div>
 </template>

<script setup>
import { useUsersStore } from '@/stores/users';
import { ref } from 'vue'
const store = useUsersStore()


const formData = ref({
  username: '',
  email: '',
  password1: '',
  password2: '',
  nickname: '',
  gender: 'M',
  occupation: 'S',
})

const signUp = () => {
  console.log('SignUp 함수 호출됨')
  console.log(store)
  console.log(formData.value)
  store.signUp(formData.value)
}
</script>

<style scoped>
.signup-container {
 min-height: 100vh;
 padding: 2rem;
 background-color: #f5f5f5;
 display: flex;
 justify-content: center;
 align-items: center;
}

.signup-card {
 background: white;
 padding: 2rem;
 border-radius: 15px;
 box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
 width: 100%;
 max-width: 500px;
}

.title {
 color: #1a2b3c;
 font-size: 2rem;
 font-weight: 700;
 text-align: center;
 margin-bottom: 2rem;
}

.signup-form {
 display: flex;
 flex-direction: column;
 gap: 1.5rem;
}

.input-group {
 display: flex;
 flex-direction: column;
 gap: 0.5rem;
}

.input-label {
 color: #1a2b3c;
 font-size: 0.9rem;
 font-weight: 600;
}

.input-field, .select-field {
 padding: 0.8rem;
 border: 2px solid #ddd;
 border-radius: 8px;
 font-size: 1rem;
 transition: all 0.3s ease;
}

.input-field:focus, .select-field:focus {
 outline: none;
 border-color: #b4446c;
 box-shadow: 0 0 0 3px rgba(180, 68, 108, 0.1);
}

.select-field {
 background-color: white;
 cursor: pointer;
}

.submit-button {
 background-color: #b4446c;
 color: white;
 padding: 1rem;
 border: none;
 border-radius: 8px;
 font-size: 1rem;
 font-weight: 600;
 cursor: pointer;
 transition: background-color 0.3s ease;
 margin-top: 1rem;
}

.submit-button:hover {
 background-color: #963c5b;
}

@media (max-width: 768px) {
 .signup-container {
   padding: 1rem;
 }

 .signup-card {
   padding: 1.5rem;
 }

 .title {
   font-size: 1.5rem;
   margin-bottom: 1.5rem;
 }
}
</style>