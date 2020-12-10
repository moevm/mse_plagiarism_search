<template>
  <div class="main-content">
    <loading :active.sync="isLoading"
             :is-full-page="isFullPage"
    >
    </loading>
    <p class="h4 mb-2">Plagiarism search</p>
    <div class="row">
      <!--      Left sub-menu -->
      <div class="col-8">
        <b-tabs content-class="mt-3">
          <b-tab title="File" active>
            <b-alert variant="info" show> supported formats: *.zip, *.js, *.java, *.cpp, *.c, *.py, *.h, *.hpp
              non-binary files.
            </b-alert>
            <p></p>

            <b-form-file
                v-model="file"
                :state="Boolean(file)"
                placeholder="Choose a file or drop it here..."
                drop-placeholder="Drop file here..."
                accept=".js, .c, .cpp, .java, .py, .h, .hpp, .zip"
            ></b-form-file>
            <p></p>
            <b-alert v-model="isEmptyFileInput" variant="danger" dismissible>
              You must select a file
            </b-alert>
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
        <b-alert v-model="isEmptyCheckboxes" variant="warning" id="danger" dismissible>
          you must select the search method and the associated method!
        </b-alert>
        <b-button variant="primary" v-on:click="submit()">
          Start searching
        </b-button>
      </div>
    </div>
  </div>
</template>

<script>
import router from "@/router";
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

export default {
  name: "Search",
  data() {
    return {
      file: null,

      isLoading: false,
      isFullPage: true,
      isEmptyCheckboxes: false,
      isEmptyFileInput: false,

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
    submit() {
      if (this.selectedSearchOptions.length && this.selectedMethodsOptions.length && this.file) {
        this.isEmptyCheckboxes = false;
        this.isEmptyFileInput = false;
        let formData = new FormData();
        formData.append('file', this.file);

        const intervalID = setInterval(() => {
          console.log('загрузка');
          this.isLoading = true;
        }, 200);

        this.$store.dispatch('SET_RESULT', formData)
            .then(() => {
              this.$store.dispatch('SET_FILENAME', this.file.name)
              clearInterval(intervalID);
              console.log('...загрузка завершена');
              this.isLoading = false;
              router.push('./search/result');
            });
      } else if (!this.file) {
        this.isEmptyFileInput = true;
      } else {
        this.isEmptyCheckboxes = true;
      }
    },

  },

  watch: {
    $route(to, from) {
      const toDepth = to.path.split('/').length
      const fromDepth = from.path.split('/').length
      this.transitionName = toDepth < fromDepth ? 'slide-right' : 'slide-left'
    }
  },

  components: {
    Loading
  }
}
</script>
