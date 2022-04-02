#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#

from ibmcloudant.cloudant_v1 import CloudantV1
import os

def main(param):
    try:
        os.environ['CLOUDANT_URL'] = param["CLOUDANT_URL"]
        os.environ['CLOUDANT_APIKEY'] = param["CLOUDANT_APIKEY"]
        databaseName = param["CLOUDANT_DATABASE"]
    
        fields_int = ['id']
        fields_str = ['city', 'state', 'st', 'address', 'zip', 'short_name', 'full_name']
        fields_float = ['lat', 'long']
        
        selector = {}
        for k,v in param.items():
            if k in fields_int:
                selector[k] = int(v)
        for k,v in param.items():
            if k in fields_str:
                selector[k] = v
        service = CloudantV1.new_instance()
        result = service.post_find(
            db=databaseName,
            selector=selector,
            fields=fields_int+fields_str+fields_float,
        ).get_result()['docs']
    
        print(result)
        
        if len(result) == 0:
            return {
                'statuscode': 404,
                'message': 'The database is empty'
            }
        return { databaseName: result }
    except:
        return {
            'statuscode': 500,
            'message': 'Something went wrong on the server'
        }
