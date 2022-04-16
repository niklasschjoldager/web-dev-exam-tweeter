import "./modal.js"
import "./dropdown.js"
import setupInputResize from "./forms/inputResize.js"
import setupTweetsActions from "./tweets/tweets.js"
import setupCreateTweet from "./tweets/createTweet.js"
import setupBackButtons from "./backButtons.js"
import setupMobileMenu from "./mobileMenu.js"

setupCreateTweet('[data-form="create-tweet"]')
setupTweetsActions('[data-form="tweet"]')
setupInputResize('[data-hook="tweet-text"]')
setupBackButtons('[data-button="back"]')
setupMobileMenu('[data-button="mobile-menu"]')
