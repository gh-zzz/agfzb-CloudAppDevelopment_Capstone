#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#

from ibmcloudant.cloudant_v1 import CloudantV1, Document
import os

def main(param):
    try:
        os.environ['CLOUDANT_URL'] = param["CLOUDANT_URL"]
        os.environ['CLOUDANT_APIKEY'] = param["CLOUDANT_APIKEY"]
        databaseName = param["CLOUDANT_DATABASE"]
        review = param["review"]
        
        fields_int = ['id', 'dealership', 'car_year']
        fields_str = ['name', 'review', 'purchase_date', 'car_make', 'car_model']
        fields_bool = ['purchase']
        
        doc = {}
        for k,v in review.items():
            if k in fields_int:
                doc[k] = int(v)
            elif k in fields_str:
                doc[k] = str(v)
            elif k in fields_bool:
                doc[k] = bool(v)
        service = CloudantV1.new_instance()
        result = service.post_document(db=databaseName, document=doc).get_result()
        print(result)
    
        return { 'statuscode': 200 }
    except:
        return {
            'statuscode': 500,
            'message': 'Something went wrong on the server'
        }
