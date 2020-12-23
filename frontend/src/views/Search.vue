<template>
  <div class="main-content">
    <loading :active.sync="isLoading"
             :is-full-page="isFullPage"
    >
    </loading>
    <p class="h4 mb-2">Plagiarism search</p>
    <!-- Left sub-menu -->
    <b-tabs content-class="mt-3">
      <b-tab title="File" active>
        <b-form-group
            label="File input:"
            label-for="file-input"
            description="file will be loaded into the database, supported formats: *.zip, *.js, *.java, *.cpp, *.c, *.py, *.h, *.hpp
              non-binary files."
            class="mb-0"
            v-model="files"
        >
          <b-form-file
              id="file-input"
              v-model="files"
              :state="Boolean(files)"
              placeholder="Choose a file or drop it here..."
              drop-placeholder="Drop file here..."
              multiple accept=".js, .c, .cpp, .java, .py, .h, .hpp, .zip"
          ></b-form-file>
        </b-form-group>

        <b-alert v-model="isEmptyFileInput" variant="danger" dismissible>
          You must select a file
        </b-alert>

        <b-button variant="primary" v-on:click="submitFile()" style="margin-top: 10px">
          Start searching
        </b-button>
      </b-tab>

      <b-tab title="GitHub">
        <b-form-group
            label="GitHub repository link:"
            label-for="github-url"
            description="repository will be loaded into the database"
            class="mb-0"
            v-model="repository"
        >
          <b-form-input
              id="github-url"
              placeholder="Enter your repository..."
          ></b-form-input>
        </b-form-group>

        <b-form-checkbox v-model="isPrivateRepo" name="check-button" style="margin-top: 10px" switch>
          private repository
        </b-form-checkbox>

        <div class="container" id="app-container" v-if="isPrivateRepo" style="margin-top: 10px">
          <b-form-group
              label="Your GitHub nickname:"
              label-for="login"
              class="mb-0"
              v-model="login"
          >
            <b-form-input
                id="login"
                placeholder="Enter Login..."
            ></b-form-input>
          </b-form-group>

          <b-form-group
              label="Your organization:"
              label-for="organization"
              class="mb-0"
              v-model="organization"
              style="margin-top: 10px"
          >
            <b-form-input
                id="organization"
                placeholder="Enter Organization..."
            ></b-form-input>
          </b-form-group>

          <b-form-group
              label="Your token:"
              label-for="token"
              class="mb-0"
              v-model="token"
              style="margin-top: 10px"
          >
            <b-form-input
                id="token"
                placeholder="Enter Token..."
            ></b-form-input>
          </b-form-group>
        </div>

        <b-button variant="primary" v-on:click="submitRepository()" style="margin-top: 10px">
          Start searching
        </b-button>
      </b-tab>

    </b-tabs>
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
      files: [],
      repository: null,
      login: null,
      organization: null,
      token: null,
      isLoading: false,
      isFullPage: true,
      isEmptyFileInput: false,
      isPrivateRepo: true
    }
  },
  methods: {
    submitFile() {
      if (this.files.length !== 0) {
        this.isEmptyFileInput = false;
        let formData = new FormData();
        for(let i = 0; i < this.files.length; ++i)
          formData.append('file', this.files[i]);

        const intervalID = setInterval(() => {
          console.log('загрузка');
          this.isLoading = true;
        }, 200);

        this.$store.dispatch('SET_RESULTS',  formData)
            .then(() => {
              clearInterval(intervalID);
              console.log('...загрузка и обработка файлов завершена');
              this.isLoading = false;
              router.push('./search/result');
            });
      } else {
        this.isEmptyFileInput = true;
      }
    },

    submitRepository() {
      /* const intervalID = setInterval(() => {
        console.log('загрузка');
        this.isLoading = true;
      }, 200);

      if(this.isPrivateRepo) {

      } else {

      }*/
    }

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
