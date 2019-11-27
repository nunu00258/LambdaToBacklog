import requests, os, urllib.parse
# S3の通知をBacklogに送る
# 環境変数にうまくいれてな

BASE_URL = 'https://{organization}.backlog.com/api/v2/{api}'

api_key      = os.environ['BACKLOG_KEY']
organization = os.environ['BACKLOG_ORG']  # 組織名
api          = 'issues'
projectId    = os.environ['BACKLOG_PROJECT']  # プロジェクトID
issueId      = os.environ['BACKLOG_ISSUE'] # 課題の種別
priorityId   = 3      # 優先度
summary      = "config通知" # 件名

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    source_ip   = event['Records'][0]['requestParameters']['sourceIPAddress']
    object_name = urllib.parse.unquote(event['Records'][0]['s3']['object']['key'])
    object_size = int(event['Records'][0]['s3']['object']['size']) /1024
    description  = '''
        S3にオブジェクト追加されました
          対象バケット: {bucket_name}
          追加されたファイル: {object_name}
          ファイルのサイズ: {object_size}KB
          実行元IPアドレス: {source_ip}
    '''
    
    url = BASE_URL.format(organization=organization, api=api)
    payload={
        'projectId': projectId,
        'issueTypeId': issueId,
        'priorityId': priorityId,
        'summary': summary,
        'description': description.format(
            bucket_name=bucket_name, 
            object_name=object_name,
            object_size=object_size,
            source_ip=source_ip
        )
    }
    params={ 'apiKey': api_key }
    r = requests.post(url, params=params, data=payload)
    print(r.json())
