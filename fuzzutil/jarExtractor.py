import subprocess
import sys
sys.path.append("..")
from common import PathContextInformation


class JarExtractor:
    def __init__(self, config, jar_path, max_path_length, max_path_width):
        self.config = config
        self.max_path_length = max_path_length
        self.max_path_width = max_path_width
        self.jar_path = jar_path


    def extract_paths(self, path):
        command = ['java', '-Xmx100g', '-XX:MaxNewSize=60g', '-cp', self.jar_path, 'JavaExtractor.App',
                   '--max_path_length', str(self.max_path_length), '--max_path_width', str(self.max_path_width),
                   '--file', path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        output = out.decode().splitlines()
        if len(output) == 0:
            err = err.decode()
            raise ValueError(err)
        hash_to_string_dict = {}
        pc_info_dict = {}
        result = []
        for i, line in enumerate(output):
            parts = line.rstrip().split(' ')
            method_name = parts[0]
            current_result_line_parts = [method_name]
            contexts = parts[1:]
            for context in contexts[:self.config.MAX_CONTEXTS]:
                # print("context:", context)
                context_parts = context.split(',')
                context_word1 = context_parts[0]
                context_path = context_parts[1]
                context_word2 = context_parts[2]
                contextInfo = {'name1': context_word1, 'path': '', 'shortPath': context_path, 'name2': context_word2}
                pc_info = PathContextInformation(contextInfo)
                current_result_line_parts += [str(pc_info)]
                pc_info_dict[(pc_info.token1, pc_info.shortPath, pc_info.token2)] = pc_info
                # hashed_path = str(self.java_string_hashcode(context_path))
                # hash_to_string_dict[hashed_path] = context_path
                # current_result_line_parts += ['%s,%s,%s' % (context_word1, hashed_path, context_word2)]
            space_padding = ' ' * (self.config.MAX_CONTEXTS - len(contexts))
            result_line = ' '.join(current_result_line_parts) + space_padding
            result.append(result_line)
        # return result, hash_to_string_dict
        return result, pc_info_dict

    def ExtractFeaturesForDir(self, dir):
        command = ['java', '-Xmx100g', '-XX:MaxNewSize=60g', '-cp', self.jar_path, 'JavaExtractor.App',
                   '--max_path_length', str(self.max_path_length), '--max_path_width', str(self.max_path_width),
                   '--dir', dir, '--num_threads', str(1)]

        # print command
        # os.system(command)
        kill = lambda process: process.kill()
        outputFileName = "dir" + dir.split('/')[-1] + ".txt"
        failed = False
        with open(outputFileName, 'a') as outputFile:
            sleeper = subprocess.Popen(command, stdout=outputFile, stderr=subprocess.PIPE)

    @staticmethod
    def java_string_hashcode(s):
        """
        Imitating Java's String#hashCode, because the model is trained on hashed paths but we wish to
        Present the path attention on un-hashed paths.
        """
        h = 0
        for c in s:
            h = (31 * h + ord(c)) & 0xFFFFFFFF
        return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000
