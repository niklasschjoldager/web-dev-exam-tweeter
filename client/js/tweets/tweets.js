import { prepareTweet } from "./global.js"

export default function setupTweetsActions(target) {
  const tweets = document.querySelectorAll(target)
  tweets.forEach(prepareTweet)
}
