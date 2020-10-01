<template>
  <li>
    <span v-bind:class="{done: todo.completed}">
      <input type="checkbox"
             v-on:change="todo.completed = !todo.completed">
      <strong>{{todo.id}}</strong>
      {{todo.title}}
    </span>
    <button v-on:click="emit('removeTodo', todo.id)">
      &times;
    </button>
  </li>
</template>

<script>
export default {
  props: {
    todo: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
  li {
    border: 1px solid #ccc;
    display: flex;
    justify-content: space-between;
    padding: .5em 2rem;
    margin-bottom: 1rem;
  }

  .done {
    text-decoration: line-through;
  }

</style>