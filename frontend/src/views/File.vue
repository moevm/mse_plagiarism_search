<template>
    <b-list-group id="v-for-object" class="demo">
      <b-list-group-item style="padding: 2px; height: 24px; border: 0"
          v-for="item in text"
          :key="item.id"
          :variant="item.status"
          v-b-tooltip:bottom="'from database search:  ' + item.match"
      >
        <div class="d-flex flex-row">
            <pre style="width: 50px">{{item.id}} </pre> <pre> {{item.string}} </pre>
        </div>
      </b-list-group-item>
    </b-list-group>
</template>

<script>
export default {
  data() {
    return {
      text: [],
      code: 'Error?'
    }
  },

  methods: {
    getFile() {
      let data = this.$store.getters.RESULT;
      let code = [];
      for(let i = 0; i < data[0].length; ++i)
      {
        let item = {};
        item['id'] = i
        code.push(data[0][i]);
        item['string'] = data[0][i];
        item['match'] = data[1][i];
        if (data[3][i] === 'plagiarism')
          item['status'] = 'danger';
        else if (data[3][i] === 'similar')
          item['status'] = 'warning';
        else
          item['status'] = 'success';
        this.text.push(item);
      }
      this.code = code.join('\n');
    },
  },

  mounted() {
    this.getFile();
  },
}
</script>