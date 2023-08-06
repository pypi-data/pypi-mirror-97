import io
import json
import logging
import os
import yaml
import re
from collections import OrderedDict

from postman2case.compat import ensure_ascii
from postman2case.parser import parse_value_from_type


class PostmanParser(object):
    def __init__(self, postman_testcase_file):
        self.postman_testcase_file = postman_testcase_file

    def read_postman_data(self):
        with open(self.postman_testcase_file, encoding='utf-8', mode='r') as file:
            postman_data = json.load(file)

        return postman_data
    
    def parse_url(self, request_url):
        url = ""
        if isinstance(request_url, str):
            url = request_url
        elif isinstance(request_url, dict):
            if "raw" in request_url.keys():
                url= request_url["raw"]
        return url
    
    def parse_header(self, request_header, api):
        headers = {}
        for header in request_header:
            key = header["key"]
            value = header["value"]
            for v in re.findall(r'\{\{.+?\}\}', key):
                api['config']["variables"][v[2:-2]] = ''
                key = key.replace(v, '${}'.format(v[2:-2]))
            for v in re.findall(r'\{\{.+?\}\}', value):
                api['config']["variables"][v[2:-2]] = ''
                value = value.replace(v, '${}'.format(v[2:-2]))
            headers[key] = value
        return headers

    def parse_each_item(self, item, variable=[]):
        """ parse each item in postman to testcase in httprunner
        """
        api = dict(config=dict(base_url='$base_url'), teststeps=[])
        api['config']["name"] = item["name"]
        api['config']["variables"] = dict()

        request = {}
        request["method"] = item["request"]["method"]

        url = self.parse_url(item["request"]["url"])

        if request["method"] == "GET":
            request["url"] = url.split("?")[0]
            request["headers"] = self.parse_header(item["request"]["header"], api)

            body = {}
            if "query" in item["request"]["url"].keys():
                for query in item["request"]["url"]["query"]:
                    api['config']["variables"][query["key"]] = parse_value_from_type(query["value"], api)
                    body[query["key"]] = "${}".format(query["key"])
            request["params"] = body
        else:
            for v in re.findall(r'\{\{.+?\}\}', url):
                api['config']["variables"][v[2:-2]] = ''
                url = url.replace(v, '${}'.format(v[2:-2]))
            request["url"] = url
            request["headers"] = self.parse_header(item["request"]["header"], api)

            body = {}
            if item["request"].get("body") and item["request"]["body"] != {}:
                mode = item["request"]["body"]["mode"]
                if isinstance(item["request"]["body"][mode], list):
                    for param in item["request"]["body"][mode]:
                        if param["type"] == "text":
                            api['config']["variables"][param["key"]] = parse_value_from_type(param["value"], api)
                        else:
                            api['config']["variables"][param["key"]] = parse_value_from_type(param["src"], api)
                        body[param["key"]] = "${}".format(param["key"])
                elif isinstance(item["request"]["body"][mode], str):
                    try:
                        mode_body = item["request"]["body"][mode]
                        for v in re.findall(r'\{\{.+?\}\}', mode_body):
                            api['config']["variables"][v[2:-2]] = ''
                            mode_body = mode_body.replace(v, '${}'.format(v[2:-2]))
                        body = json.loads(mode_body, encoding='utf8')
                    except Exception as e:
                        body = mode_body
            if isinstance(body, dict):
                request["json"] = body
            else:
                request["data"] = body

        for var in variable:
            if var.get('key'): api['config']["variables"][var.get('key')] = var.get('value')
        api["teststeps"].append(dict(name=url, request=request, validate=[dict(eq=['status_code', 200]), dict(eq=['body.code', 0])]))
        return api
    
    def parse_items(self, items, folder_name=None, variable=[]):
        result = []
        for folder in items:
            if "item" in folder.keys():
                name = folder["name"].replace(" ", "_")
                if folder_name:
                    name = os.path.join(folder_name, name)
                temp = self.parse_items(folder["item"], name, variable)
                result += temp
            else:
                api = self.parse_each_item(folder, variable)
                api["folder_name"] = folder_name
                result.append(api)
        return result

    def parse_data(self):
        """ dump postman data to json testset
        """
        logging.info("Start to generate JSON testset.")
        postman_data = self.read_postman_data()

        result = self.parse_items(postman_data["item"], postman_data.get('info', {}).get('name'), postman_data.get('variable', []))
        return result, postman_data.get('info', {}).get('name')

    def save(self, data, output_dir, output_file_type="json", name=''):
        count = 0
        output_dir = os.path.join(output_dir, "TestCases", "APICase")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        test_suites = dict(config=dict(name=name, variables=dict(base_url='')), testcases=[])
        for each_api in data:
            count += 1
            file_name = "{}.{}".format(count, output_file_type)
            
            folder_name = each_api.pop("folder_name")
            if folder_name:
                folder_path = os.path.join(output_dir, folder_name)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                file_path = os.path.join(folder_path, file_name)
            else:
                file_path = os.path.join(output_dir, file_name)
            if os.path.isfile(file_path):
                logging.error("{} file had exist.".format(file_path))
                continue
            if output_file_type == "json":
                with io.open(file_path, 'w', encoding="utf-8") as outfile:
                    my_json_str = json.dumps(each_api, ensure_ascii=ensure_ascii, indent=4)
                    if isinstance(my_json_str, bytes):
                        my_json_str = my_json_str.decode("utf-8")

                    outfile.write(my_json_str)
            else:
                with io.open(file_path, 'w', encoding="utf-8") as outfile:
                    my_json_str = json.dumps(each_api, ensure_ascii=ensure_ascii, indent=4)
                    yaml.dump(each_api, outfile, allow_unicode=True, default_flow_style=False, indent=4)
            test_suites['testcases'].append(dict(name=each_api.get('config').get('name'), testcase=file_path.replace('\\', '/')))    
            logging.info("Generate JSON testset successfully: {}".format(file_path))
        if test_suites.get('testcases'):
            folder_path = os.path.join(output_dir)
            file_name = "TEST_{}_testSuite.{}".format(test_suites.get('config').get('name'), output_file_type)
            file_path = os.path.join(folder_path, file_name)
            if output_file_type == "json":
                with io.open(file_path, 'w', encoding="utf-8") as outfile:
                    my_json_str = json.dumps(test_suites, ensure_ascii=ensure_ascii, indent=4)
                    if isinstance(my_json_str, bytes):
                        my_json_str = my_json_str.decode("utf-8")

                    outfile.write(my_json_str)
            else:
                with io.open(file_path, 'w', encoding="utf-8") as outfile:
                    my_json_str = json.dumps(test_suites, ensure_ascii=ensure_ascii, indent=4)
                    yaml.dump(test_suites, outfile, allow_unicode=True, default_flow_style=False, indent=4)
            logging.info("Generate testsuite successfully: {}".format(file_path))
