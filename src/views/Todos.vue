<template>
  <div id="app">
    <h1>TODO app</h1>
    <router-link to="/">home</router-link>
    <hr>
    <TodoList
        v-bind:todos="todos"
        @removeTodo="removeTodo"
    />
  </div>
</template>

<script>
import TodoList from '@/components/TodoList'
export default {
  name: 'App',
  data() {
    return {
      todos: [
        {id: 1, title: 'Купить хлеб', completed: false},
        {id: 2, title: 'Купить масло', completed: false},
        {id: 3, title: 'Купить пиво', completed: false},
      ]
    }
  },
  methods: {
    removeTodo(id) {
      this.todos = this.todos.filter(t => t.id !== id);
    }
  },
  components: {
    TodoList
  }
}
</script>

<style scoped>

</style>