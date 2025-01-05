import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useArticlesStore = defineStore(
  "articles",
  () => {
    const articles = ref([]);
    const article = ref(null);
    const API_URL = "http://127.0.0.1:8000";
    const token = ref(localStorage.getItem("token"));
    const router = useRouter();

    // 게시글 전체 조회
    const getArticles = function () {
      if (!token.value) return;

      axios({
        method: "get",
        url: `${API_URL}/api/v1/articles/`,
        headers: {
          Authorization: `Token ${token.value}`,
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          articles.value = res.data;
        })
        .catch((err) => console.error(err));
    };

    // 단일 게시글 조회
    const getArticle = function (articleId) {
      if (!token.value) return;

      axios({
        method: "get",
        url: `${API_URL}/api/v1/articles/${articleId}/`,
        headers: { Authorization: `Token ${token.value}` },
      })
        .then((res) => {
          article.value = res.data;
        })
        .catch((err) => console.error(err));
    };

    // 게시글 생성
    const createArticle = function (articleData) {
      if (!token.value) return;

      axios({
        method: "post",
        url: `${API_URL}/api/v1/articles/`,
        data: articleData,
        headers: { Authorization: `Token ${token.value}` },
      })
        .then(() => {
          router.push({ name: "community" }); // 작성 후 커뮤니티 페이지로 이동
        })
        .catch((err) => console.error(err));
    };

    // 게시글 삭제
    const deleteArticle = function (articleId) {
      if (!token.value) return;

      axios({
        method: "delete",
        url: `${API_URL}/api/v1/articles/${articleId}/`,
        headers: { Authorization: `Token ${token.value}` },
      })
        .then(() => {
          router.push({ name: "community" });
        })
        .catch((err) => console.error(err));
    };

    // 좋아요 토글
    const toggleLike = function (articleId) {
      if (!token.value) return;

      axios({
        method: "post",
        url: `${API_URL}/api/v1/articles/${articleId}/like/`,
        headers: { Authorization: `Token ${token.value}` },
      })
        .then(() => {
          getArticle(articleId);
        })
        .catch((err) => console.error(err));
    };

    // 댓글 생성
    const createComment = function (articleId, content) {
      if (!token.value) return;

      axios({
        method: "post",
        url: `${API_URL}/api/v1/articles/${articleId}/comments/`,
        data: { content },
        headers: { Authorization: `Token ${token.value}` },
      })
        .then(() => {
          getArticle(articleId);
        })
        .catch((err) => console.error(err));
    };

    // 댓글 삭제
    const deleteComment = function (articleId, commentId) {
      if (!token.value) return;

      axios({
        method: "delete",
        url: `${API_URL}/api/v1/articles/${articleId}/comments/${commentId}/`,
        headers: { Authorization: `Token ${token.value}` },
      })
        .then(() => {
          getArticle(articleId);
        })
        .catch((err) => console.error(err));
    };

    return {
      articles,
      article,
      getArticles,
      getArticle,
      createArticle,
      deleteArticle,
      toggleLike,
      createComment,
      deleteComment,
    };
  },
  { persist: true } // 상태 유지
);
