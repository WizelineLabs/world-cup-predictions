<template>
  <v-container fluid grid-list-xl class="py-0 pl-0 pr-3 my-4">
    <v-flex xs12>
      <div class="text-xs-left blue--text text--darken-4 wcp-bold hidden-md-and-up">
        <span class="wcp-subtext pl-3">{{ this.headers[0].text }}</span>
      </div>
      <v-table fixed-header flat class="wcp-table pt-2 pb-1 px-1">
        <thead>
          <tr class="border-0 hidden-sm-and-down">
            <th class="text-xs-left blue--text text--darken-4 wpc-table-cell-main">
              <span class="wcp-subtext">{{ headers[0].text }}</span>
            </th>
            <th class="text-xs-center wpc-table-header">{{ headers[1].text }}</th>
            <th class="text-xs-center wpc-table-header">{{ headers[2].text }}</th>
            <th class="text-xs-center wpc-table-header">{{ headers[3].text }}</th>
            <th class="text-xs-center wpc-table-header">{{ headers[4].text }}</th>
            <th class="text-xs-center wpc-table-header">{{ headers[5].text }}</th>
          </tr>
          <tr class="border-0 hidden-md-and-up">
            <th class="text-xs-left blue--text text--darken-4 wpc-table-cell-main"></th>
            <th class="text-xs-center wpc-table-header">{{ headers[1].subtext }}</th>
            <th class="text-xs-center wpc-table-header">{{ headers[2].subtext }}</th>
            <th class="text-xs-center wpc-table-header">{{ headers[3].subtext }}</th>
            <th class="text-xs-center wpc-table-header">{{ headers[4].subtext }}</th>
            <th class="text-xs-center wpc-table-header">{{ headers[5].subtext }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in teams" :key="item.name" class="wcp-table-row border-0">
            <!-- Flag and Name Cell -->
            <td class="pr-0">
              <div :class="['wcp-flag', 'mr-1', 'fi', 'fi-' + item.flag_code]"></div>
              <span class="wcp-table-title hidden-sm-and-down">{{ item.name }}</span>
            </td>
            <!-- Sixteen Cell -->
            <td class="pa-0 text-xs-center border-r-1">
              <div class="wcp-table-cell-text" :style="{
                'background-color': `rgba(76, 175, 80, ${item.advance})`
              }">
                {{ $filters.percentage(item.advance) }}
              </div>
            </td>
            <!-- Quarter Cell -->
            <td class="pa-0 text-xs-center border-r-1">
              <div class="wcp-table-cell-text" :style="{
                'background-color': `rgba(76, 175, 80, ${item.pass_round16_prob})`
              }">
                {{ $filters.percentage(item.pass_round16_prob) }}
              </div>
            </td>
            <!-- Semis Cell -->
            <td class=" pa-0 text-xs-center border-r-1">
              <div class="wcp-table-cell-text" :style="{
                'background-color': `rgba(76, 175, 80, ${item.pass_quarters_prob})`
              }">
                {{ $filters.percentage(item.pass_quarters_prob) }}
              </div>
            </td>
            <!-- Final Cell -->
            <td class="pa-0 text-xs-center border-r-1">
              <div class="wcp-table-cell-text" :style="{
                'background-color': `rgba(76, 175, 80, ${item.pass_semi_prob})`
              }">
                {{ $filters.percentage(item.pass_semi_prob) }}
              </div>
            </td>
            <!-- Winner Cell -->
            <td class="pa-0 text-xs-center">
              <div class="wcp-table-cell-text" :style="{
                'background-color': `rgba(76, 175, 80, ${item.pass_final_prob})`
              }">
                {{ $filters.percentage(item.pass_final_prob) }}
              </div>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-flex>
  </v-container>
</template>

<script>
export default {
  name: 'KnockoutPhase',
  computed: {
    teams() {
      return this.$store.getters['teamsByWinnerProb'];
    },
  },
  data() {
    return {
      headers: [
        {
          text: 'Chances of reaching round:',
          align: 'left',
          sortable: false,
          value: 'name',
        },
        {
          text: 'ROUND OF 16',
          subtext: 'R16',
          align: 'center',
          sortable: false,
          value: 'sixteen',
        },
        {
          text: 'QUARTERS',
          subtext: 'QUA',
          align: 'center',
          sortable: false,
          value: 'quarters',
        },
        {
          text: 'SEMIS',
          subtext: 'SEM',
          align: 'center',
          sortable: false,
          value: 'semi',
        },
        {
          text: 'FINAL',
          subtext: 'FIN',
          align: 'center',
          sortable: false,
          value: 'final',
        },
        {
          text: 'WINNER',
          subtext: 'WIN',
          align: 'center',
          sortable: false,
          value: 'winner',
        },
      ],
    };
  },
};
</script>

<style lang="scss">
.wcp-table {
  .wcp-table-row td {
    font-size: 16px;
  }

  .wcp-table-row:hover {
    background-color: transparent !important;
  }

  .wpc-table-cell-main {
    width: 35%;
  }

  .wpc-table-header {
    width: 13%;
  }

  .wcp-table-cell-text {
    padding-top: 2px;
  }

  .border-0 {
    border: 0 !important;
  }

  .border-r-1 {
    border-right: 1px dashed #d7dbdf;
  }

  .active {
    background-color: #e7ebf3;
  }

  .active-text {
    color: rgba(0, 0, 0, 0.87);
    font-family: 'ProximaNova-Semibold', 'Roboto', sans-serif;
    font-weight: 500;
  }
}

.wcp-table-title {
  display: inline-block;
  padding: 5px 10px;
}

.wcp-flag {
  background-color: #adb6c0;
  border-radius: 2px;
  display: inline-block;
  height: 24px;
  line-height: 24px;
  margin: 0 0 -6px 0;
  width: 32px;
}

// Responsiveness
.xs,
.sm {
  .wpc-table-cell-main {
    width: 25%;
  }

  .wpc-table-header {
    width: 15%;
  }

  .wcp-table thead th:first-child,
  .wcp-table tbody td:first-child,
  .wcp-table thead th:not(:first-child) {
    padding: 0 4px;
  }
}
</style>
