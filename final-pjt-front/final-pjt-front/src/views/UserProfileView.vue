<template>
  <div class="profile-container">
    <div class="profile-card">
      <h1 class="title">프로필</h1>

      <div v-if="store.user" class="profile-content">
        <div class="profile-image-section">
          <h3 class="section-title">프로필 이미지</h3>
          <div class="image-container">
            <img src="@/assets/images/default_img.png" alt="default_img" class="profile-image">
          </div>
        </div>

        <div class="info-grid">
          <div class="info-item">
            <h3 class="info-label">아이디</h3>
            <p class="info-value">{{ store.user.username }}</p>
          </div>
          <div class="info-item">
            <h3 class="info-label">닉네임</h3>
            <p class="info-value">{{ store.user.nickname }}</p>
          </div>
          <div class="info-item">
            <h3 class="info-label">이메일</h3>
            <p class="info-value">{{ store.user.email }}</p>
          </div>
          <div class="info-item">
            <h3 class="info-label">나이</h3>
            <p class="info-value">{{ store.user.age }}</p>
          </div>
          <div class="info-item">
            <h3 class="info-label">성별</h3>
            <p class="info-value">{{ store.user.gender === "M" ? "남성" : "여성" }}</p>
          </div>
          <div class="info-item">
            <h3 class="info-label">직업</h3>
            <p class="info-value">{{ store.user.occupation === "S" ? "학생" : "개발자" }}</p>
          </div>
          <div class="info-item">
            <h3 class="info-label">가입일</h3>
            <p class="info-value">{{ formatDate(store.user.data_joined) }}</p>
          </div>
        </div>

        <div class="button-container">
          <button @click="openModal" class="edit-button">정보수정</button>
          <button @click="store.deleteAccount(store.user.username)" class="delete-button">
            회원탈퇴
          </button>
        </div>
      </div>
    </div>

    <!-- 모달 -->
    <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h2 class="modal-title">프로필 수정</h2>
        <form @submit.prevent="handleSubmit" class="edit-form">
          <div class="form-group">
            <label>닉네임</label>
            <input v-model="updateData.nickname" :placeholder="store.user.nickname" class="form-input">
          </div>

          <div class="form-group">
            <label>이메일</label>
            <input v-model="updateData.email" type="email" :placeholder="store.user.email" class="form-input">
          </div>

          <div class="form-group">
            <label>나이</label>
            <input v-model="updateData.age" type="number" :placeholder="store.user.age" class="form-input">
          </div>

          <div class="form-group">
            <label>성별</label>
            <select v-model="updateData.gender" class="form-select">
              <option value="M">남성</option>
              <option value="F">여성</option>
            </select>
          </div>

          <div class="form-group">
            <label>직업</label>
            <select v-model="updateData.occupation" class="form-select">
              <option value="S">학생</option>
              <option value="D">개발자</option>
            </select>
          </div>

          <div class="modal-buttons">
            <button type="submit" class="save-button">저장</button>
            <button type="button" @click="closeModal" class="cancel-button">취소</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script setup>

import { useUsersStore } from "@/stores/users";
import { onMounted, ref } from "vue";
const store = useUsersStore();

// 상태 관리
const isModalOpen =ref(false)
const user= ref(localStorage.getItem('username'))
const username = user.value
console.log(username)
console.log(store.user.nickname)
console.log(store.user.username)
console.log(store.user.email)
console.log(store.user.profile_img)

const handleSubmit = function (){
  store.updateUserProfile(username, updateData);
  isModalOpen.value = false;
}

// updateData는 store.user의 현재 데이터를 사용
const updateData = ref({});

// 모달 열 때 현재 사용자 정보로 설정
const openModal = () => {
  updateData.value = {
    nickname: store.user.nickname,
    email: store.user.email,
    age: store.user.age,
    gender: store.user.gender,
    occupation: store.user.occupation
  };
  isModalOpen.value = true;
};

// 모달 닫기 - 추가
const closeModal = () => {
  isModalOpen.value = false;
};

const formatDate= function (dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

onMounted(() => {
  store.getUserProfile(username);  
  console.log(store.user.username)
});
</script>

<style scoped>
.profile-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.profile-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.title {
  color: #1a2b3c;
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2rem;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-image-section {
  text-align: center;
}

.image-container {
  width: 150px;
  height: 150px;
  margin: 1rem auto;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #b4446c;
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.info-item {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.info-label {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.info-value {
  color: #1a2b3c;
  font-size: 1.1rem;
  font-weight: 500;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.edit-button, .delete-button {
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-button {
  background-color: #b4446c;
  color: white;
  border: none;
}

.edit-button:hover {
  background-color: #963c5b;
}

.delete-button {
  background-color: white;
  color: #dc3545;
  border: 2px solid #dc3545;
}

.delete-button:hover {
  background-color: #dc3545;
  color: white;
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
  width: 90%;
  max-width: 500px;
}

.modal-title {
  color: #1a2b3c;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-align: center;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
}

.form-input, .form-select {
  padding: 0.8rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #b4446c;
}

.modal-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.save-button, .cancel-button {
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-button {
  background-color: #b4446c;
  color: white;
  border: none;
}

.save-button:hover {
  background-color: #963c5b;
}

.cancel-button {
  background-color: white;
  color: #666;
  border: 2px solid #ddd;
}

.cancel-button:hover {
  background-color: #f5f5f5;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 1rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .button-container {
    flex-direction: column;
  }

  .edit-button, .delete-button {
    width: 100%;
  }
}
</style>