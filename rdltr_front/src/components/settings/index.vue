<template>
  <div class="contnr" id="actionType">
    <div class="rdltr-box">
      <router-link
        class="btn-rdltr btn-rdltr-auto"
        tag="button"
        to="/settings/categories"
      >
        Categories
      </router-link>
      <router-link
        class="btn-rdltr btn-rdltr-auto"
        tag="button"
        to="/settings/tags"
      >
        Tags
      </router-link>
      <hr />
      <router-link class="btn-rdltr" tag="button" to="/">
        Back to home
      </router-link>
    </div>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
.btn-rdltr-auto {
  margin-top: 0.5em;
}
</style>
