# Docker Swarm Demo
Docker containers have already changed the way we develop and ship software,
but container orchestration can seem like a very daunting task when you're
ready to scale up in production.

This project lays out a simplified example of how to deploy your app to Docker
Swarm, which is Docker's built-in container orchestration mechanism.

## What is the app?
It's a simple Flask app that tells you the id of the container the process is
running in, as well as the number of requests it has received.

A shared redis process is utilized so the request count is persistent.

## What are the takeaways here?
The goal is to demonstrate just how easy it is to deploy a stack of services
to a swarm. Without any work, the web workers will find the redis process
thanks to Docker's internal DNS magic. Additionally, the nginx and web services
can be scaled up as much as you wish. You'll be able to see how when you make
a request to the swarm, it will automatically load balance the requests across
the running containers. It also emphasizes just how easy Swarm makes it to
securely store and deploy your app's secrets.

## How do I get started?
To test the app on your computer without Swarm mode, simply run:
```
docker-compose up
```

If you're on a machine (or several machines) with Swarm, you can deploy it as
a stack:
```
echo "supersecretpassword" | docker secret create db_password -

docker stack deploy -c docker-compose.yml demo
docker stack deploy -c docker-compose.override.yml demo
```

The first line defines the `db_password` secret in your Swarm, and the second deploys the actual stack.
https://www.callicoder.com/docker-machine-swarm-stack-golang-example/

# Add label
docker node update --label-add api=true twj0h009ik6bntl4ejoae4pe7
docker node update --label-add api=true i6m5t7ecmu8yv6xfny5xz4vv9
docker node update --label-add nginx=true i6m5t7ecmu8yv6xfny5xz4vv9
docker node update --label-add celery_worker=true ytnceolfpy0sre2rbu782zbkk
# Remove label
docker node update --label-rm api ytnceolfpy0sre2rbu782zbkk
docker node update --label-rm api p5hsf6ckj07r4jxd5iv4a4ojf
docker node update --label-rm nginx p5hsf6ckj07r4jxd5iv4a4ojf
docker node update --label-rm nginx ytnceolfpy0sre2rbu782zbkk
docker node update --label-rm demo_nginx ytnceolfpy0sre2rbu782zbkk


# Get Label of node
docker node ls -q | xargs docker node inspect \
  -f '{{ .ID }} [{{ .Description.Hostname }}]: {{ .Spec.Labels }}'

# Deploy
docker stack deploy -c docker-compose.yml demo

docker swarm init --advertise-addr 178.128.26.202