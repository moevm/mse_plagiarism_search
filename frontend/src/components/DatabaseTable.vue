<template>
  <div class="overflow">
    <!-- File add controls -->
    <b-form-file class="mb-2"
                 v-model="file1"
                 :state="Boolean(file1)"
                 placeholder="Choose a file or drop it here..."
                 drop-placeholder="Drop file here..."
    ></b-form-file>

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
export default {
  data() {
    return {
      items: [
        {lines: 40, filename: 'my_database.sql', date: "02.03.04"},
        {lines: 41, filename: 'my_database2.sql', date: "03.03.04"},
        {lines: 42, filename: 'my_database3.sql', date: "04.03.14"},
        {lines: 43, filename: 'my_database4.sql', date: "05.03.05"},
        {lines: 44, filename: 'my_database5.sql', date: "06.03.15"},
        {lines: 40, filename: 'my_database.sql', date: "02.03.04"},
        {lines: 41, filename: 'my_database2.sql', date: "03.03.04"},
        {lines: 42, filename: 'my_database3.sql', date: "04.03.14"},
        {lines: 43, filename: 'my_database4.sql', date: "05.03.05"},
        {lines: 44, filename: 'my_database5.sql', date: "06.03.15"},
        {lines: 40, filename: 'my_database.sql', date: "02.03.04"},
        {lines: 41, filename: 'my_database2.sql', date: "03.03.04"},
        {lines: 42, filename: 'my_database3.sql', date: "04.03.14"},
        {lines: 43, filename: 'my_database4.sql', date: "05.03.05"},
        {lines: 44, filename: 'my_database5.sql', date: "06.03.15"},
      ],

      fields: [
        {key: 'filename', label: 'Filename', sortable: true, sortDirection: 'desc'},
        {key: 'lines', label: 'Lines of code', sortable: true, class: 'text-center'},
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
      file1: null,
      file2: null,
    }
  },

  computed: {
    sortOptions() {
      // Create an options list from our fields
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
      this.items.splice(index, 1);
    },

    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length
      this.currentPage = 1
    }
  },

  mounted() {
    // Set the initial number of items
    this.totalRows = this.items.length
  },

}
</script>