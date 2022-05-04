import "./modal.js"
import "./dropdown.js"
import setupInputResize from "./forms/inputResize.js"
import setupTweetsActions from "./tweets/tweets.js"
import setupCreateTweet from "./tweets/createTweet.js"
import setupMobileMenu from "./mobileMenu.js"
import setupUserActions from "./users/users.js"
import setupForms from "./forms/forms.js"

setupCreateTweet('[data-form="create-tweet"]')
setupTweetsActions('[data-form="tweet"]')
setupInputResize('[data-hook="tweet-text"]')
setupMobileMenu('[data-button="mobile-menu"]')
setupUserActions('[data-form="user"]')
setupForms("[data-form]")
