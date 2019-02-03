<template>
  <div id="welcome">
    <h1>rdltr</h1>
    <p>a simple "read-it later" app!</p>
    <div class="cta">
      <router-link to="/register">Register</router-link>
      <router-link to="/login">Log In</router-link>
    </div>
  </div>
</template>

<style scoped>
  #welcome {
    width: 80%;
    margin: auto;
  }

  h1 {
    text-align: center;
  }

  p {
    text-align: center;
  }

  .cta {
    width: 300px;
    margin: auto;
    text-align: center;
  }

  .cta a {
    margin: 10px;
    text-decoration: none;
    display: inline-block;
    border: 1px solid #8c95aa;
    border-radius: 3px;
    width: 100px;
    padding: 10px;
    box-sizing: border-box;
    color: #8c95aa;
  }

  .cta a:hover,
  .cta a:active {
    background-color: #8c95aa;
    color: white;
  }
</style>
