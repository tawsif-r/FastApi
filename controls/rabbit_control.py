import pika
import json
import uuid




class RabbitControl():
    def __init__(self,hostname:str)->None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(hostname))
        self.channel = self.connection.channel()
        
    
    def exchange_set(self,exchange:str,exchange_type:str)->None:
        """
        Sets the exchange parameters for the message broker
        Args:
            exchange (str): The exchange name e.g 'order'.
            exchange_type (str): The type of exchange this would be e.g 'direct'.

        Returns:
            None

        """

        self.exchange = exchange
        self.exchange_type = exchange_type
        self.channel.exchange_declare(
        exchange=self.exchange,
        exchange_type = self.exchange_type, 
        )
        
    def publish_notify(self,content:dict,credential:str)->str:
        """
        Publish a notification message with the provided content.
        Args:
            content (dict): e.g order = {
                                        'id':str(uuid.uuid4()),
                                        'user_email':'john.doe@gmail.com',
                                        'product':'Leather Jacket',
                                        'quantity':1
                                        }
        Returns:
            str
        
        """
        try:
            self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=f'{self.exchange}.notify',
            body = json.dumps({f'{credential}':content[credential]})
            )
            print('[x] Sent notify message')
        except:
            print('[!] Failed to send notify message')
            raise

    def publish_report(self,content)->str:
        """
        Publishes a report message to the RabbitMQ exchange with the specified content.
        Args:
            content (dict): The content of the report to be published. This should be a dictionary that will be converted to a JSON string.
        Returns:
            str: A confirmation message indicating that the report message has been sent.
        Raises:
            pika.exceptions.AMQPError: If there is an error during the publishing process.
        Example:
            content = {"report_id": 123, "status": "completed"}
            self.publish_report(content)
        """

        self.channel.basic_publish(
            exchange = self.exchange,
            routing_key = f'{self.exchange}.report',
            body = json.dumps(content)
        )
        print(' [x] Sent report message')

    def get_notification(self,exchange:str,cred:str):
        
        """
        Args:
            exchange (str): The name of the exchange
            cred(str): the name of person or the id or even the email of the person in concern

        Returns:
            None
            
        """

        queue = self.channel.queue_declare(f'{exchange}_notify')
        queue_name = queue.method.queue

        self.channel.queue_bind(
            exchange=exchange,
            queue=queue_name,
            routing_key=f'{exchange}.notify'
        )

        def callback(ch, method,properties,body):
            payload = json.loads(body)
            print(' [x] Notifying {}'.format(payload[cred]))
            print(' [x] Done')
            ch.basic_ack(delivery_tag = method.delivery_tag)

        self.channel.basic_consume(on_message_callback=callback,queue=queue_name)
        print(' [*] Waiting for notify messages. To exit press CTL + C')
        self.channel.start_consuming()
    
    def get_report(self,exchange:str,fields:list):
        """
        Args:
            exchange (str): The name of the exchange
            fields (list): The list of fields for the payload

        Returns:
            None
            
        """

        queue = self.channel.queue_declare(f'{exchange}_report')
        queue_name = queue.method.queue

        self.channel.queue_bind(
            exchange=exchange,
            queue=queue_name,
            routing_key=f'{exchange}.report' #binding key
        )

        def callback(ch, method,properties,body):
            payload = json.loads(body)
            print(' [x] Generating report')
            for field in fields:
                print(f"{field} : {payload.get(field)} \n")
            print(' [x] Done')
            ch.basic_ack(delivery_tag = method.delivery_tag)

        self.channel.basic_consume(on_message_callback=callback,queue=queue_name)
        print(' [*] Waiting for Report messages. To exit press CTL + C')
        self.channel.start_consuming()



    def close(self):
        self.connection.close()

        