<template>
  <div>
    <p class="h4 mb-2">{{this.fileName}}</p>
    <b-list-group id="v-for-object" class="demo">
      <b-list-group-item style="padding: 2px; height: 24px; border: 0"
                         v-for="item in text"
                         :key="item.id"
                         :variant="item.status"
                         v-b-tooltip:bottom="'from database search:  ' + item.match"
      >
        <div class="d-flex flex-row">
          <pre style="width: 50px">{{ item.id }} </pre>
          <pre> {{ item.string }} </pre>
        </div>
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
export default {
  data() {
    return {
      fileName: null,
      text: [],
      code: 'Error?',

    }
  },

  methods: {
    getFile() {
      this.fileName = this.$router.history.current.path.replace(/^.*[\\//]/, '');
      let data = this.$store.getters.RESULTS.filter(file => file[1] === this.fileName)[0][0];
      console.log(data);
      let code = [];
      for (let i = 0; i < data[0].length; ++i) {
        let item = {};
        item['id'] = i
        code.push(data[0][i]);
        item['string'] = data[0][i];
        item['match'] = data[2][i];
        if (data[5][i] === 'plagiarism')
          item['status'] = 'danger';
        else if (data[5][i] === 'similar')
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
