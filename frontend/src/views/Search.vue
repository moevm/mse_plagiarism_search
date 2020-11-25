<template>
  <div class="main-content">
    <p class="h4 mb-2">Plagiarism search</p>
    <div class="row">
      <!--      Left sub-menu -->
      <div class="col-8">
        <b-tabs content-class="mt-3">
          <b-tab title="File" active>
            <!-- <b-alert show variant="info"> supported formats: *.zip, *.rar, non-binary files.</b-alert> -->
            <b-alert variant="info"> supported formats: *.js, *.java, *.cpp, *.c, non-binary files.</b-alert>
            <b-form-file
                v-model="file1"
                :state="Boolean(file1)"
                placeholder="Choose a file or drop it here..."
                drop-placeholder="Drop file here..."
            ></b-form-file>

          </b-tab>
          <b-tab title="Git">

            <div class="input-group mb-3">
              <input type="text" class="form-control" id="basic-url" aria-describedby="basic-addon3">
              <div class="input-group-append">
                <button class="btn btn-outline-secondary" type="button">Add</button>
              </div>
            </div>


          </b-tab>
        </b-tabs>
      </div>
      <!--      Right sub-menu -->
      <div class="col-4">
        <label> Search settings: </label>
          <b-form-checkbox-group
              v-model="selectedSearchOptions"
              :options="searchOptions"
              class="mb-3"
              value-field="value"
              text-field="text"
              disabled-field="notEnabled"
          >
          </b-form-checkbox-group>

        <label> Methods of search:</label>
          <b-form-checkbox-group
              v-model="selectedMethodsOptions"
              :options="methodsOptions"
              class="mb-3"
              value-field="value"
              text-field="text"
              disabled-field="notEnabled"
          >
          </b-form-checkbox-group>

        <label> Open source:</label>
        <b-form-checkbox-group
            v-model="selectedOpenSourceOptions"
            :options="openSourceOptions"
            class="mb-3"
            value-field="value"
            text-field="text"
            disabled-field="notEnabled"
        >
        </b-form-checkbox-group>

        <!--        Footer content -->
        <b-button variant="primary" v-on:click="submit()">Start searching</b-button>
      </div>
    </div>
  </div>
</template>

<script>
import router from "@/router";

export default {
  name: "Search",
  data() {
    return {
      file1: null,
      file2: null,

      selectedSearchOptions: [],
      selectedMethodsOptions: [],
      selectedOpenSourceOptions: [],

      searchOptions: [
        {text: 'Database search', value: 'database'},
        {text: 'Open source search', value: 'opensource', notEnabled: true},
      ],
      methodsOptions: [
        {text: 'Levenshtein distance', value: 'levenshtein'},
        {text: 'PlagCheck', value: 'plagcheck', notEnabled: true},
      ],
      openSourceOptions: [
        {text: 'StackOverflow', value: 'stackoverflow', notEnabled: true},
        {text: 'GitHub', value: 'github', notEnabled: true},
      ]
    }
  },
  methods: {
    /*
    #TODO
      - нормальная обработка чекбокса;
    */
    submit() {
        if (this.selectedSearchOptions.length && this.selectedMethodsOptions.length && this.file1) {
          let formData = new FormData();
          formData.append('file', this.file1);

          const intervalID = setInterval(() => {
            console.log('загрузка')
          }, 200);

          this.$store.dispatch('SET_RESULT', formData).then(() => {
            clearInterval(intervalID);
            console.log('...загрузка завершена');
            router.push('./search/result');
          })
        }
    },

    },

  watch: {
    $route(to, from) {
      const toDepth = to.path.split('/').length
      const fromDepth = from.path.split('/').length
      this.transitionName = toDepth < fromDepth ? 'slide-right' : 'slide-left'
    }
  }
}
</script>

<style scoped>

</style>