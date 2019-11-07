import requests

BASE_URL = 'https://{organization}.backlog.com/api/v2/{api}'

api_key      = '<<BacklogAPI key>>>'
organization = 'nunu00258'  # 組織名
api          = 'issues'
projectId    =   # プロジェクトID
issueId      =  # 課題の種別
priorityId   = 3      # 優先度
summary      = "S3通知" # 件名

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    source_ip   = event['Records'][0]['requestParameters']['sourceIPAddress']
    description  = '''
        Lambda通信局発
          S3バケットにオブジェクトが追加されました。
          対象オブジェクト: {bucket_name}
          実行元IPアドレス: {source_ip}
          改2
    '''
    
    url = BASE_URL.format(organization=organization, api=api)
    payload={
        'projectId': projectId,
        'issueTypeId': issueId,
        'priorityId': priorityId,
        'summary': summary,
        'description': description.format(bucket_name=bucket_name, source_ip=source_ip)
    }
    params={ 'apiKey': api_key }
    r = requests.post(url, params=params, data=payload)
    print(r.json())

