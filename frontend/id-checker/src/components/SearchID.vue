<template>
  <v-container class="pa-5 page-container">
    <v-card class="pa-5 frosted-card">
      <v-card-title class="text-h5 font-weight-bold">SA ID Checker</v-card-title>

      <v-card-text>
        <p class="description-text">
          Enter a South African ID Number to check if there are any important public holidays on the date of birth.
        </p>
      </v-card-text>

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

        <!-- search results card -->
        <v-card v-if="result" outlined class="mt-5 frosted-card">
          <v-card-title class="font-weight-bold text-h6">Search Results</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6">
                <p><strong>Date of Birth:</strong> {{ result.dateOfBirth }}</p>
                <p><strong>Gender:</strong> {{ result.gender }}</p>
              </v-col>
              <v-col cols="12" sm="6">
                <p><strong>SA Citizen:</strong> {{ result.saCitizen ? "Yes" : "No" }}</p>
                <p><strong>Search Count:</strong> {{ result.searchCount }}</p>
              </v-col>
            </v-row>
            <v-divider class="my-4"></v-divider>
            <h4 class="text-h6 font-weight-bold">Holidays:</h4>

            <div class="holiday-list-container" @scroll="onScroll">
              <template v-if="result.holidays.length > 0">
                <!-- holiday list -->
                <v-row>
                  <v-col
                    v-for="(holiday, index) in visibleHolidays"
                    :key="index"
                    cols="12"
                  >
                    <v-card class="holiday-card">
                      <v-card-title>
                        <v-icon color="blue lighten-2" class="mr-3">mdi-calendar</v-icon>
                        <strong>{{ holiday.holiday_name }}</strong>
                      </v-card-title>
                      <v-card-subtitle class="holiday-details">
                        <p>
                          <v-icon color="primary" small>mdi-calendar-range</v-icon>
                          <strong>Date:</strong> {{ holiday.holiday_date }}
                        </p>
                        <p>
                          <v-icon color="green lighten-2" small>mdi-tag</v-icon>
                          <strong>Type:</strong> {{ holiday.holiday_type }}
                        </p>
                        <p>
                          <v-icon color="orange lighten-2" small>mdi-information</v-icon>
                          <strong>Description:</strong> {{ holiday.description }}
                        </p>
                      </v-card-subtitle>
                    </v-card>
                  </v-col>
                </v-row>
              </template>

              <!-- error message if holiday isnt found-->
              <template v-else>
                <v-alert type="info" class="mt-3" dense outlined>
                  No holidays found for this date of birth.
                </v-alert>
              </template>
            </div>
          </v-card-text>
        </v-card>
      </v-card-text>
    </v-card>
    <br />
    <br />
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
      visibleCount: 5,
    };
  },
  computed: {
    isValidID() {
      return this.validateID(this.idNumber) === true;
    },
    visibleHolidays() {
      return this.result ? this.result.holidays.slice(0, this.visibleCount) : [];
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
    onScroll(event) {
      const bottom = event.target.scrollHeight === event.target.scrollTop + event.target.clientHeight;
      if (bottom && this.result.holidays.length > this.visibleCount) {
        this.visibleCount += 5;
      }
    },
  },
};
</script>

<style scoped>
.holiday-list-container {
  max-height: 400px;
  overflow-y: scroll;
  padding-right: 10px;
}

.page-container {
  max-height: 100vh;
  overflow-y: scroll;
}

.frosted-card {
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.holiday-card {
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(6px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  margin-bottom: 10px;
  height: 200px;
}

.holiday-card .v-card-title {
  font-weight: bold;
  font-size: 1.2rem;
  color: #333;
}

.holiday-details p {
  margin: 5px 0;
  font-size: 0.9rem;
  color: #555;
  display: flex;
  align-items: center;
}
</style>
