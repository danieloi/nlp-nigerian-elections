var fs = require("fs");

/**
 * This file goes through all the tweet data I've fetched from the
 * twitter api and gets the "meat" of the data.
 *
 * the properties to check for are:
 *  - was this retweeted?
 *  - was this quoted?
 *  - is this an extended tweet?
 *
 * according to the docs,
 *
 * a retweet is a restatement of an original tweet without
 * any added text by the retweeter
 *
 * a quoted tweet is a retweet but with added text from the retweeter
 *
 * a
 *
 * Rather than parse "RT..." to discover whether a tweet was a retweet,
 * I take advantage of the root level flags they have like the
 * "retweeted" attribute and just check for the value to determine
 * what attributes contain the data I want.
 *
 * The same goes for quoted tweets.
 *
 * In this case I just use the "is_quote_status" field
 *
 * In the case of retweeted statuses, the meat resides in the
 */

/**
 * Array with cleaned tweet content
 */
const text_from_tweets = [];

const months = ["dec", "january", "feb"];

const checks = ["is_quote_status", "retweeted"];

function cleanUp(tweetsArray, personality) {
  const cleaned = tweetsArray.map(tweet => {
    let meat;

    if (tweet.truncated) {
      meat = tweet.extended_tweet.full_text;
    } else {
      meat = tweet.text;
    }

    if (tweet.retweeted_status) {
      if (tweet.retweeted_status.truncated) {
        meat = tweet.retweeted_status.extended_tweet.full_text;
      } else {
        meat = tweet.retweeted_status.text;
      }
    }

    return { personality, text: meat, sentiment: null };
  });

  return cleaned;
}

function constructTweetsForPersonality(months, personality) {
  let content = [];
  const pages = Array(5)
    .fill(null)
    .map((u, i) => i + 1);

  // console.log(pages);
  // console.log(months);

  months.forEach(month => {
    pages.forEach(page => {
      const filePath = `${month}-page-${page}-${personality}.json`;
      console.log(filePath);

      let file = fs.readFileSync(filePath);
      const resultsArray = JSON.parse(file).results;
      content.push(...resultsArray);
    });
  });

  fs.writeFileSync(`${personality}-complete.json`, JSON.stringify(content));
  console.log(`file: ${personality}-complete.json created!`);
}

// constructTweetsForPersonality(months, "buhari");

function constructTweetsToLabel(file, personality) {
  const tweets = JSON.parse(fs.readFileSync(file));
  const cleaned = cleanUp(tweets, personality);
  fs.writeFileSync(`${personality}-cleaned.json`, JSON.stringify(cleaned));
}

// constructTweetsToLabel("buhari-complete.json", "buhari");

function seperateTenPercentRandomTestData(file, personality) {
  const tweets = JSON.parse(fs.readFileSync(file));
  const test_tweets = [];
  const train_tweets = [];
  tweets.forEach((tweet, i) => {
    if (Math.random() < 0.1) {
      train_tweets.push(tweet);
    } else {
      test_tweets.push(tweet);
    }
  });
  fs.writeFileSync(`${personality}-test.json`, JSON.stringify(test_tweets));
  fs.writeFileSync(`${personality}-train.json`, JSON.stringify(train_tweets));
}

seperateTenPercentRandomTestData("buhari-cleaned.json", "buhari");
