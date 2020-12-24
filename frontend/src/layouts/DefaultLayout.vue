<template>
  <div>
    <div class="header-default">
      <b-navbar toggleable type="dark" variant="dark" style="height: 80px">
        <b-navbar-toggle style="border: none" target="sidebar-backdrop"></b-navbar-toggle>
        <b-navbar-brand href="/search">Source Code Similarity Detection</b-navbar-brand>
      </b-navbar>

      <b-sidebar id="sidebar-backdrop" backdrop width="auto" style="background-color: aliceblue">
        <div class="px-3 py-2">
          <nav class="mb-3">
            <b-nav vertical>
              <b-nav-item href="/search">
                <p class="h6 mb-2">
                  <b-icon icon="search"></b-icon>
                  Plagiarism search
                </p>
              </b-nav-item>
              <b-nav-item href="/database">
                <p class="h6 mb-2">
                  <b-icon icon="server"></b-icon>
                  Database
                </p>
              </b-nav-item>
              <b-nav-item href="/history">
                <p class="h6 mb-2">
                  <b-icon icon="clock-history"></b-icon>
                  History
                </p>
             </b-nav-item>
              <!-- <b-nav-item href="/about">
                <p class="h6 mb-2">
                  <b-icon icon="info-square"></b-icon>
                  About
                </p>
              </b-nav-item>-->
            </b-nav>
          </nav>
        </div>
      </b-sidebar>
    </div>

    <div class="mx-auto" style="background-color: #D8D8D8">
      <div class="SS mx-auto" style="width: 1000px; padding: 75px; height: auto; background-color: #ffffff">
        <router-view/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DefaultLayout"
}
</script>
