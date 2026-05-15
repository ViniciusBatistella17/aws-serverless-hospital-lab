import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ProntuariosPacientes')

def lambda_handler(event, context):
    print("--- CARTA RECEBIDA DO S3 ---")
    print(event) 
    print("----------------------------")

    try:
        
        nome_do_arquivo = event['Records'][0]['s3']['object']['key']
        nome_do_bucket = event['Records'][0]['s3']['bucket']['name']
        
        print(f"Processando arquivo {nome_do_arquivo} do bucket {nome_do_bucket}")

        # Salvando TUDO em um único registro (Mais eficiente)
        table.put_item(
            Item={
                'id_atendimento': nome_do_arquivo, 
                'Status': 'Processado pelo Lambda',
                'Projeto': 'Saude_Tech_N1',
                'Bucket_Origem': nome_do_bucket # Guardamos o nome do bucket como uma coluna extra
            }
        )
        
        return {'statusCode': 200, 'body': 'Arquivo processado com sucesso!'}

    except Exception as e:
        print(f"Erro detectado: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Erro ao salvar no banco.')
        }
