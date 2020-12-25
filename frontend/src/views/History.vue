<template>
  <div>
    <p class="h4 mb-2">History</p>
    <ul id="example-1">
      <li v-for="item in items" :key="item.id" v-on:click="submitResult(item.id)">
        <b-link>{{item.id}} : {{ item.link }}</b-link>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
import {URL} from "@/url.config";
import router from "@/router";

export default {
  data() {
    return {
      items: [],
      isLoading: false
    }
  },

  methods: {
    submitResult(id) {

      const intervalID = setInterval(() => {
        console.log('загрузка');
        this.isLoading = true;
      }, 100);


      this.$store.dispatch('SET_HISTORY_RESULTS',  id)
          .then(() => {
            clearInterval(intervalID);
            console.log('...загрузка и обработка файлов завершена');
            this.isLoading = false;
            router.push('./search/result');
          });
      },

    getHistory() {
      axios.get(`${URL + 'getAllResults'}`)
          .then(res => {
            console.log(res.data)
            for (let i = 0; i < res.data.length; ++i) {

              this.items.push({
                'id': res.data[i][0],
                'link': res.data[i][2]
              });
              console.log(res.data[i][2])
            }
          });
    },
  },

  created() {
    this.getHistory();
  }
}
</script>
