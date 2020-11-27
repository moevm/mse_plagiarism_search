<template>
  <div>
    <p class="h4 mb-2">Database</p>
    <DatabaseTable/>
  </div>
</template>

<script>
import DatabaseTable from "@/components/DatabaseTable";

export default {
  name: "Database",
  components: {
    DatabaseTable
  }
}
</script>