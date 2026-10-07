"""Source declarations only; execution remains in the accepted evaluators."""
from domain_source_vm import parse, Array, Literal, word

SYSTEM_SELECTORS = {
    'name': 0, '-objID-': 0x1000, '-size-': 0x1001,
    '-propDict-': 0x1002, '-methDict-': 0x1003,
    '-classScript-': 0x1004, '-script-': 0x1005,
    '-super-': 0x1006, '-info-': 0x1007,
}


def literal(value, constants):
    if isinstance(value, int):
        return word(value)
    if type(value) is str and value in constants:
        return literal(constants[value], constants)
    raise ValueError(('Only numeric static declarations are supported', value))


def declarations(source):
    ast = parse(source)
    constants = {n[1]: n[2] for n in ast if n[0] == 'define'}
    result = []
    offset = 0
    for node in ast:
        if node[0] != 'local':
            continue
        i = 1
        while i < len(node):
            declaration = node[i]
            i += 1
            if not isinstance(declaration, Array) or len(declaration) != 2:
                raise ValueError(('Named fixed-size local array required', declaration))
            name, count = declaration
            count = literal(count, constants)
            if count <= 0:
                raise ValueError(('Invalid array size', name, count))
            values = []
            if i < len(node) and node[i] == '=':
                values = [literal(v, constants) for v in node[i + 1]]
                i += 2
            if len(values) > count:
                raise ValueError(('Initializer exceeds array', name))
            result.append(dict(name=name, word_offset=offset, byte_offset=2*offset,
                               word_count=count, initial_words=values+[0]*(count-len(values))))
            offset += count
    return result


def selector_map(sources):
    result = dict(SYSTEM_SELECTORS)
    names = []
    for source in sources:
        for node in parse(source):
            if node[0] != 'class':
                continue
            for part in node[2:]:
                if not isinstance(part, list) or not part:
                    continue
                if part[0] == 'properties':
                    names.extend(part[1::2])
                elif part[0] == 'method':
                    names.append(part[1][0])
    for name in names:
        if name not in result:
            index = 1
            while index in result.values():
                index += 1
            if index >= 0x1000:
                raise ValueError('Domain selectors collide with system selectors')
            result[name] = index
    return result
