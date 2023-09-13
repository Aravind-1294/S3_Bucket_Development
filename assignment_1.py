import boto3
import pandas as pd
import numpy as np
import gradio as gr


session = boto3.Session()
s3 = session.resource(service_name = 's3',
                    region_name='us-east-2',
                    aws_access_key_id='AKIAS2WNRMRNQLY5ILKL',
                    aws_secret_access_key='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')


def aws(files):
    data = open(files.name, 'rb')
    s3.Bucket('20bds010-1').put_object(Key=files.name.split('/')[4], Body=data)
    a=[]
    bucket = s3.Bucket('20bds010-1')
    for obj in bucket.objects.all():
        a.append(obj.key)
    return a

def delete_file(txt):
    s3.Bucket('20bds010-1').delete_objects(Delete={'Objects':[{'Key':txt}]})
    a=[]
    bucket = s3.Bucket('20bds010-1')
    for obj in bucket.objects.all():
        a.append(obj.key)
    return a


with gr.Blocks() as demo:
        gr.Markdown("## Upload Your Files into AWS S3 Bucket")
        file = gr.File(source="Upload")
        btn = gr.Button(value="Submit")
        output_text=gr.outputs.Textbox(label='Files in S3 Bucket After Adding')
        btn.click(aws, inputs=file, outputs=output_text)
        gr.Markdown("## Delete Files From AWS S3 Bucket")
        txt = gr.Textbox(label="Enter the file name to Delete")
        btn1 = gr.Button(value="Submit")
        output_text_delete=gr.outputs.Textbox(label='Files in S3 Bucket After deleting')
        btn1.click(delete_file,inputs=txt,outputs=output_text_delete)        

    
if __name__ == "__main__":
    demo.launch()