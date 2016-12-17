# Web view for Exercise 6. Search engine of news.
To run this You need to:<br>
1. download [Elasticsearch](https://www.elastic.co/downloads/elasticsearch)<br>
2. run `bin\elasticsearch`<br>
3. execute [notebook](../../Excercises_6.ipynb)<br>
4. export FLASK_APP=flaskr<br>
5. flask run<br>
   Then you can proceed to http://localhost:5000/<br>
6. Enter **login: admin**, **password: default**<br>

### Additional data
You need to download [texts](https://yadi.sk/d/92TbmE7cy5Lds) and put it in `data\` folder. This is due to the reason that github does not allow to load files larger than 100mb. <br>

In the end, you should get something like this:<br>
![web view example](images/2016-12-17_20-15-58.png)

Thanks to flask for [flaskr example](https://github.com/pallets/flask/tree/master/examples/flaskr/)
