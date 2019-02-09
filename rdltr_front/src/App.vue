<template>
  <div id="app">
    <app-header />
    <router-view></router-view>
  </div>
</template>

<script>
import Header from './components/header/header.vue'

export default {
  name: 'app',
  components: {
    'app-header': Header,
  },
}
</script>

<style>
body,
html {
  color: #4e4e4e;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  margin: 0;
}

@media screen and (max-width: 400px) {
  .contnr {
    width: auto;
  }
}

.container {
  margin-top: 0.5em;
}

.article-content a {
  color: black;
}

.article-content img {
  display: block;
  margin-left: auto;
  margin-right: auto;
  max-width: 100%;
}

.article-content pre {
  background-color: #f4f4f4;
  padding: 0.5em;
}

.badge-rdltr {
  background-color: #8c95aa;
  color: white;
  margin-top: 1em;
  margin-bottom: 0.5em;
}

.btn-rdltr {
  background-color: #f5f5f7;
  border: 1px solid #8c95aa;
  color: #8c95aa;
  height: calc(2.25rem + 2px);
  padding: 0.5em 0.8em;
  font: inherit;
  cursor: pointer;
}

.btn-rdltr:hover {
  background-color: #8c95aa;
  color: white;
}

.btn-rdltr-auto {
  width: 100%;
}

.rdltr-box {
  width: 400px;
  margin: 30px auto;
  border: 1px solid #eee;
  padding: 20px;
  box-shadow: 0 2px 3px #ccc;
}

.rdltr-error {
  color: red;
  text-align: center;
}

@media screen and (max-width: 400px) {
  .rdltr-box {
    width: auto;
  }
}

.form-control {
  border-radius: 0;
}

.input {
  margin: 10px auto;
}

.input label {
  display: block;
  margin-bottom: 6px;
}

.input.inline label {
  display: inline;
}

.input input,
.input textarea {
  font: inherit;
  width: 100%;
  padding: 6px 12px;
  box-sizing: border-box;
  border: 1px solid #ccc;
}

.input.inline input {
  width: auto;
}

.input input:focus {
  outline: none;
  border: 1px solid #8c95aa;
  background-color: #eee;
}

.input select {
  border: 1px solid #ccc;
  font: inherit;
}

.link {
  color: #8c95aa;
}

.submit button {
  background-color: #f5f5f7;
  border: 1px solid #8c95aa;
  color: #8c95aa;
  padding: 10px 20px;
  font: inherit;
  cursor: pointer;
}

.submit button:hover,
.submit button:active {
  background-color: #8c95aa;
  color: white;
}

.submit button[disabled],
.submit button[disabled]:hover,
.submit button[disabled]:active {
  border: 1px solid #ccc;
  background-color: transparent;
  color: #ccc;
  cursor: not-allowed;
}
</style>
