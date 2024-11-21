<template>
    <v-card class="pa-5">
      <v-card-title>SA ID Checker</v-card-title>
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
        <v-alert v-if="result" type="success" class="mt-3">
          <p><strong>Date of Birth:</strong> {{ result.date_of_birth }}</p>
          <p><strong>Gender:</strong> {{ result.gender }}</p>
          <p><strong>SA Citizen:</strong> {{ result.sa_citizen ? "Yes" : "No" }}</p>
          <p><strong>Search Count:</strong> {{ result.search_count }}</p>
          <h4>Holidays:</h4>
          <ul>
            <li v-for="holiday in result.holidays" :key="holiday.holiday_name">
              {{ holiday.holiday_name }} ({{ holiday.holiday_date }})
            </li>
          </ul>
        </v-alert>
      </v-card-text>
    </v-card>
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
          const response = await axios.post("http://127.0.0.1:8000/api/search/", {
            idNumber: this.idNumber,
          });
          this.result = response.data;
          this.error = "";
        } catch (err) {
          this.error = err.response?.data?.error || "An error occurred";
        }
      },
    },
  };
  </script>
  
 
 