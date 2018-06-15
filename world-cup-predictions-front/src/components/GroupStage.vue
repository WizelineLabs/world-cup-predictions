<template>
  <div>
    <v-container fluid grid-list-xl class="py-0 pl-0 pr-3 my-4">
      <v-layout row wrap>
        <v-flex v-for="(list, group) in teams" :key="`group-${group}`" xs12 lg6>
          <v-data-table
            :headers="headers"
            :items="list"
            hide-actions
            class="wcp-group-table elevation-0 pt-2 pb-1 px-1"
          >
            <template slot="headers" slot-scope="props">
              <tr class="border-0">
                <th class="text-xs-left title blue--text text--darken-4 wpc-group-table-cell-main">
                  {{ props.headers[0].text + ' ' + group }}
                </th>
                <th class="text-xs-center wpc-group-table-header">{{ props.headers[1].text }}</th>
                <th class="text-xs-center wpc-group-table-header">{{ props.headers[2].text }}</th>
                <th class="text-xs-center wpc-group-table-header">{{ props.headers[3].text }}</th>
              </tr>
            </template>
            <template slot="items" slot-scope="props">
              <tr class="wcp-group-table-row border-0">
                <!-- Flag and Name Cell -->
                <td class="pr-0">
                  <div
                    :class="['wcp-flag', 'flag-icon', 'flag-icon-' + props.item.flag_code]"
                  ></div>
                  <span class="wcp-group-table-title">{{ props.item.name }}</span>
                </td>
                <!-- Advance Cell -->
                <td class="wcp-group-table-cell text-xs-center border-r-1">
                  <div
                    class="wcp-group-table-cell-text"
                    :class="{
                      active: props.item.shaded,
                      'active-text': props.item.shaded,
                      'grey--text text--darken-1': !props.item.shaded
                    }"
                  >
                  {{
                    props.item.pass_group_runner_prob + props.item.pass_group_winner_prob
                    | percentage
                  }}
                  </div>
                </td>
                <!-- Advance Second Cell -->
                <td class=" wcp-group-table-cell text-xs-center">
                  <div
                    class="wcp-group-table-cell-text"
                    :class="{
                      active: props.item.second || props.item.first,
                      'active-text': props.item.second,
                      'grey--text text--darken-1': !props.item.second
                    }"
                  >
                  {{ props.item.pass_group_runner_prob | percentage }}
                  </div>
                </td>
                <!-- Advance First Cell -->
                <td class="wcp-group-table-cell text-xs-center">
                  <div
                    class="wcp-group-table-cell-text"
                    :class="{
                      active: props.item.first,
                      'active-text': props.item.first,
                      'grey--text text--darken-1': !props.item.first
                    }"
                  >
                  {{props.item.pass_group_winner_prob | percentage }}
                  </div>
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  name: 'GroupStage',
  computed: {
    teams() {
      return this.$store.getters['team/teamsByGroup'];
    },
  },
  data() {
    return {
      headers: [
        {
          text: 'Group',
          align: 'left',
          sortable: false,
          value: 'name',
        },
        {
          text: 'ADVANCE',
          align: 'center',
          sortable: false,
          value: 'advance',
        },
        {
          text: 'SECOND',
          align: 'center',
          sortable: false,
          value: 'second',
        },
        {
          text: 'FIRST',
          align: 'center',
          sortable: false,
          value: 'first',
        },
      ],
    };
  },
};
</script>

<style lang="scss">
.wcp-group-table {
  .wcp-group-table-row td {
    font-size: 16px;
  }

  .wcp-group-table-row:hover {
    background-color: transparent !important;
  }

  .wpc-group-table-cell-main {
    width: 34%;
  }

  .wpc-group-table-header {
    width: 22%;
  }

  .wcp-group-table-cell {
    padding: 0 !important;
  }

  .wcp-group-table-cell-text {
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

.wcp-group-table-title {
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
