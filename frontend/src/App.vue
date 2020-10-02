<template>
  <div id="app">
    <component :is="layout">
      <router-view/>
    </component>
  </div>
</template>

<script>
import DefaultLayout from "@/layouts/DefaultLayout";

export default {
  computed: {
    layout() {
      return this.$route.meta.layout || 'default-layout'
    }
  },
  components: {
    DefaultLayout
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

html,
body {
  margin: 0;
  padding: 0;
  background-color: #D8D8D8;
}
</style>
