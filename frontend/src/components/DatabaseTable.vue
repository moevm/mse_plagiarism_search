<template>
  <div class="overflow">
    <!-- File add controls -->
    <b-form-group
        label="File input:"
        label-for="file-input"
        description="file will be loaded into the database, supported formats: *.zip, *.js, *.java, *.cpp, *.c, *.py, *.h, *.hpp
              non-binary files."
        class="mb-0"
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
    <b-row>
        <b-button variant="primary" v-on:click="submitFile()" style="margin: 10px"> Upload</b-button>
        <!-- <b-button variant="danger" v-on:click="deleteAllFiles()" style="margin: 10px"> Delete All</b-button> -->
    </b-row>


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
import axios from 'axios'
import {URL} from '@/url.config'

export default {
  data() {
    return {
      items: [],

      fields: [
        {key: 'filename', label: 'Filename', sortable: true, sortDirection: 'desc'},
        {
          key: 'date',
          label: 'Date of download',
          sortable: true,
          class: 'text-center',
          formatter: "formatDateAssigned",
          sortDirection: 'desc'
        },
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
      files: [],
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
      axios.delete(`${URL + 'deleteFile/' + this.items[index].id}`);
      this.totalRows--;
      this.items.splice(index, 1);
    },

    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length
      this.currentPage = 1
    },

    async submitFile() {
      for(let i = 0; i < this.files.length; ++i) {
        let formData = new FormData();
        formData.append('file', this.files[i]);
        await axios.post(`${URL+ 'upload'}`,
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data; charset=utf-8'
              }
            }).then(() => {
              this.items = [];
          this.getFiles();

        })
      }
    },

    getFiles() {
      axios.get(`${URL + 'getAllFiles'}`)
          .then(res => {
            for (let key in res.data) {
              this.items.push({
                'id': key,
                'filename': res.data[key][0].replace(/^.*[\\/]/, ''),
                'date': res.data[key][1]
              });
              this.totalRows++;
            }
          });
    },

    deleteAllFiles() {
      axios.delete(`${URL + 'deleteAll/'}`);
      this.totalRows--;
      this.items.splice(0, this.items.length)
    }
  },

  created() {
    this.getFiles();
  }
}
</script>
