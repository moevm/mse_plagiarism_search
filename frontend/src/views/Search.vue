<template>
  <div class="main-content">
    <p class="h4 mb-2">Plagiarism search</p>
    <div class="row">
      <!--      Left sub-menu -->
      <div class="col-8">
        <b-tabs content-class="mt-3">
          <b-tab title="File" active>
            <b-alert show variant="info"> supported formats: *.zip, *.rar, non-binary files.</b-alert>

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
        <b-form-group label="Search settings:">
          <b-form-checkbox
              v-for="option in searchOptions"
              v-model="selected"
              :key="option.value"
              :value="option.value"
              name="flavour-3a"
          >
            {{ option.text }}
          </b-form-checkbox>
        </b-form-group>

        <b-form-group label="Methods of search:">
          <b-form-checkbox
              v-for="option in methodsOptions"
              v-model="selected"
              :key="option.value"
              :value="option.value"
              name="flavour-3a"
          >
            {{ option.text }}
          </b-form-checkbox>
        </b-form-group>

        <b-form-group label="Open source:">
          <b-form-checkbox
              v-for="option in openSourceOptions"
              v-model="selected"
              :key="option.value"
              :value="option.value"
              name="flavour-3a"
          >
            {{ option.text }}
          </b-form-checkbox>
        </b-form-group>
        <!--        Footer content -->
        <b-button variant="primary" v-on:click="submit()">Start searching</b-button>
      </div>
    </div>
    <div>
      <div class="mt-3">Config selected : {{ file1 ? file1.name : '' }}, {{ selected }}</div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Search",
  data() {
    return {
      file1: null,
      file2: null,
      selected: [],

      searchOptions: [
        {text: 'Database search', value: 'database'},
        {text: 'Open source search', value: 'opensource'},
      ],
      methodsOptions: [
        {text: 'Levenshtein distance', value: 'levenshtein'},
        {text: 'PlagCheck', value: 'plagcheck'},
      ],
      openSourceOptions: [
        {text: 'BitBucket', value: 'bitbucket'},
        {text: 'StackOverflow', value: 'stackoverflow'},
        {text: 'GitHub', value: 'github'},
      ]
    }
  },
  methods: {
    submit() {
      let formData = new FormData();
      formData.append('file', this.file1);
      axios.post('http://127.0.0.1:5000/loadAndCheckFile',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data; charset=utf-8'
            }
          })
          .then((res) => {
            console.log('SUCCESS!!');
            console.log(res.data);
          })
          .catch(() => {
            console.log('FAILURE!!');
          });
    }
  }
}
</script>

<style scoped>

</style>