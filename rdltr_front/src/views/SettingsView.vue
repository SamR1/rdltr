<script setup lang="ts"></script>

<template>
  <div class="contnr" id="actionType">
    <div class="rdltr-box">
      <button class="btn-rdltr btn-rdltr-auto" @click="$router.push('/settings/categories')">
        Categories
      </button>
      <button class="btn-rdltr btn-rdltr-auto" @click="$router.push('/settings/tags')">Tags</button>
      <hr />
      <button class="btn-rdltr" @click="$router.push('/')">Back to home</button>
    </div>
  </div>
</template>

<style scoped>
.btn-rdltr-auto {
  margin-top: 0.5em;
}
</style>
