# ace-power

A simple backend server, aiming for high concurrency.

## How to run it?

First, install Python packages specified in `requirements.txt` with `pip`:

```
pip install -r requirements.txt
```

Then, as this program runs together with MySQL, Redis, RabbitMQ, you also need to install and configure them correctly. The simplest way is to use package managers like `apt` (if you don't mind installing outdated versions):

```
sudo apt update
sudo apt install mysql-server
sudo apt install redis-server
sudo apt insatll rabbitmq-server
```

After successfully installing these software, edit `config.py` to make sure you can connect to them correctly.

If everything goes well, now you can easily run this program for debugging:

```
uvicorn server:app --reload
```

Also, don't forget to run `consumer.py` at the same time. Otherwise,  there will be nobody to query from MySQL actually!

## Architecture

![architecture](./architecture.png)