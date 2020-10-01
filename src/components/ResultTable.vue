<template>
  <div class="overflow">
    <!-- Main table element -->
    <b-table
        show-empty
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
        @filtered="onFiltered"
    >

      <template v-slot:cell(percentBar)="row">
        <template v-if="items[row.index]['percent'] >= 80">
          <b-progress :value="items[row.index]['percent']" variant="success"/>
        </template>
        <template v-else-if="items[row.index]['percent'] >= 60">
          <b-progress :value="items[row.index]['percent']" variant="warning"/>
        </template>
        <template v-else>
          <b-progress :value="items[row.index]['percent']" variant="danger"/>
        </template>
      </template>

      <template v-slot:cell(filename)="data">
        <router-link :to="'./result/' + `${data.value}`">
          {{ data.value }}
        </router-link>
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
        {filename: 'main.cpp', percent: 95.06, lines: 258, type: 'file'},
        {filename: 'Game.cpp', percent: 68.77, lines: 300, type: 'file'},
        {filename: 'Game.hpp', percent: 35.95, lines: 160, type: 'file'},
        {filename: 'src', percent: 75.05, lines: 900, type: 'directory'},
      ],

      fields: [
        {key: 'filename', label: 'Filename', sortable: true, sortDirection: 'desc'},
        {key: 'percentBar', class: 'text-center'},
        {key: 'percent', label: '% of originality', sortable: true, class: 'text-center', sortDirection: 'desc'},
        {key: 'lines', label: 'Lines of code', sortable: true, class: 'text-center', sortDirection: 'desc'},
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

  props: {
    file: String
  },

  mounted() {
    // Set the initial number of items
    this.totalRows = this.items.length
  },
  methods: {
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length
      this.currentPage = 1
    },
    fullName(value) {
      return `${value.filename};`
    }
  }
}
</script>