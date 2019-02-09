<template>
  <form>
    <div class="input">
      <label for="description">Comments</label>
      <textarea v-if="onCommentsEdition"
        id="description"
        v-model="comments"
        :disabled="!onCommentsEdition"
      >
      </textarea>
      <p id="comments" v-else>{{comments}}</p>
    </div>
    <div v-if="onCommentsEdition" class="submit">
      <button
        type="submit"
        @click.prevent="onSubmit()"
      >
        Submit
      </button>
      <button
        type="submit"
        @click.prevent="onCommentsEdition=!onCommentsEdition"
      >
        Cancel
      </button>
    </div>
    <div v-else>
      <button
        class="btn-rdltr"
        type="submit"
        @click.prevent="onCommentsEdition=!onCommentsEdition"
      >
        Edit comments
      </button>
    </div>
  </form>
</template>

<script>
export default {
  props: ['articleComments'],
  methods: {
    onSubmit () {
      this.$store.dispatch('updateArticle', {
        id: this.$route.params.id,
        formData: {
          comments: this.comments
        }
      }).then(() => {
        this.onCommentsEdition = false
      })
    }
  },
  data () {
    return {
      comments: '',
      onCommentsEdition: false
    }
  },
  beforeMount () {
    this.comments = this.articleComments
  }
}
</script>

<style scoped>
  #comments {
    font-style: italic;
    margin: .5em;
    white-space: pre;
  }
</style>
