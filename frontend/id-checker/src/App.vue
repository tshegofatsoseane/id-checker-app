<template>
  <v-app>
    <v-container class="pa-0">
      <v-img
        :src="require('@/assets/background.jpg')"
        class="background-image"
        cover
        height="100vh"
      >
        <!-- centre SearchID component on top of the bg image -->
        <v-row justify="center" align="center" class="fill-height">
          <v-col cols="12" sm="8" class="search-id-col">
            <SearchID />
          </v-col>
        </v-row>
      </v-img>
    </v-container>
  </v-app>
</template>

<script>
import SearchID from "@/components/SearchID.vue";

export default {
  name: "App",
  components: {
    SearchID,
  },
};
</script>

<style scoped>
.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.search-id-col {
  position: relative;
  z-index: 2; 
}

.pa-0 {
  padding: 0;
}

.fill-height {
  height: 100%;
}
</style>
