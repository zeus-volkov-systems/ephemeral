from ephemeral.build_api.lib_builder import LibBuilder
from typing import List


# Define some functions
def filter_string_length(string_list, word_length=None, comparison=None) -> List[str]:

    if comparison == "less":
        filtered_strings = [string for string in string_list if len(string) < word_length]
    elif comparison == "greater":
        filtered_strings = [string for string in string_list if len(string) > word_length]
    else:
        filtered_strings = string_list
    return filtered_strings


def capitalize_words(words_map) -> List[str]:
    """
    A simple function to illustrate use of the task factory pattern.
    """
    words = words_map["strings"]
    capitalized_words = [word.upper() for word in words]
    return capitalized_words


# Create a library
lib = LibBuilder()

# Add your functions to the library
capitalize = lib.add_function(name='capitalize-words', method=capitalize_words)
filter_word_length_task = lib.add_function(name='filter', method=filter_string_length)

# Create a job
job = lib.create_job('my job')

# Create job tasks, start with input
job_input = job.create_input_task('this is a test')

capitalized = capitalize(job_input, task_name='capitalize')

filtered_long = filter_word_length_task(capitalized, task_name='filter-long', word_length=5, comparison='greater')
filtered_short = filter_word_length_task(capitalized, task_name='filter-short', word_length=6, comparison='less')

job.print_tasks()
