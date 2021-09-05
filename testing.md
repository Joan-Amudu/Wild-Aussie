# TESTING



## Index – Table of Contents

- [Initial Testing](#intial-testing)


*** 

## Inital Testing
### Mongo DB

Testing connection to Mongodb


### Flask app

Testing Flask 


### connecting Flask to mongo db

Connecting mongo database to flask app
 pip3 install flask-pymongo

 pip3 install dndpython


 using jinja to loop through and getting data from Flask application and bringing it to template


testing css file is being picked up by base template

    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" 
    integrity="sha512-1ycn6IcaQQ40/MKBW2W4Rhis/DbILU74C1vSrLJxCq57o941Ym01SwNsOMqvEBFlcgUa6xLiPY/NS5R+E6ztJQ==" crossorigin="anonymous" referrerpolicy="no-referrer" type="text/css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" type="text/css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" type="text/css">
    {% block styles %}
    {% endblock %}
    <title>Wild Aussie</title>
</head>
<body>

    <h1>Testing base template</h1>

    <h2>Welcome to Wild Aussie</h2>
  
    {% block content %}

    {% endblock %}
   
    <script src="https://code.jquery.com/jquery-3.6.0.js"
      integrity="sha256-H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk=" crossorigin="anonymous"></script> 
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
    {% block scripts %}
    {% endblock %}


css file - testing background color
body {
    background-color: blue;
}




