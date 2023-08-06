def get_relative_path(file_path: str, root_dir: str) -> str:
    if root_dir in file_path:
        return './' + file_path.split(root_dir, 1)[-1].strip(' /')

    file_path = file_path.strip('/')
    root_dir = root_dir.strip('/')

    file_path_tokens = file_path.split('/')
    root_dir_tokens = root_dir.split('/')

    i = 0
    maximum = min(len(file_path_tokens), len(root_dir_tokens))
    while i < maximum:
        if file_path_tokens[i] != root_dir_tokens[i]:
            break
        i += 1

    relative_path = '../' * (len(root_dir_tokens) - i)
    relative_path += '/'.join(file_path_tokens[i:])

    return relative_path


print(get_relative_path('/home/rujas/code_workspace/enigma3/def.cc',
                        '/home/rujas/code_workspace/enigma3/cryptography/build/src/v1/abc'))
