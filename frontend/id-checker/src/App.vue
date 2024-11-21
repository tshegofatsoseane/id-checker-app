<template>
  <v-app>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" sm="8">
          <SearchID />
        </v-col>
      </v-row>
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
