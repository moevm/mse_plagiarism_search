<template>
  <div>
    <b-form-textarea
        class="overflow-auto"
        id="textarea"
        v-model="text"
        rows="20"
        max-rows="60"
        readonly
    ></b-form-textarea>
  </div>
</template>

<script>
export default {
  data() {
    return {
      text: 'CODE'
    }
  },
}
</script>