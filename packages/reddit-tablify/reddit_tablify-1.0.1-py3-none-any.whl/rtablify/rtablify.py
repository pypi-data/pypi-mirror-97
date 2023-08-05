
def makeRedditString(obj, headers=[]):
    if not headers:
        headers = list(obj.keys())

    return ''.join([str(obj[header]) + '|' if index < len(headers) - 1 else str(obj[header]) for index, header in enumerate(headers)])


def tableHeaders(headers):
    return ''.join([header + '|' if index < len(headers) - 1 else header for index, header in enumerate(headers)])


def justificationLine(justifyString, count):
    justifyDict = {
        'c': ':-:',
        'l': ':--',
        'r': '--:'
    }
    if count > len(justifyString):
        difference = count - len(justifyString)
        justifyString += ''.join([justifyString[-1]] * difference)

    return ''.join([justifyDict[char] + '|' if index < len(justifyString) -
                    1 else justifyDict[char] for index, char in enumerate(justifyString)])


def createRedditTable(obj, headers=[], justifyString='c', outputfile='', index='index', includeIndex=False):
    lines = []
    if includeIndex:
        obj = {o: {index: o, **obj[o]} for o in obj}

    if not headers:
        headers = obj[list(obj.keys())[0]]

    lines.append(tableHeaders(headers))

    lines.append(justificationLine(justifyString, len(headers)))

    tableData = [makeRedditString(obj[o]) for o in obj]

    lines += tableData
    if not outputfile:
        [print(line) for line in lines]
    else:
        with open(outputfile, 'w') as f:
            f.writelines('\n'.join(lines))
