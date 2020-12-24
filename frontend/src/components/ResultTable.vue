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
        <template v-else-if="items[row.index]['percent'] > 5">
          <b-progress :value="items[row.index]['percent']" variant="danger"/>
        </template>
        <template v-else>
          <b-progress :value="100" variant="danger"/>
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
      items: [],

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

  methods: {
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length
      this.currentPage = 1
    },

    fullName(value) {
      return `${value.filename};`
    },

    getFiles() {
      for (let file of this.$store.getters.RESULTS)
      {
        this.items.push({
          'filename': file[1].replace(/^.*[\\//]/, ''),
          'percent': (100 - file[0][6]).toFixed(1),
          'lines': file[0][0].length
        })
        this.totalRows++;
      }
    }
  },

  created() {
    this.getFiles();
  },
}
</script>
