<template>
  <div class="col-sm-6 col-md-4 col-lg-3">
    <conf-modal
      v-if="showModal"
      :title="article.title"
      :onDeleteArticle="onDeleteArticle"
      @close="showModal = false"
    ></conf-modal>
    <div class="card" :class="`status${article.read ? '-read' : ''}`">
      <div class="card-body">
        <button
          aria-label="Close"
          class="close"
          title="delete article"
          type="button"
          @click="showModal = true"
        >
          <span aria-hidden="true">&times;</span>
        </button>
        <app-badge :name="article.category.name"></app-badge>
        <h5 class="card-title">{{ article.title }}</h5>
        <app-badge
          v-for="tag in article.tags"
          :tag_id="tag.id"
          :is-tag="true"
          :key="tag.id"
          :name="tag.name"
        ></app-badge>
        <p class="card-text"></p>
      </div>
      <div class="card-footer">
        <router-link
          class="btn-rdltr"
          tag="button"
          :to="{ name: 'articleDetail', params: { id: article.id } }"
        >
          Read
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import CustomBadge from '../common/customBagde'
import ConfModal from '../common/deleteConfirmationModal'

export default {
  components: {
    AppBadge: CustomBadge,
    ConfModal: ConfModal,
  },
  props: ['article'],
  data: function() {
    return {
      showModal: false,
    }
  },
  methods: {
    onDeleteArticle() {
      return this.$store.dispatch('deleteArticle', this.article.id)
    },
  },
}
</script>

<style scoped>
.card {
  box-shadow: 0 2px 3px #ccc;
  margin: 0.5em 0;
}

.card-footer {
  background-color: transparent;
  border: none;
}

.status-read {
  opacity: 0.5;
}
</style>
