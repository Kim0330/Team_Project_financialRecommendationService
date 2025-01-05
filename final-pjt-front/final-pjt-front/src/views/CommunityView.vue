<template>
  <div class="community-container">
    <div class="header-section">
      <h1 class="title">Community</h1>
      <router-link 
        :to="{ name: 'CreateView' }"
        class="create-button"
      >
        ✍️ 글쓰기
      </router-link>
    </div>
    
    <div class="articles-grid">
      <div v-for="article in store.articles" 
           :key="article.id"
           class="article-card"
           @click="goToDetail(article.id)"
      >
        <h2 class="article-title">{{ article.title }}</h2>
        <div class="article-info">
          <div class="author-info">
            <span class="author-icon">👤</span>
            <span class="author-name">{{ article.username }}</span>
          </div>
          <div class="interaction-stats">
            <span class="stat-item">
              <span class="heart-icon">❤️</span>
              {{ article.like_count }}
            </span>
            <span class="stat-item">
              <span class="comment-icon">💬</span>
              {{ article.comments.length }}
            </span>
          </div>
        </div>
      </div>
    </div>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useArticlesStore } from '@/stores/articles';

const router = useRouter();
const store = useArticlesStore();

onMounted(() => {
  store.getArticles();
});

const goToDetail = (articleId) => {
  router.push({ name: 'ArticleDetailView', params: { id: articleId } });
};
</script>

<style scoped>
.community-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem 0;
}

.title {
  color: #1a2b3c;
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.create-button {
  background-color: #b4446c;
  color: white;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition: background-color 0.3s ease;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.create-button:hover {
  background-color: #963c5b;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.article-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.article-title {
  color: #1a2b3c;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
}

.author-name {
  font-weight: 500;
}

.interaction-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  color: #666;
  font-weight: 500;
}

.heart-icon, .comment-icon {
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .community-container {
    padding: 1rem;
  }
  
  .header-section {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .title {
    font-size: 2rem;
  }
  
  .articles-grid {
    grid-template-columns: 1fr;
  }
}
</style>