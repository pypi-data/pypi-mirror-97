
from collections import defaultdict

def score_team(score_data):

    score = score_data['upright_tokens']

    if score_data['robot_moved']:
        score += 1

    score += len(set(score_data['zones_owned']))

    slots_owned = set(score_data['slots_owned'])
    score += len(slots_owned)

    # Plus the bonus for adjacent slots:
    for s in slots_owned:
        # 3 & 4 aren't next to each other as they're on opposite sides
        before = s - 1 if s != 4 else None
        after  = s + 1 if s != 3 else None

        if before in slots_owned or after in slots_owned:
            score += 1

    return score

def tidy_slots(slot_map):
    owners = {}
    tidied = {}

    for tla, slots in slot_map.items():
        for s, val in slots.items():
            if val:
                if s in owners:
                    msg = "Slot {0} claims to be owned by at least '{1}' and '{2}'." \
                            .format(s, tla, owners[s])
                    raise Exception(msg)

                owners[s] = tla

        tidied[tla] = set()

    for slot, owner in owners.items():
        tidied[owner].add(slot)

    return tidied

def tidy_zones(zone_map):
    token_map = defaultdict(lambda: defaultdict(set))
    tidied = {}

    for tla, zones in zone_map.items():
        for z, val in zones.items():
            if val > 0:
                token_map[z][val].add(tla)

        tidied[tla] = set()

    owners = {}
    for z, claims in token_map.items():
        max_tokens = max(claims.keys())
        top_teams = claims[max_tokens]
        if len(top_teams) == 1:
            owners[z] = top_teams.pop()

    for slot, owner in owners.items():
        tidied[owner].add(slot)

    return tidied

def validate_team(tla, team_data):

    keys = ['robot_moved', 'zone_tokens', 'slot_bottoms', 'upright_tokens']
    NUM_ZONES = 4
    NUM_SLOTS = 8
    MAX_TOKENS = 8

    def check_missing(all_, actual, type_):
        missing = set(all_) - set(actual)
        if len(missing) > 0:
            missing_str = ', '.join(str(m) for m in missing)
            raise Exception("Data for '{0}' is missing {1}: {2}." \
                                .format(tla, type_, missing_str))

    check_missing(keys, team_data.keys(), 'keys')

    moved = team_data['robot_moved']
    # Proton says this defaults to true.
    # While we shouldn't need to worry about it not being there, just to be safe.
    present = team_data.get('present', True)

    if moved and not present:
        raise Exception("Data for '{0}' indicates that the robot moved but was not present!".format(tla))

    zone_tokens = team_data['zone_tokens']
    check_missing(range(NUM_ZONES), zone_tokens.keys(), 'information for zones')

    slot_bottoms = team_data['slot_bottoms']
    check_missing(range(NUM_SLOTS), slot_bottoms.keys(), 'information for slots')

    token_count = sum(1 if v else 0 for v in slot_bottoms.values())

    for z, v in zone_tokens.items():
        if v < 0:
            raise Exception("Data for '{0}' cannot a negative number ({1}) of tokens in zone {2}!".format(tla, v, z))
        token_count += v

    if token_count > MAX_TOKENS:
        raise Exception("Data for '{0}' has too many tokens ({1}, max is {2})!".format(tla, token_count, MAX_TOKENS))
