<template>
<v-container class="mb-5">
    <v-layout row wrap justify-center class="mb-4">
      <v-flex xs10>
        <h1 class="display-1 mt-5 mb-4 text--darken-2 grey--text">
          Prediction Game
        </h1>
        <p class="wcp-text my-4">
          As part of an internal initiative, we created a prediction system that estimates
          the probabilities of each team making it through each of the rounds and ultimately
          winning the World Cup.
          <br /><br />
          You can keep track of you favorite team's chances making it through the groups
          stage and the knockout phase in the
          <router-link to="/prediction">prediction tool page</router-link>.
          <br /><br />
          To make things more fun and interesting, the Team decided to create a Prediction
          Game, commonly known as football pools or "quinielas", where you can place your
          votes on which teams you think will win or draw. Besides that, there is a
          leaderboard where you can keep track of which Wizeliners have been making the
          best predictions.
        </p>
        <h3 class="headline pt-3">
          Earning Points
        </h3>
        <p class="wcp-text my-4">
          For each right guess, you’ll be granted 10 points. You will also have one extra
          shot to guess the ultimate winner of the cup. This is a wildcard and voting
          is open until the start of round 2 in the groups stage. If you guess right,
          you’ll get 30 extra points!
        </p>
        <h3 class="headline pt-3">
          Beat Paul
        </h3>
        <p class="wcp-text my-4">
          Our prediction tool will also be participating in the game with the alias "Paul".
          Paul's prediction for the matchup will be visible once your vote is locked and the
          match is in progress.
        </p>
        <h3 class="headline pt-3">
          Joining the Game
        </h3>
        <p class="wcp-text my-4">
          Participation is open to Wizeliners across all offices and Wizeline Teams, just sign
          in with your Wizeline and Wizeline Teams account to join the game and place your
          votes!
        </p>
      </v-flex>
    </v-layout>
  </v-container>
</template>
