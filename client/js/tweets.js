import Modal from "./classes/modal.js"

const DROPDOWN_BUTTON = "[data-dropdown-button]"
const DROPDOWN_CONTAINER = "[data-dropdown-container]"
const DROPDOWN = "[data-dropdown]"
const BUTTON_VALUES = [
  {
    name: "edit",
    callback: showEditModal,
  },
  {
    name: "delete",
    callback: showDeleteModal,
  },
  {
    name: "like",
    callback: likeTweet,
  },
  {
    name: "unlike",
    callback: unlikeTweet,
  },
  {
    name: "comment",
    callback: showCommentModal,
  },
  {
    name: "retweet",
    callback: toggleRetweet,
  },
  {
    name: "share",
    callback: showShareModal,
  },
]

let isDropdownOpen = false

document.addEventListener("click", handleClick)
setupEditTweetModal()

function setupEditTweetModal() {
  const modal = document.querySelector("[data-modal=edit-tweet]")
  const buttonAddImage = modal.querySelector("[data-action=add-image]")
  const buttonRemoveImage = modal.querySelector("[data-action=remove-image]")
  const inputAddImage = modal.querySelector("[data-hook=input-tweet-image")
  const tweetImageContainer = modal.querySelector("[data-hook=tweet-image-container]")
  const tweetImage = modal.querySelector("[data-hook=tweet-image]")
  inputAddImage.addEventListener("change", () => handleTweetAddImage(inputAddImage, tweetImage, tweetImageContainer))
  buttonAddImage.addEventListener("click", () => inputAddImage.click())
  buttonRemoveImage.addEventListener("click", () =>
    handleTweetRemoveImage(inputAddImage, tweetImage, tweetImageContainer)
  )
}

function handleClick(event) {
  const target = event.target

  if (isDropdownOpen) {
    isDropdownOpen = false
    closeAllDropdowns(DROPDOWN)
  }

  if (!target.closest("[data-form=tweet]")) return

  BUTTON_VALUES.forEach(({ name, callback }) => {
    const selector = `[data-button=${name}]`
    if (target.matches(selector) || target.closest(selector)) {
      const tweetId = target.closest("[data-form=tweet]").dataset.id
      callback(tweetId)
    }
  })

  if (target.matches(DROPDOWN_BUTTON) || target.closest(DROPDOWN_BUTTON)) {
    event.preventDefault()
    const dropdown = target.closest(DROPDOWN_CONTAINER).querySelector(DROPDOWN)
    isDropdownOpen = true
    openDropdown(dropdown)
  }
}

function closeAllDropdowns(dropdownIdentifier) {
  document.querySelectorAll(dropdownIdentifier).forEach((dropdown) => dropdown.classList.add("is-hidden"))
}

function openDropdown(dropdown) {
  dropdown.classList.remove("is-hidden")
}

function showEditModal(id) {
  const modalEditTweet = new Modal("[data-modal=edit-tweet]", null, () => requestEditTweet(id, modalEditTweet))
  const tweetForm = document.querySelector(`[data-form="tweet"][data-id="${id}"]`)
  const tweetText = tweetForm.querySelector("[data-field=text").textContent
  const tweetImage = tweetForm.querySelector("[data-field=image")
  modalEditTweet.openModal()

  const inputText = modalEditTweet.modal.querySelector("[data-hook=tweet-text]")
  const inputImage = modalEditTweet.modal.querySelector("[data-hook=input-tweet-image]")
  const image = modalEditTweet.modal.querySelector("[data-hook=tweet-image]")
  const imageContainer = modalEditTweet.modal.querySelector("[data-hook=tweet-image-container]")
  image.src = tweetImage.src
  if (!tweetImage.classList.contains("is-hidden")) {
    // inputImage.files[0] = tweetImage
    imageContainer.classList.remove("is-hidden")
  }
  inputText.value = tweetText
  inputText.style.height = ""
  inputText.style.height = `${inputText.scrollHeight}px`
}

function showDeleteModal(id) {
  const modalDeleteTweet = new Modal("[data-modal=delete-tweet]", null, () => requestDeleteTweet(id, modalDeleteTweet))
  modalDeleteTweet.openModal()
}

function showCommentModal() {
  console.log("showCommentModal")
}

function showShareModal() {
  console.log("showShareModal")
}

function toggleRetweet() {
  console.log("toggleRetweet")
}

async function unlikeTweet(id) {
  const target = event.target
  const request = await fetch(`/tweets/${id}/unlike`, {
    method: "DELETE",
  })

  const response = await request

  if (!response.ok) return alert("Could not unlike tweet")

  const unlikeButton = target.closest("button")
  const unlikeCounter = unlikeButton.querySelector("[data-field=unlike-counter]")
  const likeButton = target.closest("form").querySelector("[data-button=like")
  const likeCounter = likeButton.querySelector("[data-field=like-counter]")
  const currentLikes = Number(likeCounter.textContent)

  if (currentLikes - 1) {
    unlikeCounter.textContent = currentLikes - 1
    likeCounter.textContent = currentLikes - 1
  } else {
    unlikeCounter.textContent = ""
    likeCounter.textContent = ""
  }

  likeButton.classList.remove("is-hidden")
  unlikeButton.classList.add("is-hidden")
}

async function likeTweet(id) {
  const target = event.target
  const request = await fetch(`/tweets/${id}/like`, {
    method: "POST",
  })

  const response = await request

  if (!response.ok) return alert("Could not like tweet")

  const unlikeButton = target.closest("form").querySelector("[data-button=unlike")
  const unlikeCounter = unlikeButton.querySelector("[data-field=unlike-counter]")
  const likeButton = target.closest("button")
  const likeCounter = likeButton.querySelector("[data-field=like-counter]")
  likeCounter.textContent = Number(likeCounter.textContent) + 1
  unlikeCounter.textContent = Number(unlikeCounter.textContent) + 1
  likeButton.classList.add("is-hidden")
  unlikeButton.classList.remove("is-hidden")
}

async function requestDeleteTweet(id, modal) {
  const request = await fetch(`/tweets/${id}`, {
    method: "DELETE",
  })

  const response = await request

  if (!response.ok) return alert("Could not delete tweet")

  document.querySelector(`[data-form="tweet"][data-id="${id}"]`).remove()
  modal.closeModal()
}

async function requestEditTweet(id, modal) {
  event.preventDefault()
  const form = modal.modal.querySelector("[data-form=edit-tweet]")
  const formData = new FormData(form)

  if (form.querySelector("[data-hook=tweet-image-container]").classList.contains("is-hidden")) {
    formData.set("tweet_image", null)
  }

  const request = await fetch(`/tweets/${id}`, {
    method: "PUT",
    body: formData,
  })

  const response = await request

  if (!response.ok) return alert("Could not edit tweet")
  const data = await response.json()

  const tweet = document.querySelector(`[data-form="tweet"][data-id="${id}"]`)
  tweet.querySelector("[data-field=text]").textContent = formData.get("tweet_text")
  if (data["tweet_image_file_name"]) {
    tweet.querySelector("[data-field=image]").src = `/static/tweets/${data["tweet_image_file_name"]}`
    tweet.querySelector("[data-field=image]").classList.remove("is-hidden")
  } else {
    tweet.querySelector("[data-field=image]").src = "#"
    tweet.querySelector("[data-field=image]").classList.add("is-hidden")
  }

  modal.closeModal()
}

export function handleTweetAddImage(imageInput, image, imageContainer) {
  const selectedFile = imageInput.files[0]

  if (!selectedFile) return imageContainer.classList.add("is-hidden")

  image.src = URL.createObjectURL(selectedFile)
  imageContainer.classList.remove("is-hidden")
}

export function handleTweetRemoveImage(imageInput, image, imageContainer) {
  image.src = ""
  imageContainer.classList.add("is-hidden")
}
