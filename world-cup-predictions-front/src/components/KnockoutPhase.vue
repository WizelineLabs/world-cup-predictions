<template>
  <v-container fluid grid-list-xl class="py-0 pl-0 pr-3 my-4">
    <v-layout row wrap>
      <v-flex xs12>
        <v-data-table
          :headers="headers"
          :items="teams"
          hide-actions
          flat
          class="wcp-table pt-2 pb-1 px-1"
        >
          <template slot="headers" slot-scope="props">
            <tr class="border-0">
              <th class="text-xs-left blue--text text--darken-4 wpc-table-cell-main">
                <span class="wcp-subtext">{{ props.headers[0].text }}</span>
              </th>
              <th class="text-xs-center wpc-table-header">{{ props.headers[1].text }}</th>
              <th class="text-xs-center wpc-table-header">{{ props.headers[2].text }}</th>
              <th class="text-xs-center wpc-table-header">{{ props.headers[3].text }}</th>
              <th class="text-xs-center wpc-table-header">{{ props.headers[4].text }}</th>
              <th class="text-xs-center wpc-table-header">{{ props.headers[5].text }}</th>
            </tr>
          </template>
          <template slot="items" slot-scope="props">
            <tr class="wcp-table-row border-0">
              <!-- Flag and Name Cell -->
              <td class="pr-0">
                <div
                  :class="['wcp-flag', 'flag-icon', 'flag-icon-' + props.item.flag_code]"
                ></div>
                <span class="wcp-table-title">{{ props.item.name }}</span>
              </td>
              <!-- Sixteen Cell -->
              <td class="pa-0 text-xs-center border-r-1">
                <div
                  class="wcp-table-cell-text"
                  :style="{
                    'background-color': `rgba(76, 175, 80, ${props.item.advance})`
                  }"
                >
                  {{props.item.advance | percentage}}
                </div>
              </td>
              <!-- Quarter Cell -->
              <td class="pa-0 text-xs-center border-r-1">
                <div
                  class="wcp-table-cell-text"
                  :style="{
                    'background-color': `rgba(76, 175, 80, ${props.item.pass_round16_prob})`
                  }"
                >
                  {{props.item.pass_round16_prob | percentage}}
                </div>
              </td>
              <!-- Semis Cell -->
              <td class=" pa-0 text-xs-center border-r-1">
                <div
                  class="wcp-table-cell-text"
                  :style="{
                    'background-color': `rgba(76, 175, 80, ${props.item.pass_quarters_prob})`
                  }"
                >
                  {{ props.item.pass_quarters_prob | percentage }}
                </div>
              </td>
              <!-- Final Cell -->
              <td class="pa-0 text-xs-center border-r-1">
                <div
                  class="wcp-table-cell-text"
                  :style="{
                    'background-color': `rgba(76, 175, 80, ${props.item.pass_semi_prob})`
                  }"
                >
                  {{props.item.pass_semi_prob | percentage }}
                </div>
              </td>
              <!-- Winner Cell -->
              <td class="pa-0 text-xs-center">
                <div
                  class="wcp-table-cell-text"
                  :style="{
                    'background-color': `rgba(76, 175, 80, ${props.item.pass_final_prob})`
                  }"
                >
                  {{props.item.pass_final_prob | percentage }}
                </div>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'KnockoutPhase',
  computed: {
    teams() {
      return this.$store.getters['team/teamsByWinnerProb'];
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
          align: 'center',
          sortable: false,
          value: 'sixteen',
        },
        {
          text: 'QUARTERS',
          align: 'center',
          sortable: false,
          value: 'quarters',
        },
        {
          text: 'SEMIS',
          align: 'center',
          sortable: false,
          value: 'semi',
        },
        {
          text: 'FINAL',
          align: 'center',
          sortable: false,
          value: 'final',
        },
        {
          text: 'WINNER',
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
</style>
