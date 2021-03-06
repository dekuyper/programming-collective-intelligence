# -*- coding: utf-8 -*-
from math import sqrt
# A dictionary of movie critics and their ratings of a small set of movies
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0,
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5,
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0,
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5,
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0,
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
    },
    'Toby': {
        'Snakes on a Plane': 4.5,
        'You, Me and Dupree': 1.0,
        'Superman Returns': 4.0
    },
    'Nicu': {
        'Superman Returns': 4.0,
        'You, Me and Dupree': 3.5
    }
}


def simDistance(prefs, person1, person2):
    shared_items = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            shared_items[item] = 1

    if len(shared_items) == 0:
        return 0
    sum_of_squares = sum(
        [pow(prefs[person1][item] - prefs[person2][item], 2) for item in shared_items])
    return 1 / (1 + sqrt(sum_of_squares))


def simPearson(prefs, person1, person2):
    # Get the list of mutually rated items
    shared_items = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            shared_items[item] = 1

    # Find the number of elements
    n = len(shared_items)

    if n == 0:
        return 0

    # Add up all the preferences
    sum1 = sum([prefs[person1][item] for item in shared_items])
    sum2 = sum([prefs[person2][item] for item in shared_items])

    # Sum up the squares
    sum1Sq = sum([pow(prefs[person1][item], 2) for item in shared_items])
    sum2Sq = sum([pow(prefs[person2][item], 2) for item in shared_items])

    # Sum up the products
    pSum = sum([prefs[person1][item] * prefs[person2][item]
                for item in shared_items])

    # Calculate Pearson score
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))

    # Protection against division by 0 errors
    if den == 0:
        return 0

    result = num / den

    return result


def topMatches(prefs, person, n=5, similarity=simPearson):
    """
    Returns the best matches for person from the prefs dictionary
    Number of results and similarity function are optional parameters
    """
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]

    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]


def getRecommendations(prefs, person, similarity=simPearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # don't compare me to myself
        if other == person:
            continue

        sim = similarity(prefs, person, other)

        # ignore scores of 0 or lower
        if sim <= 0:
            continue

        for item in prefs[other]:
            # only scores movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

        # Create the normalized list
        rankings = [(total / simSums[item], item)
                    for item, total in totals.items()]

        # Return the sorted list
        rankings.sort()
        rankings.reverse()

        return rankings
