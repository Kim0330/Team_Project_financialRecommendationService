<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="welcome-text">WELCOME</h1>
      <h2 class="card-salad-text">CARD-SALAD</h2>
      
      <form @submit.prevent="logIn" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            type="text" 
            id="username" 
            v-model.trim="username"
            placeholder="Enter your username"
            class="form-input"
          >
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model.trim="password"
            placeholder="Enter your password"
            class="form-input"
          >
        </div>

        <button type="submit" class="login-button">
          LOGIN
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUsersStore } from '@/stores/users'

const username = ref(null)
const password = ref(null)
const store = useUsersStore()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.welcome-text {
  color: #1a2b3c;
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 10px;
  letter-spacing: 2px;
}

.card-salad-text {
  color: #b4446c;
  font-size: 2rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 30px;
  letter-spacing: 1px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
}

.form-input {
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #b4446c;
}

.login-button {
  margin-top: 10px;
  padding: 14px;
  background-color: #b4446c;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  font-family: 'squidFont';
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #963c5b;
}

.welcome-text {
  font-family: 'squidFont';
}

@media (max-width: 480px) {
  .login-card {
    padding: 20px;
  }

  .welcome-text {
    font-size: 2rem;
  
  }

  .card-salad-text {
    font-size: 1.5rem;
  }
}
</style>