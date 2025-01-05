<template>
  <div class="container mx-auto px-4 py-6" v-if="store.article">
    <div class="bg-white rounded-lg shadow-lg p-6">
      <h1 class="text-3xl font-bold mb-4">{{ store.article.title }}</h1>

      <div class="flex justify-between items-center mb-6">
        <div class="text-gray-600">
          <span>작성자: {{ store.article.username }}</span>
          <span class="mx-2">|</span>
          <span>{{ store.article.created_at }}</span>
        </div>

        <div class="flex items-center space-x-4">
          <button
            @click="store.toggleLike(articleId)"
            class="flex items-center space-x-1"
          >
            <span>{{ store.article.is_liked ? "❤️" : "🤍" }}</span>
            <span>{{ store.article.like_count }}</span>
          </button>

          <div v-if="isAuthor">
            <button
              @click="store.deleteArticle(articleId)"
              class="text-red-500 hover:text-red-700"
            >
              삭제
            </button>
          </div>
        </div>
      </div>

      <div class="prose max-w-none mb-8">
        {{ store.article.content }}
      </div>

      <!-- 댓글 섹션 -->
      <div class="mt-8">
        <h3 class="text-xl font-bold mb-4">댓글</h3>

        <!-- 댓글 작성 폼 -->
        <div class="mb-6">
          <form @submit.prevent="submitComment" class="flex gap-2">
            <input
              v-model="newComment"
              type="text"
              class="comment-input"
              placeholder="댓글을 입력하세요"
              required
            />
            <button type="submit" class="submit-button">등록</button>
          </form>
        </div>

        <!-- 댓글 목록 -->
        <div v-if="store.article.comments && store.article.comments.length">
          <div
            v-for="comment in store.article.comments"
            :key="comment.id"
            class="comment-box"
          >
            <div>
              <span class="comment-author">{{ comment.username }}</span>
              <p class="comment-content">{{ comment.content }}</p>
              <span class="comment-date">{{
                formatDate(comment.created_at)
              }}</span>
            </div>
            <!-- 댓글 삭제 버튼 -->
            <button
              v-if="comment.is_author"
              @click="deleteComment(comment.id)"
              class="delete-button"
            >
              삭제
            </button>
          </div>
        </div>

        <!-- 댓글이 없을 때 -->
        <div v-else class="text-gray-500 text-center py-4">
          첫 댓글을 작성해보세요!
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { useArticlesStore } from "@/stores/articles";

const route = useRoute();
const store = useArticlesStore();
const articleId = route.params.id;
const newComment = ref("");

const currentUser = computed(() => localStorage.getItem("username") || "");
const isAuthor = computed(() => store.article?.is_author || false);

onMounted(() => {
  store.getArticle(articleId);
});

const submitComment = () => {
  if (newComment.value.trim()) {
    store.createComment(articleId, newComment.value);
    newComment.value = "";
  }
};

const deleteComment = (commentId) => {
  if (confirm("댓글을 삭제하시겠습니까?")) {
    store.deleteComment(articleId, commentId);
  }
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};
</script>

<style scoped>
/* 스타일 생략 */
</style>
