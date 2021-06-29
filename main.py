from enum import Enum


class State(Enum):
    Nothing = 1
    Variable = 2
    VariableName = 3
    VariableValue = 4
    Out = 5
    LineOut = 6


variables = {}


def parseLine(line):
    parseState = State.Nothing
    result = ''
    varName = ''
    for i in range(0, len(line)):
        if parseState == State.Nothing and line[i] == '\\' and (line[i + 1] == '\"' or line[i + 1] == '\''):
            continue
        elif parseState == State.Nothing and line[i] != '$':
            result += line[i]
        elif parseState == State.Nothing and line[i] == '$':
            parseState = State.VariableName
        elif parseState == State.VariableName and line[i] != ' ':
            varName += line[i]
        elif parseState == State.VariableName and line[i] == ' ':
            parseState = State.Nothing
            if varName in variables:
                result += str(variables[varName]) + ' '
            varName = ''

    if parseState == State.VariableName and varName in variables:
        result += str(variables[varName])
    return result


def main():
    input_data = open("input.txt").readlines()

    state = State.Nothing
    currVar = ''
    currValue = ''
    varIsLine = False
    lineOut = ''

    for line in input_data:
        for index in range(0, len(line)):
            if line[index] == ';' and state != State.Nothing:
                if not varIsLine and state == State.Variable:
                    state = State.Nothing
                    variables[currVar] = int(currValue)
                    currVar = ''
                    currValue = ''
                    varIsLine = False
                else:
                    print(state, currVar, currValue, line[index])
                    print('error\n')
                    return
            elif state != State.LineOut and state != State.VariableValue and line[index] == '$':
                state = State.VariableName
            elif state == State.VariableName and line[index] != ' ':
                currVar += line[index]
            elif state == State.VariableName and line[index] == ' ':
                state = State.Variable
            elif state == State.Variable and line[index] == '\"':
                state = state.VariableValue
                varIsLine = True
            elif state == State.VariableValue and (line[index] != '\"' or line[index - 1] == '\\'):
                currValue += line[index]
            elif state == State.Variable and not varIsLine and line[index] != '\"' and line[index] != ' ' and line[index] != '=':
                currValue += line[index]
            elif state == State.VariableValue and line[index] == '\"' and line[index - 1] != '\\':
                state = State.Nothing
                variables[currVar] = parseLine(currValue)
                currVar = ''
                currValue = ''
                varIsLine = False
            elif state == State.Nothing and len(line) > index + 3 and line[index] == 'e' and line[index + 1] == 'c' and line[index + 2] == 'h' and line[index + 3] == 'o':
                state = State.Out
            elif state == State.Out and line[index] == '\"':
                state = State.LineOut
            elif state == State.LineOut and (line[index] != '\"' or line[index - 1] == '\\'):
                lineOut += line[index]
            elif state == State.LineOut and line[index] == '\"' and line[index - 1] != '\\':
                print(parseLine(lineOut))
                lineOut = ''
                state = State.Nothing


if __name__ == "__main__":
    main()
