<template>
  <div class="overflow">
    <!-- File add controls -->
    <b-form-file class="mb-2"
                 v-model="file1"
                 :state="Boolean(file1)"
                 placeholder="Choose a file or drop it here..."
                 drop-placeholder="Drop file here..."
                 accept=".js, .c, .cpp, .java, .py, .h, .hpp"
    ></b-form-file>
    <b-button variant="primary" v-on:click="submitFile()"> Upload </b-button>

    <!-- Main table element -->
    <b-table
        show-empty
        striped
        bordered
        head-variant="light"
        stacked="md"
        :items="items"
        :fields="fields"
        :current-page="currentPage"
        :per-page="perPage"
        :filter="filter"
        :filter-included-fields="filterOn"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :sort-direction="sortDirection"
        :sort-compare="dateCompare"
        @filtered="onFiltered"
    >

      <template v-slot:cell(actions)="row">
        <b-button size="sm" @click="deleteItem(row.index)">
          Delete
        </b-button>
      </template>
    </b-table>

    <!-- User Interface controls -->
    <b-row>
      <b-col sm="2">
        <b-form-select
            v-model="perPage"
            id="perPageSelect"
            size="sm"
            :options="pageOptions"
        ></b-form-select>
      </b-col>

      <b-col>
        <b-pagination
            v-model="currentPage"
            :total-rows="totalRows"
            :per-page="perPage"
            size="sm"
            align="right"
        ></b-pagination>
      </b-col>
    </b-row>

  </div>
</template>

<script>
/*
  #TODO
    1) пагинация
    2) удаление из папки ../backend/uploads
    3) загрузка сразу нескольких файлов
*/

import axios from 'axios'

export default {
  data() {
    return {
      items: [],

      fields: [
        {key: 'filename', label: 'Filename', sortable: true, sortDirection: 'desc'},
        {key: 'date', label: 'Date of download', sortable: true, class: 'text-center', formatter: "formatDateAssigned", sortDirection: 'desc'},
        {key: 'actions', label: 'Actions', class: 'text-center'}
      ],

      totalRows: 1,
      currentPage: 1,
      perPage: 5,
      pageOptions: [5, 10, 15],
      sortBy: '',
      sortDesc: false,
      sortDirection: 'asc',
      filter: null,
      filterOn: [],
      file1: null,
    }
  },

  computed: {
    sortOptions() {
      return this.fields
          .filter(f => f.sortable)
          .map(f => {
            return {text: f.label, value: f.key}
          })
    }
  },

  methods: {
    dateCompare(itemA, itemB, key) {
      if (key === 'date') {
        let a = (itemA[key] === null ? '00.00.0000' : itemA[key]).split('.');
        let b = (itemB[key] === null ? '00.00.0000' : itemB[key]).split('.');
        return parseInt(`${a[2]}${a[1]}${a[0]}`) - parseInt(`${b[2]}${b[1]}${b[0]}`);
      } else {
        return false;
      }
    },

    deleteItem(index) {
      axios.delete(`http://127.0.0.1:5000/deleteEntry/${this.items[index].id}`);
      this.items.splice(index, 1);
    },

    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length
      this.currentPage = 1
    },

    submitFile() {
      let formData = new FormData();
      formData.append('file', this.file1);
      axios.post( 'http://127.0.0.1:5000/upload',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data; charset=utf-8'
            }
          })
          .then(() => {
            this.items = [];
            this.getFiles();
          })
          .catch(() => {
          });
    },

    getFiles() {
      axios.get("http://127.0.0.1:5000//getAllFiles")
          .then(res => {
            for (let key in res.data)
                this.items.push({
                      'id' : key,
                      'filename' : res.data[key][0].replace(/^.*[\\//]/, ''),
                      'date' : res.data[key][1]
                    });
          });
    }
  },

  mounted() {
    this.totalRows = this.items.length
  },

  created() {
    this.getFiles();
    this.totalRows = this.items.length
  }
}
</script>
