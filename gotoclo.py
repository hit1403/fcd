import copy

def grammarAugmentation(rules, nonterm_userdef, start_symbol):
    newRules = []
    newChar = start_symbol + "'"
    while newChar in nonterm_userdef:
        newChar += "'"

    newRules.append([newChar, ['.', start_symbol]])

    for rule in rules:
        k = rule.split("->")
        lhs = k[0].strip()
        rhs = k[1].strip()
        multirhs = rhs.split('|')

        for rhs1 in multirhs:
            rhs1 = rhs1.strip().split()
            rhs1.insert(0, '.')
            newRules.append([lhs, rhs1])
    return newRules

def findClosure(input_state, dotSymbol):
    global start_symbol, separatedRulesList, statesDict

    closureSet = []

    if dotSymbol == start_symbol:
        for rule in separatedRulesList:
            if rule[0] == dotSymbol:
                closureSet.append(rule)
    else:
        closureSet = input_state

    prevLen = -1

    while prevLen != len(closureSet):
        prevLen = len(closureSet)

        tempClosureSet = []

        for rule in closureSet:
            indexOfDot = rule[1].index('.')
            if rule[1][-1] != '.':
                dotPointsHere = rule[1][indexOfDot + 1]
                for in_rule in separatedRulesList:
                    if dotPointsHere == in_rule[0] and in_rule not in tempClosureSet:
                        tempClosureSet.append(in_rule)

        for rule in tempClosureSet:
            if rule not in closureSet:
                closureSet.append(rule)
    return closureSet

def compute_GOTO(state):
    global statesDict, stateCount

    generateStatesFor = []
    for rule in statesDict[state]:
        if rule[1][-1] != '.':
            indexOfDot = rule[1].index('.')
            dotPointsHere = rule[1][indexOfDot + 1]
            if dotPointsHere not in generateStatesFor:
                generateStatesFor.append(dotPointsHere)

    if generateStatesFor:
        for symbol in generateStatesFor:
            GOTO(state, symbol)
    return

def GOTO(state, charNextToDot):
    global statesDict, stateCount, stateMap

    newState = []
    for rule in statesDict[state]:
        indexOfDot = rule[1].index('.')
        if rule[1][-1] != '.':
            if rule[1][indexOfDot + 1] == charNextToDot:
                shiftedRule = copy.deepcopy(rule)
                shiftedRule[1][indexOfDot] = shiftedRule[1][indexOfDot + 1]
                shiftedRule[1][indexOfDot + 1] = '.'
                newState.append(shiftedRule)

    addClosureRules = []
    for rule in newState:
        indexDot = rule[1].index('.')

        if rule[1][-1] != '.':
            closureRes = findClosure(newState, rule[1][indexDot + 1])
            for rule in closureRes:
                if rule not in addClosureRules and rule not in newState:
                    addClosureRules.append(rule)

    for rule in addClosureRules:
        newState.append(rule)

    stateExists = -1
    for state_num in statesDict:
        if statesDict[state_num] == newState:
            stateExists = state_num
            break

    if stateExists == -1:
        stateCount += 1
        statesDict[stateCount] = newState
        stateMap[(state, charNextToDot)] = stateCount
    else:
        stateMap[(state, charNextToDot)] = stateExists
    return

def generateStates(statesDict):
    prev_len = -1
    called_GOTO_on = []

    while len(statesDict) != prev_len:
        prev_len = len(statesDict)
        keys = list(statesDict.keys())

        for key in keys:
            if key not in called_GOTO_on:
                called_GOTO_on.append(key)
                compute_GOTO(key)
    return

def first(rule):
    global rules, nonterm_userdef, term_userdef, diction, firsts

    if rule and rule[0] in term_userdef:
        return rule[0]
    elif rule and rule[0] == '#':
        return '#'

    if rule:
        if rule[0] in diction:
            fres = []
            rhs_rules = diction[rule[0]]

            for itr in rhs_rules:
                indivRes = first(itr)
                if isinstance(indivRes, list):
                    fres.extend(indivRes)
                else:
                    fres.append(indivRes)

            if '#' not in fres:
                return fres
            else:
                fres.remove('#')
                if len(rule) > 1:
                    ansNew = first(rule[1:])
                    if ansNew is not None:
                        if isinstance(ansNew, list):
                            fres.extend(ansNew)
                        else:
                            fres.append(ansNew)
                    else:
                        fres
                fres.append('#')
                return fres

def follow(nt):
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows

    solset = set()
    if nt == start_symbol:
        solset.add('$')

    for curNT in diction:
        rhs = diction[curNT]

        for subrule in rhs:
            if nt in subrule:
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]

                    if subrule:
                        res = first(subrule)
                        if '#' in res:
                            res.remove('#')
                            ansNew = follow(curNT)
                            if ansNew is not None:
                                if isinstance(ansNew, list):
                                    res.extend(ansNew)
                                else:
                                    res.append(ansNew)
                            res
                    else:
                        if nt != curNT:
                            res = follow(curNT)

                    if res is not None:
                        if isinstance(res, list):
                            solset.update(res)
                        else:
                            solset.add(res)
    return list(solset)

def createParseTable(statesDict, stateMap, T, NT):
    global separatedRulesList, diction

    rows = list(statesDict.keys())
    cols = T + ['$'] + NT

    Table = []
    for _ in range(len(rows)):
        Table.append([''] * len(cols))

    for entry in stateMap:
        state = entry[0]
        symbol = entry[1]

        row_index = rows.index(state)
        col_index = cols.index(symbol)
        if symbol in NT:
            Table[row_index][col_index] += str(stateMap[entry]) + ' '
        elif symbol in T:
            Table[row_index][col_index] += 'S' + str(stateMap[entry]) + ' '

    numbered = {}
    key_count = 0
    for rule in separatedRulesList:
        tempRule = copy.deepcopy(rule)
        tempRule[1].remove('.')
        numbered[key_count] = tempRule
        key_count += 1

    addedR = separatedRulesList[0][0] + " -> " + separatedRulesList[0][1][1]
    rules.insert(0, addedR)
    for rule in rules:
        k = rule.split("->")
        lhs = k[0].strip()
        rhs = k[1].strip()
        multirhs = rhs.split('|')

        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip().split()
        diction[lhs] = multirhs

    for stateno in statesDict:
        for rule in statesDict[stateno]:
            if rule[1][-1] == '.':
                temp2 = copy.deepcopy(rule)
                temp2[1].remove('.')
                for key in numbered:
                    if numbered[key] == temp2:
                        follow_result = follow(rule[0])
                        for col in follow_result:
                            col_index = cols.index(col)
                            if key == 0:
                                Table[stateno][col_index] = "Accept"
                            else:
                                Table[stateno][col_index] += 'R' + str(key) + ' '

    print("\nSLR(1) parsing table:")
    print(" ", end=" ")
    print(" ".join(cols))

    for index, row in enumerate(Table):
        print("I" + str(index) + ":", end=" ")
        print(" ".join(row))

def printResult(rules):
    for rule in rules:
        print(rule[0] + " -> " + " ".join(rule[1]))

def printAllGOTO(diction):
    for itr in diction:
        print("GOTO(I" + str(itr[0]) + ", " + itr[1] + ") = I" + str(stateMap[itr]))

rules = ["E -> E + T | T",
        "T -> T * F | F",
        "F -> ( E ) | id"
        ]

nonterm_userdef = ['E', 'T', 'F']
term_userdef = ['id', '+', '*', '(', ')']
start_symbol = nonterm_userdef[0]

print("\nOriginal grammar input:")
for rule in rules:
    print(rule)

print("\nGrammar after Augmentation:")
separatedRulesList = grammarAugmentation(rules, nonterm_userdef, start_symbol)
printResult(separatedRulesList)

start_symbol = separatedRulesList[0][0]
print("\nCalculated closure: I0")
I0 = findClosure(0, start_symbol)
printResult(I0)

statesDict = {}
stateMap = {}
statesDict[0] = I0
stateCount = 0

generateStates(statesDict)

print("\nStates Generated:")
for state in statesDict:
    print("State = I" + str(state))
    printResult(statesDict[state])
    print("")

print("Result of GOTO computation:")
printAllGOTO(stateMap)

diction = {}

createParseTable(statesDict, stateMap, term_userdef, nonterm_userdef)
