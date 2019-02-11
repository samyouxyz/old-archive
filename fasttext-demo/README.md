# fastText Web Demo
Web demo of Facebook's [fastText](https://fasttext.cc/) language detection.

TRY IT: Since I use Heroku free dyno, the first time you get the result might take several seconds because the server needed to wake up from sleep. Now, check it out: [yrsamrith.github.io/fasttext-demo](https://yrsamrith.github.io/fasttext-demo/)


## Explanation
- Client contains the HTML/Javascript files for frontend.
- Server is a Flask app deployed to Heroku. You can run it local or deploy to your own Heroku dyno.
- The client sends POST request with JSON data, e.g. { "text": "Bonjour" }, to fasttext.herokuapp.com/v1/detectlanguage. The response looks like this: { "result": "en" }.
- In the server, app.py uses fastText to detect "text" from the POST request.

## Philosophy
- Minimal
- A little bit crappy sometimes
