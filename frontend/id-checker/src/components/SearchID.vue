<template>
  <v-container class="pa-5">
    <v-card class="pa-5">
      <v-card-title class="text-h5 font-weight-bold">SA ID Checker</v-card-title>
      <v-card-text>
        <v-text-field
          label="Enter South African ID Number"
          v-model="idNumber"
          outlined
          :rules="[validateID]"
          @input="error = ''"
        />
        <v-btn :disabled="!isValidID" color="primary" @click="searchID">
          Search
        </v-btn>
        <v-alert v-if="error" type="error" class="mt-3">{{ error }}</v-alert>
        <v-card v-if="result" outlined class="mt-5">
            <v-card-title class="font-weight-bold text-h6">Search Results</v-card-title>
            <v-card-text>
        <v-row>
      <v-col cols="12" sm="6">
        <p><strong>Date of Birth:</strong> {{ result.date_of_birth }}</p>
        <p><strong>Gender:</strong> {{ result.gender }}</p>
      </v-col>
      <v-col cols="12" sm="6">
        <p><strong>SA Citizen:</strong> {{ result.saCitizen ? "Yes" : "No" }}</p>
        <p><strong>Search Count:</strong> {{ result.searchCount }}</p>
      </v-col>
    </v-row>
    <v-divider class="my-4"></v-divider> 
    <h4 class="text-h6 font-weight-bold">Holidays:</h4>
    <v-list dense>
      <v-list-item
        v-for="holiday in result.holidays"
        :key="holiday.holiday_name"
      >
        <v-list-item-content>
          <v-list-item-title>
            <strong>{{ holiday.holiday_name }}</strong>
          </v-list-item-title>
          <v-list-item-subtitle>
            <strong>Date:</strong> {{ holiday.holiday_date }}
          </v-list-item-subtitle>
          <v-list-item-subtitle>
            <strong>Type:</strong> {{ holiday.holiday_type }}
          </v-list-item-subtitle>
          <v-list-item-subtitle class="holiday-description">
            <strong>Description:</strong> {{ holiday.description }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card-text>
</v-card>

      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      idNumber: "",
      result: null,
      error: "",
    };
  },
  computed: {
    isValidID() {
      return this.validateID(this.idNumber) === true;
    },
  },
  methods: {
    validateID(id) {
      if (id.length !== 13 || !/^\d+$/.test(id)) return "ID must be 13 digits";
      let sum = 0;
      for (let i = 0; i < 13; i++) {
        let num = parseInt(id[i]);
        if (i % 2 !== 0) {
          num *= 2;
          if (num > 9) num -= 9;
        }
        sum += num;
      }
      return sum % 10 === 0 || "Invalid ID number";
    },
    async searchID() {
  try {
    const response = await axios.post("http://127.0.0.1:8000/api/search", {
      idNumber: this.idNumber,
    });
    console.log(response.data);
    this.result = response.data;
    this.error = "";
  } catch (err) {
    this.error = err.response?.data?.error || "An error occurred";
  }
},
  },
};
</script>

<style scoped>
.v-list-item-title {
  font-weight: bold;
}
.v-list-item-subtitle {
  font-style: italic;
}

</style>
