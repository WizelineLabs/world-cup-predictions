<template>
  <label class="wildcard mb-4" :class="[`${matchState}`]">
    <input
      :id="`wildcard-${team.id}`"
      type="radio"
      name="wildcards"
      :value="team.id"
      :checked="team.id === currentWildcard"
      @click="handleWildcardSelected"
      :disabled="matchState !== 'open'"
    />
    <div class="wildcard-container">
      <div class="wildcard-team-container text-xs-center">
        <div
          class="wildcard-flag flag-icon"
          :class="[`flag-icon-${team.flag_code}`]"
        ></div>
        <span class="wildcard-team-name d-block mt-2 text-xs-center">
          {{team.name}}
        </span>
      </div>
    </div>
    <div class="match-card-save-status"
      :class="{
        show: showSaveStatus,
        'status-error': errorSaving
      }">
      {{saveStatus}}
    </div>
  </label>
</template>

<script>
export default {
  name: 'Wildcard',
  props: ['team', 'matchState'],
  data() {
    return {
      wildcardSelected: '',
      saveStatus: '',
      showSaveStatus: false,
      errorSaving: false,
    };
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
    currentWildcard() {
      return this.wildcardSelected || this.user.data.winner_choice;
    },
  },
  methods: {
    handleWildcardSelected(event) {
      const value = parseInt(event.target.value, 10);
      this.wildcardSelected = this.currentWildcard === value ? '' : value;

      if (this.wildcardSelected) {
        this.$store
          .dispatch('setWildcard', {
            wildcardId: this.wildcardSelected,
          })
          .then(() => {
            this.$store.dispatch('getUser');
            this.saveStatus = 'Wildcard Saved!';
            this.showStatus();
          })
          .catch(() => {
            this.saveStatus = "We couldn't save your wildcard";
            this.showStatus(true);
          });
      }
    },
    showStatus(hasError) {
      const self = this;
      self.showSaveStatus = true;
      self.errorSaving = hasError;
      setTimeout(() => {
        self.showSaveStatus = false;
        self.errorSaving = false;
      }, 3000);
    },
  },
};
</script>

<style lang="scss">
.wildcard {
  display: block;
  position: relative;
  user-select: none;

  > input {
    cursor: pointer;
    height: 100%;
    position: absolute;
    visibility: hidden;
    width: 100%;
  }

  > input:checked ~ .wildcard-container,
  &:hover > input:checked ~ .wildcard-container {
    background-color: rgba(21, 101, 192, 0.3);
    border-color: transparent;
    opacity: 1;
  }

  &:hover .wildcard-container {
    background-color: rgba(231, 235, 243, 0.5);
    border: solid 1px #1565c0;
  }

  &.locked > input,
  &.locked .wildcard-container,
  &.locked:hover .wildcard-container {
    background-color: #f1f3f7;
    border-color: #adb6c0;
    cursor: default;
    opacity: 0.7;
  }
}

.wildcard-container {
  align-items: center;
  border-radius: 8px;
  border: solid 1px #adb6c0;
  cursor: pointer;
  display: flex;
  justify-content: center;
  min-height: 138px;
  padding: 8px;
}

.wildcard-team-container {
  width: 100%;
}

.wildcard-flag {
  background-color: #adb6c0;
  border-radius: 2px;
  height: 42px;
  line-height: 42px;
  margin: 0;
  pointer-events: none;
  width: 56px;
}

.wildcard-team-name {
  font-size: 16px;
  line-height: 1.5;
}

.wildcard-save-status {
  color: #1565c0;
  font-family: 'ProximaNova-Semibold', 'Roboto', sans-serif;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  letter-spacing: 0.3px;
  opacity: 0;
  position: absolute;
  text-align: center;
  transition: all 0.3s ease-out;
  top: 99%;
  width: 100%;

  &.status-error {
    color: #d32f2f;
  }

  &.show {
    opacity: 1;
    top: 102%;
  }
}
</style>
