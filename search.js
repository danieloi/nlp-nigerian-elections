//Demonstrates making a POST request to Twitter Search.
//A headless script that makes a single request, and does not paginate with API supplied tokens.
//Has hardcoded search query. A more useful script would have this passed in ;)
//Write API response to console (system out).
require("dotenv").config();
var request = require("request");
var fs = require("fs");

//Twitter OAuth --- Application only, user context not required.
var search_auth = {
  consumer_key: process.env.CONSUMER_KEY,
  consumer_secret: process.env.CONSUMER_SECRET //,
  //token: process.env.ACCESS_TOKEN,
  //token_secret: process.env.ACCESS_TOKEN_SECRET
};

//Product details
var search_config = {
  url: process.env.TWITTER_SEARCH_URL,
  env: process.env.ENV
};

// build request <-- input
var query = {
  //   query: "(atiku OR atikulated) -buhari -@MBuhari -pmb -buharist",
  query: "(buhari OR @MBuhari OR pmb OR buharist) -atiku -@atiku -atikulated",
  fromDate: "201902010000",
  toDate: "201902222359",
  next:
    "eyJhdXRoZW50aWNpdHkiOiI4YmZiYzhjMzI3NTMwMTVkYzVhMTFlOTRmZjM4OThjMjcwZjY3Mzk0ZTEyNGU3OGQyOGU2M2NlZjg3Y2Y3NWRlIiwiZnJvbURhdGUiOiIyMDE5MDIwMTAwMDAiLCJ0b0RhdGUiOiIyMDE5MDIyMjIzNTkiLCJuZXh0IjoiMjAxOTAyMjIyMzU5MDAtMTA5OTA5NDc4OTEzNDQzNDMwNi0wIn0="
};

// request options
var request_options = {
  //POST form with "body: query" below
  url: "https://" + search_config["url"] + search_config["env"] + ".json",

  oauth: search_auth,
  json: true,
  headers: {
    "content-type": "application/json"
  },
  body: query
};

// POST request
request.post(request_options, function(error, response, body) {
  //console.log(request_options['url'])

  if (error) {
    console.log("Error making search request.");
    console.log(error);
    return;
  }

  fs.writeFile("feb-page-5-buhari.json", JSON.stringify(body), err => {
    console.log("File Created");
  });
});
