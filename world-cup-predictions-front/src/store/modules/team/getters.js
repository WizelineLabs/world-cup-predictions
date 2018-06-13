const teamsByGroup = (state) => {
  const groups = {};
  const teams = [...state.list].sort((a, b) => a.id - b.id);

  // Group teams by group name
  teams.forEach((team) => {
    if (!groups[team.group]) {
      groups[team.group] = [];
    }
    groups[team.group].push(team);
  });

  // Add a property to the winner of each group
  Object.keys(groups).forEach((groupName) => {
    const group = groups[groupName];

    // eslint-disable-next-line
    const advanceTeams = group.filter((team) => team.shaded);

    // eslint-disable-next-line
    const advanceFirst = advanceTeams.reduce((max, team) => {
      return team.pass_group_winner_prob > max.pass_group_winner_prob
        ? team
        : max;
    }, advanceTeams[0]);
    advanceFirst.is_group_winner = true;
  });
  return groups;
};

const wildcards = (state) => {
  const teams = [...state.list].sort((a, b) => a.id - b.id);

  // eslint-disable-next-line
  return teams.map((team) => {
    return {
      id: team.id,
      flag_code: team.flag_code,
      name: team.name,
    };
  });
};

export default {
  teamsByGroup,
  wildcards,
};
