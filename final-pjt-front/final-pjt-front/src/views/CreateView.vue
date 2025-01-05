<template>
  <div class="create-container">
    <div class="form-container">
      <h1 class="title">새 글 작성</h1>
      
      <form @submit.prevent="submitArticle" class="create-form">
        <div class="input-group">
          <label class="input-label">제목</label>
          <input 
            v-model="title"
            type="text"
            placeholder="제목을 입력해주세요"
            class="input-field"
            required
          >
        </div>
        
        <div class="input-group">
          <label class="input-label">내용</label>
          <textarea 
            v-model="content"
            rows="10"
            placeholder="내용을 입력해주세요"
            class="input-field textarea"
            required
          ></textarea>
        </div>
        
        <div class="button-group">
          <button 
            type="button"
            @click="$router.push({ name: 'community' })"
            class="cancel-button"
          >
            취소
          </button>
          <button 
            type="submit"
            class="submit-button"
          >
            등록
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useArticlesStore } from '@/stores/articles';

const store = useArticlesStore();
const title = ref('');
const content = ref('');

const submitArticle = () => {
  const articleData = {
    title: title.value,
    content: content.value
  };
  store.createArticle(articleData);
};

</script>


<style scoped>
.create-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.form-container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.title {
  color: #1a2b3c;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
}

.create-form {
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
  font-size: 1rem;
  font-weight: 600;
}

.input-field {
  padding: 0.8rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  width: 100%;
}

.input-field:focus {
  outline: none;
  border-color: #b4446c;
  box-shadow: 0 0 0 3px rgba(180, 68, 108, 0.1);
}

.textarea {
  resize: vertical;
  min-height: 200px;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.submit-button, .cancel-button {
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button {
  background-color: #b4446c;
  color: white;
  border: none;
}

.submit-button:hover {
  background-color: #963c5b;
}

.cancel-button {
  background-color: white;
  color: #666;
  border: 2px solid #ddd;
}

.cancel-button:hover {
  background-color: #f5f5f5;
  border-color: #ccc;
}

@media (max-width: 768px) {
  .create-container {
    padding: 1rem;
  }

  .form-container {
    padding: 1.5rem;
  }

  .title {
    font-size: 1.5rem;
  }

  .button-group {
    flex-direction: column;
  }

  .submit-button, .cancel-button {
    width: 100%;
  }
}
</style>