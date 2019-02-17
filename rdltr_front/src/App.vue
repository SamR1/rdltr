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

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
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
  margin-bottom: 1em;
  margin-top: 0.5em;
}

.fa-spinner {
  color: #8c95aa;
}

.alert {
  margin: 0.5em 0;
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

.btn-rdltr {
  background-color: #f5f5f7;
  border: 1px solid #8c95aa;
  color: #8c95aa;
  cursor: pointer;
  font: inherit;
  height: calc(2.25rem + 2px);
  padding: 0.5em 0.8em;
}

.btn-rdltr:hover {
  background-color: #8c95aa;
  color: white;
}

.btn-rdltr-auto {
  width: 100%;
}

.rdltr-box {
  border: 1px solid #eee;
  box-shadow: 0 2px 3px #ccc;
  margin: 30px auto;
  padding: 20px;
  width: 400px;
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
  box-sizing: border-box;
  border: 1px solid #ccc;
  font: inherit;
  padding: 6px 12px;
  width: 100%;
}

.input.inline input {
  width: auto;
}

.input input:focus {
  background-color: #eee;
  border: 1px solid #8c95aa;
  outline: none;
}

.input select {
  border: 1px solid #ccc;
  font: inherit;
}

.link {
  color: #8c95aa;
}

.multiselect__input {
  border-color: black;
}

.multiselect__option--highlight,
.multiselect__option--highlight:after {
  background: #8c95aa;
  color: #fff;
}

.multiselect__tag {
  background-color: #a3aabb;
}

.multiselect__tag-icon {
  color: white;
}

.multiselect__tag-icon:after {
  color: white;
}

.multiselect__tag-icon:focus,
.multiselect__tag-icon:hover {
  background: #8c95aa;
}

.multiselect__tags {
  border: 1px solid #ccc;
  border-radius: 0;
}

.submit button {
  background-color: #f5f5f7;
  border: 1px solid #8c95aa;
  font: inherit;
  color: #8c95aa;
  cursor: pointer;
  padding: 10px 20px;
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
