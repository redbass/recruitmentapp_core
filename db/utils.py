def dict_to_datapath(data):
    result = {}

    for key, value in data.items():

        if isinstance(value, dict):

            sub_data = dict_to_datapath(value)

            if sub_data.items():

                for sub_key, sub_value in sub_data.items():
                    new_key = '.'.join([key, sub_key])
                    result[new_key] = sub_value

            else:

                result[key] = sub_data

        else:
            result[key] = value

    return result
