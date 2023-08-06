import sys


PIPELINE_VERBOSE = False
PIPELINE_MARKER = "[Pipeline]"
PIPELINE_BLOCK_START = '{'
PIPELINE_BLOCK_END = '}'
PIPELINE_BLOCK_START_NOTE = '('
PIPELINE_BLOCK_START_NOTE_END = ')'
PIPELINE_BLOCK_END_NOTE = "//"


def verbose_enable():
    global PIPELINE_VERBOSE
    PIPELINE_VERBOSE = True


def verbose_disable():
    global PIPELINE_VERBOSE
    PIPELINE_VERBOSE = False


def consume_token(s, token, l_trunc=0, r_trunc=0, strip_leading=True):
    """
    :param s: String to scan
    :param token: Substring to target
    :param l_trunc: Truncate chars from left; Positive integer
    :param r_trunc: Truncate chars from right; Positive integer
    :param strip_leading: Remove leading whitespace
    :return: Modified input string
    """
    s_len = len(s)
    token_len = len(token)
    result = s[l_trunc + s.find(token) + token_len:s_len - r_trunc]

    if strip_leading:
        result = result.strip()

    return result


def printv(*args, **kwargs):
    if PIPELINE_VERBOSE:
        kwargs["file"] = sys.stderr
        print(*args, **kwargs)


def parse_log(filename):
    """
    Parse a Jenkins pipeline log and return information about each logical section
    :param filename: path to log file
    :return: list of section dictionaries
    """
    section_defaults = {
        "type": "",
        "name": "",
        "data": "",
        "depth": 0,
    }
    depth = 0
    master_log = False
    last_name = ""
    last_type = ""
    last_line = 0
    section = section_defaults.copy()
    result = list()

    # Reducing code duplication and trying to increase readability with "macro" like functions here.
    # Don't move these.
    def is_pipeline(lobj):
        return lobj[0].startswith(PIPELINE_MARKER)

    def is_pipeline_block_start(lobj):
        return lobj[0] == PIPELINE_BLOCK_START

    def is_pipeline_block_start_note(lobj):
        return lobj[0].startswith(PIPELINE_BLOCK_START_NOTE)

    def is_pipeline_block_end(lobj):
        return lobj[0] == PIPELINE_BLOCK_END

    def is_pipeline_block_end_note(lobj):
        return lobj[0] == PIPELINE_BLOCK_END_NOTE

    def commit(block):
        if block != section_defaults:
            if not block["name"]:
                block["name"] = last_name
            if not block["type"]:
                block["type"] = last_type
            block["depth"] = depth
            block["line"] = last_line
            result.append(block)
            block = section_defaults.copy()
        return block

    # Parsing begins
    for lineno, line in enumerate(open(filename, "r").readlines()):
        line = line.strip()
        if not line:
            continue

        # Format:
        #  [Pipeline]\ {?}?\ (?STRING?|\/\/\ COMMENT?)?
        #
        # The first two arguments are important.
        #  1) Is it a pipeline log record?
        #  2) Is it a block start/end/comment?
        # All string data beyond this point is considered a section "name" or "type"
        data = line.split(" ", 2)

        if is_pipeline(data):
            # Parsing: [Pipeline]
            # Information related to the groovy pipeline is always preceded by: [Pipeline]
            if master_log:
                section = commit(section)

            master_log = False
            section = commit(section)
            data = data[1:]

            if is_pipeline_block_end(data):
                # Parsing: [Pipeline] }
                depth -= 1
                printv("DEPTH ::", depth)
                if section != section_defaults:
                    section = commit(section)
            elif is_pipeline_block_end_note(data):
                # Ignoring: [Pipeline] // NAME HERE
                pass
            elif is_pipeline_block_start(data):
                # Parsing: [Pipeline] {
                depth += 1
                printv("DEPTH ::", depth)

                if len(data) == 2:
                    # Parsing: [Pipeline] { (NAME HERE)
                    # Read the stage name.
                    # Stage names are preceded by a "{" and the literal name is encapsulated by parenthesis
                    x = data[1:]
                    if is_pipeline_block_start_note(x):
                        section["name"] = consume_token(x[0], PIPELINE_BLOCK_START_NOTE, r_trunc=1)
                        last_name = section["name"]
                        printv("NAME  ::", section["name"])
            elif len(data) == 1:
                # Parsing: [Pipeline] NAME HERE
                # A standalone string without a preceding "{" denotes the type of step being executed
                section["type"] = data[0]
                last_type = section["type"]
                printv("TYPE  ::", section["type"])

            # Finished with [Pipeline] data for now... see if there's more
            last_line = lineno
            continue

        if not depth and not is_pipeline(line):
            # Parser depth begins at zero. Trigger only when a line doesn't begin with: [Pipeline]
            master_log = True
            section["name"] = "master"
            section["type"] = "masterLog"
            section["data"] += line + "\n"
            section["depth"] = depth
        else:
            # Consume raw log data at current depth
            section["type"] = last_type
            section["data"] += line + "\n"
            printv("RAW   ::", line)

    # Save any data appearing after: [Pipeline] End of Pipeline
    # This data belongs to the master node
    commit(section)

    return result
