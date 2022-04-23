import handleDeleteTweet from "./deleteTweet.js"
import handleEditTweet from "./editTweet.js"
import handleLikeTweet from "./likeTweet.js"
import handleUnlikeTweet from "./unlikeTweet.js"
import handleFollowUser from "../users/followUser.js"
import handleUnfollowUser from "../users/unfollowUser.js"
import { handleAddImage, handleRemoveImage } from "../utils.js"

export function displayTweet(tweet) {
  const {
    tweet_id: id,
    tweet_image_file_name: imageFileName,
    tweet_text: text,
    user_username: username,
    user_name: name,
    user_profile_image: profileImage,
  } = tweet

  const hook = document.querySelector("[data-hook=tweets]")

  if (!hook) return
  const template = document.querySelector("[data-template=tweet-item]").content.cloneNode(true)
  const form = template.querySelector("[data-form=tweet]")
  template.querySelector("[data-form=tweet]").setAttribute("data-id", id)
  template.querySelector("[data-field=text]").textContent = text
  template.querySelector("[data-field=username]").href = `/users/${username}`
  template.querySelector("[data-field=username]").textContent = `@${username}`
  template.querySelector("[data-field=name-link]").href = `/users/${username}`
  template.querySelector("[data-field=name]").textContent = name
  if (profileImage) {
    template.querySelector("[data-field=profile-image]").src = `/static/users/${profileImage}`
  } else {
    template.querySelector("[data-field=profile-image]").src = "/static/images/default-profile-image.png"
  }

  if (imageFileName) {
    template.querySelector("[data-field=image]").src = `static/tweets/${imageFileName}`
    template.querySelector("[data-field=image]").classList.remove("is-hidden")
  } else {
    template.querySelector("[data-field=image]").src = "#"
    template.querySelector("[data-field=image]").classList.add("is-hidden")
  }

  prepareTweet(form)
  hook.prepend(template)
}

export function prepareTweet(tweet) {
  const userId = tweet.dataset.userId
  const username = tweet.dataset.username
  const tweetId = tweet.dataset.id

  const deleteButton = tweet.querySelector("[data-button=delete]")
  const editButton = tweet.querySelector("[data-button=edit]")
  const likeButton = tweet.querySelector("[data-button=like]")
  const unlikeButton = tweet.querySelector("[data-button=unlike]")
  const followButton = tweet.querySelector("[data-button=follow]")
  const unfollowButton = tweet.querySelector("[data-button=unfollow]")

  deleteButton && deleteButton.addEventListener("click", () => handleDeleteTweet(tweetId, tweet))
  editButton && editButton.addEventListener("click", () => handleEditTweet(tweetId, tweet))
  likeButton && likeButton.addEventListener("click", () => handleLikeTweet(tweetId, tweet))
  unlikeButton && unlikeButton.addEventListener("click", () => handleUnlikeTweet(tweetId, tweet))
  followButton && followButton.addEventListener("click", () => handleFollowUser(userId))
  unfollowButton && unfollowButton.addEventListener("click", () => handleUnfollowUser(userId, username))
}

export function prepareActions(modal) {
  const buttonAddImage = modal.querySelector("[data-action=add-image]")
  const buttonRemoveImage = modal.querySelector("[data-action=remove-image]")
  const inputTweetImage = modal.querySelector("[data-hook=input-tweet-image")
  const tweetImageContainer = modal.querySelector("[data-hook=tweet-image-container]")
  const tweetImage = modal.querySelector("[data-hook=tweet-image]")
  inputTweetImage.addEventListener("change", () => handleAddImage(inputTweetImage, tweetImage, tweetImageContainer))
  buttonAddImage.addEventListener("click", () => inputTweetImage.click())
  buttonRemoveImage.addEventListener("click", () => handleRemoveImage(inputTweetImage, tweetImage, tweetImageContainer))
}

export function resetForm(form) {
  const tweetImageContainer = form.querySelector("[data-hook=tweet-image-container]")
  const tweetImage = form.querySelector("[data-hook=tweet-image]")
  tweetImageContainer.classList.add("is-hidden")
  tweetImage.src = ""

  form.reset()
  form.elements["tweet_text"].style.height = ""

  const isModal = form.closest("[data-modal]")

  if (isModal) {
    document.body.classList.remove("modal-is-open")
    isModal.classList.add("is-hidden")
  }
}
