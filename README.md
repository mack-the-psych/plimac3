# plimac3
## Python3-based NLP library for assessment content/constructed response

## Docker usage example
$ docker build . -t trial_plimac3 <br>
$ docker run -v /home/ubuntu/MELVA-S:/MELVA-S -p 9999:9999 -p 6006:6006 -it --name plimac3_run trial_plimac3 <br>
\# exit <br><br>
$ docker start plimac3_run <br>
$ docker exec -it plimac3_run jupyter notebook --port 9999 --ip=0.0.0.0 --allow-root <br>
