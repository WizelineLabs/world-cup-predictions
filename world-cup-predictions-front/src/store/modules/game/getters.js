const MATCHES_PER_GROUP_ROUND = 16;
const MATCHES_IN_GROUPS = 48;
const MATCHES_IN_ROUND_OF_16 = 8;
const MATCHES_IN_QUARTERS = 4;
const MATCHES_IN_SEMIS = 2;
const MATCHES_IN_FINALS = 2;

const matchday1 = (state) => {
  const matches = [...state.list].sort(
    (a, b) => new Date(a.date) - new Date(b.date),
  );

  const rangeStart = 0;
  const rangeEnd = MATCHES_PER_GROUP_ROUND;
  if (matches.length >= rangeEnd) {
    return matches.slice(rangeStart, rangeEnd);
  }
  return [];
};

const matchday2 = (state) => {
  const matches = [...state.list].sort(
    (a, b) => new Date(a.date) - new Date(b.date),
  );

  const rangeStart = MATCHES_PER_GROUP_ROUND;
  const rangeEnd = MATCHES_PER_GROUP_ROUND * 2;
  if (matches.length >= rangeEnd) {
    return matches.slice(rangeStart, rangeEnd);
  }
  return [];
};

const matchday3 = (state) => {
  const matches = [...state.list].sort(
    (a, b) => new Date(a.date) - new Date(b.date),
  );

  const rangeStart = MATCHES_PER_GROUP_ROUND * 2;
  const rangeEnd = MATCHES_IN_GROUPS;
  if (matches.length >= rangeEnd) {
    return matches.slice(rangeStart, rangeEnd);
  }
  return [];
};

const roundOf16 = (state) => {
  const matches = [...state.list].sort(
    (a, b) => new Date(a.date) - new Date(b.date),
  );

  const rangeStart = MATCHES_IN_GROUPS;
  const rangeEnd = rangeStart + MATCHES_IN_ROUND_OF_16;
  if (matches.length >= rangeEnd) {
    return matches.slice(rangeStart, rangeEnd);
  }
  return [];
};

const quarters = (state) => {
  const matches = [...state.list].sort(
    (a, b) => new Date(a.date) - new Date(b.date),
  );

  const rangeStart = MATCHES_IN_GROUPS + MATCHES_IN_ROUND_OF_16;
  const rangeEnd = rangeStart + MATCHES_IN_QUARTERS;
  if (matches.length >= rangeEnd) {
    return matches.slice(rangeStart, rangeEnd);
  }
  return [];
};

const semis = (state) => {
  const matches = [...state.list].sort(
    (a, b) => new Date(a.date) - new Date(b.date),
  );

  const rangeStart =
    MATCHES_IN_GROUPS + MATCHES_IN_ROUND_OF_16 + MATCHES_IN_QUARTERS;
  const rangeEnd = rangeStart + MATCHES_IN_SEMIS;
  if (matches.length >= rangeEnd) {
    return matches.slice(rangeStart, rangeEnd);
  }
  return [];
};

const final = (state) => {
  const matches = [...state.list].sort(
    (a, b) => new Date(a.date) - new Date(b.date),
  );

  const rangeStart =
    MATCHES_IN_GROUPS +
    MATCHES_IN_ROUND_OF_16 +
    MATCHES_IN_QUARTERS +
    MATCHES_IN_SEMIS;
  const rangeEnd = rangeStart + MATCHES_IN_FINALS;
  if (matches.length >= rangeEnd) {
    return matches.slice(rangeStart, rangeEnd);
  }
  return [];
};

const wildcardDate = (state) => {
  const matches = [...state.list].sort(
    (a, b) => new Date(a.date) - new Date(b.date),
  );

  // The deadline for the submit the wildcard is the 1st match of the 2nd round
  return matches.length >= 16 ? matches[16].date : null;
};

export default {
  matchday1,
  matchday2,
  matchday3,
  roundOf16,
  quarters,
  semis,
  final,
  wildcardDate,
};
