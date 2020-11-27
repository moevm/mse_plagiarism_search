<template>
  <div>
    <p class="h4 mb-2">Result</p>
    <ResultTable/>
  </div>
</template>

<script>
import ResultTable from "@/components/ResultTable";

export default {
  name: "Result",
  components: {
    ResultTable
  }
}
</script>