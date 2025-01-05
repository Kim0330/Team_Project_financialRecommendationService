import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import swal from 'sweetalert'

export const useUsersStore = defineStore('users', () => {

  const API_URL = 'http://127.0.0.1:8000'
  // 새로고침을 하더라도 로그아웃되지 않기 위해서는 이렇게 만들어야 함
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)
  const isLogin = computed(() => token.value !== null)
  const router = useRouter()
  
  // 회원가입 
    const signUp = function(payload) {
      axios({
        method: 'post',
        url: `${API_URL}/dj-rest-auth/registration/`,
        data: payload,
        // headers: {
        //   Authorization: `Token ${token.value}`
        // } // 회원가입시에는 토큰이 있긴하지만 받지 않음!
      })
        .then((res) => {
          const LogInfo = {
            username: payload.username,
            email: payload.email,
            password : payload.password1,
          }
          console.log(LogInfo)
          // console.log(res.data) : 토큰이 키밸류로 들어옴
          console.log(LogInfo.username)
          swal(`${LogInfo.username}님 저랑 게임 하나 하시겠습니까?`, {
            buttons: false,
            timer: 1000,
          });
          // 회원가입 성공 후 자동으로 로그인
          logIn(LogInfo)
        })
        .catch((err) => {
          console.error(err)
          alert('회원가입에 실패했습니다.')
        })
    }


  // 로그인 요청
  const logIn = function(payload) {
    axios({
      method: "post",
      url: `${API_URL}/dj-rest-auth/login/`,
      data: payload
    })
      .then((res) => {
        // 토큰저장하기
        token.value = res.data.key
        localStorage.setItem('token', res.data.key)
        localStorage.setItem('username', payload.username)
        user.value = payload

        // 로그인 성공 후 전체 유저 정보 가져오기
        getUserProfile(payload.username)
        console.log(token.value)
        console.log(payload)
        swal(`${payload.username}님 무궁화 꽃이 피었습니다!`, {
          buttons: false,
          timer: 1000,
        });
        router.push({name:'home'})
      })
      .catch((err) => {
        console.error(err)
        alert('로그인에 실패했습니다.')
      })
  }

  // 로그아웃
  const logOut = function() {
    const username = user.value?.username

    axios({
      method: 'post',
      url: `${API_URL}/dj-rest-auth/logout/`,
      headers: {
          Authorization: `Token ${token.value}`
        }
    })
      .then(() => {
        token.value = null
        user.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('username')
        swal(`${username}님 우리는 깐부잖아! 곧 다시 만나길 기대할게요. 😊`, {
          buttons: false,
          timer: 1000,
        });
        router.push({name:'home'})
      })
      .catch((err) => console.log(err))
  }

  // 마이페이지 정보 조회
  const getUserProfile = function(username) {
      
      axios({
        method: 'get',
        url: `${API_URL}/accounts/page/${username}/`,
        headers: { 
          Authorization: `Token ${token.value}` 
        }
      })
        .then((res) => {
          user.value = res.data
          console.log(res.data)
        })
        .catch((err) => console.error(err))
    }
  
  // 마이페이지 정보 수정
  const updateUserProfile = function(username, updateData) {

    const updatedData = {
      ...user.value,  // 기존 정보 유지
      ...updateData   // 수정된 정보로 덮어쓰기
    }
    axios({
      method: 'put',
      url: `${API_URL}/accounts/page/${username}/`,
      data: updateData,
      headers: { 
        Authorization: `Token ${token.value}` 
      }
    })
    .then((res) => {
      user.value = res.data
    })
    .catch((err) => console.error(err))
  }

  // 회원 탈퇴
  const deleteAccount = function(username) {
    if (!confirm('깐부! 정말 탈퇴하시겠습니까?')) return
    
    axios({
      method: 'delete',
      url: `${API_URL}/accounts/delete/${username}/`, 
      headers: { 
        Authorization: `Token ${token.value}`,
        // csrf 토큰 추가
        // 'X-CSRFToken': 'csrftoken' 
      }
    })
      .then(() => {
        token.value = null
        user.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('username')
        router.push({ name: 'home' })
      })
      .catch((err) => console.log(err))
  }
  return {
  
    signUp,
    logIn,
    isLogin,
    logOut,
    getUserProfile,
    updateUserProfile,
    deleteAccount,user, token

  }
}, { persist: true })