import "./modal.js"
import "./dropdown.js"
import setupInputResize from "./forms/inputResize.js"
import setupTweetsActions from "./tweets/tweets.js"
import setupCreateTweet from "./tweets/createTweet.js"

setupCreateTweet("[data-form=create-tweet]")
setupTweetsActions("[data-form=tweet]")
setupInputResize("[data-hook=tweet-text]")
