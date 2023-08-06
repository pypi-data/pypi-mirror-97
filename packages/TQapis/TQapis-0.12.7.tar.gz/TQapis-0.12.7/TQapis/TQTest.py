import os
from .TQConnection import Connection, Message
from .TQConnection import TQRequests


def make_request( param, function_name):
    return TQRequests.ParamBuilder().build(param, function_name)


def delete_file(result_new_file_path):
    try:
        os.remove(result_new_file_path)
    except:
        pass
    return Message(True, "")


def write_test_file(file_path,section_tag, params, delimiter_char, comment_char):
    try:
        writefile = open(file_path, "w")
        for name, param in params:
            line = section_tag+":"+name+"\n"
            writefile.write(line)
            for key, value in param.items():
                line = key.lstrip()+ delimiter_char + value + "\n"
                writefile.write(line)
            writefile.write("\n")
        writefile.close()
        return Message(True, "")
    except Exception as e:
        return Message(False, str(e))


def read_test_file(file_path, section_tag, delimiter, comment):
    params = list()
    param = None
    try:
        line_cntr = 0
        inputfile = open(file_path, "r")
        for line in inputfile:
            # ignore blank lines
            if len(line.lstrip()) == 0:
                line_cntr += 1
                continue
            loc = line.rfind(comment)
            if loc == 0:
                line_cntr += 1
                continue

            #
            # a proper line to process
            #
            #has it got comment?
            if comment in line:
                line=line.split(comment)[0]
            #empty line on the ledt side?
            if line.rstrip().lstrip()=='':
                continue

            if section_tag in line:
                tag_name=""
                if ':' in line:
                    tag_name=line.split(':')[1].lstrip().rstrip().replace('\n','')
                param = dict()
                params.append((tag_name,param))
                continue

            if line.find(delimiter)==-1:
                line_cntr += 1
                return Message(False,
                               "Missing delimiter {} in file {} line:{}".format(delimiter, file_path,
                                                                                line_cntr)), params
            tokens = line.split(delimiter)
            tokens[0] = tokens[0].lstrip().rstrip()
            tokens[1] = tokens[1].lstrip().rstrip().replace('"', '')
            if len(tokens[0]) == 0:
                line_cntr += 1
                return Message(False,
                               "Missing delimiter key in key-value pair in file {} line:{}".format(file_path,
                                                                                                   line_cntr)), params
            if len(tokens[1]) == 0:
                line_cntr += 1
                return Message(False,
                               "Missing delimiter value in key-value pair in file {} line:{}".format(file_path,
                                                                                                     line_cntr)), params
            param[tokens[0]] = tokens[1]
            line_cntr += 1
        inputfile.close()
        return Message(True, ""), params
    except Exception as e:
        return Message(False, str(e)), params

def _process_diff(result_new_file_path,result_section_tag,result_news,delimiter_char,comment_char):
    Message = write_test_file(result_new_file_path, result_section_tag, result_news, delimiter_char,
                              comment_char)
    Message.content = "New results generated!"
    return Message


class Runner:
    def __init__(self, email,target_url):
        self.__param_factory = [
            'describe'
            ,'account_status'
            , 'account_password_change'
            , 'account_ip_change'
            , 'account_create'
            , 'account_send_activation_key'
            , 'account_activate'
            , 'account_profile'
            , 'account_activation_key_status'
            , 'ip_return'
            , 'market_fx_rates'
            , 'show_available'
            , 'workspace'
            , 'market_swap_rates'
            , 'pnl_attribute'
            , 'pnl_predict'
            , 'price'
            , 'price_fx_forward'
            , 'price_vanilla_swap'
            , 'risk_ladder'
            , 'formatted_grid_swap_rates'
            , 'formatted_grid_fx'
        ]
        self.connection = Connection(email,target_url)

    def validate(self, params):
        if 'function_name' not in params:
            return Message(False, "There is no value for the key 'function_name'.")
        function_name = params['function_name']
        if function_name not in self.__param_factory:
            return Message(False, "function_name '" + function_name + "' is not recognised.")
        # param_builder = self.__param_factory[function_name]
        # Message = param_builder.validate(params)
        # if not Message.is_OK:
        #     return Message
        return Message(True, "")

    def send(self, params):
        function_name = params['function_name']
        #param_builder = self.__param_factory[function_name]
        request = make_request(params, function_name)

        Message = self.connection.send(request)
        return Message

    def get_response(self):
        return self.connection.response

    def get_all_test_file_names(self, root_folder, request_extension):
        file_names = list()
        for root, dirs, files in os.walk(root_folder):
            for filename in files:
                fname, fextension = os.path.splitext(filename)
                if fextension.lower() == "." + request_extension.lower():
                    file_names.append(fname)
        return file_names

    def run(self, root_folder, request_extension='request', result_extension='result',
            result_new_extension='result_new'):
        report = dict()
        test_file_names = self.get_all_test_file_names(root_folder, request_extension)
        for test_file_name in test_file_names:
            Message = self.execute_single_test(root_folder, test_file_name, request_extension, result_extension,
                                             result_new_extension)
            status_result = "OK"
            if len(Message.content) > 0:
                status_result = Message.content
            report[test_file_name] = status_result
            print ("{}:{}".format(test_file_name,status_result))
        return report

    def execute_single_test(self, root_folder, test_file_name, request_extension="request", result_extension="result", result_new_extension="result_new"):
        delimiter_char = '='
        comment_char = '#'
        test_section_tag = "[test]"
        result_section_tag = "[result]"

        volatile_list=['activation_key', 'balance', 'ip', 'last_login','ip_return', 'id']

        request_file_path = os.path.join(root_folder, test_file_name + "." + request_extension)
        result_file_path = os.path.join(root_folder, test_file_name + "." + result_extension)
        result_new_file_path = os.path.join(root_folder, test_file_name + "." + result_new_extension)

        Message, names_with_params = read_test_file(request_file_path,test_section_tag, delimiter_char, comment_char)

        result_news=list()
        if not Message.is_OK:
            return Message

        for name,param in names_with_params:
            Message = self.validate(param)
            if not Message.is_OK:
                return Message

            Message = self.send(param)
            return_values=dict()
            return_values= self.connection.response.results
            if not Message.is_OK:
                return_values = self.connection.response.errors

            return_values_clean=dict()
            for key, value in  return_values.items():
                return_values_clean[key]=value.rstrip().lstrip()

            result_news.append((name,return_values_clean))
            Message = delete_file(result_new_file_path)
            if not Message.is_OK:
                return Message



        Message, base_results = read_test_file(result_file_path,result_section_tag, delimiter_char, comment_char)

        if (len(base_results) == 0):
            Message = write_test_file(result_file_path,result_section_tag, result_news, delimiter_char, comment_char)
        else:
            if len(result_news) !=len(base_results):
                Message = _process_diff(result_new_file_path, result_section_tag, result_news, delimiter_char,
                                        comment_char)
            else:
                for i in range(0,len(result_news)):
                    base_name=base_results[i][0]
                    new_names=result_news[i][0]
                    if new_names!=base_name:
                        Message = _process_diff(result_new_file_path, result_section_tag, result_news, delimiter_char, comment_char)
                    else:
                        base_param=base_results[i][1]
                        new_param=result_news[i][1]
                        base_keys=base_param.keys()
                        new_keys=new_param.keys()
                        if new_keys!=base_keys:
                            Message = _process_diff(result_new_file_path, result_section_tag, result_news, delimiter_char,
                                                    comment_char)
                        else:
                            for base_key in base_keys:
                                if (base_key not in volatile_list) and new_param[base_key] != base_param[base_key]:
                                    Message = _process_diff(result_new_file_path, result_section_tag, result_news,
                                                            delimiter_char, comment_char)

        return Message


def run_test_all(folder, email,  target_url="http://operations.treasuryquants.com"):

    runner = Runner(email,  target_url)
    return runner.run(folder)


def run_test_single(root_folder, file_path,email, target_url="http://operations.treasuryquants.com"):

    runner = Runner(email, target_url)
    status_result = "OK"
    Message=runner.execute_single_test(root_folder,file_path)
    if len(Message.content) > 0:
        status_result = Message.content
    print(file_path, status_result)
    report={file_path:status_result}
    return report


