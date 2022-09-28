import pika
import time, sys, os, json, ast
import binascii

# ip = "192.168.168.123"
ip = "120.126.18.131"

def main():

    credentials = pika.PlainCredentials('admin','admin')

    parm1 = pika.ConnectionParameters(host=ip, port=5672, credentials=credentials)
    parm2 = pika.ConnectionParameters(host=ip, port=5673, credentials=credentials)
    parm3 = pika.ConnectionParameters(host=ip, port=5674, credentials=credentials)
    all_parm = [parm1, parm2, parm3]
    
    connection = pika.BlockingConnection(
        #pika.ConnectionParameters(host='192.168.168.123', credentials=credentials)
        all_parm
    )
    channel = connection.channel()

    channel.queue_declare(queue='DEMO')

    def callback(ch, method, properties, body):

        # print(" [x] Received %r" % body)
        # time.sleep(2)

        tmp = json.loads(body.decode())
        cipher_polys = ast.literal_eval(tmp["cipherPolys"])
        signature = binascii.unhexlify(tmp["sign"])
        print(f"\ncipher_polys : {cipher_polys}\n\nsignature : {signature}")
        
        pass

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
