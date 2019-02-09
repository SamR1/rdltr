<template>
  <div class="not-found">
    <div class="test">
      <p>Page not found!</p>
      <br />
      <router-link class="btn-rdltr" tag="button" to="/">
        Back to home
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  align-items: center;
  display: flex;
  height: 50vh;
  margin: 30px auto;
  padding: 20px;
  text-align: center;
  width: 400px;
}
.test {
  text-align: center;
  width: 100%;
}
</style>
