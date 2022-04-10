const elements = document.querySelectorAll("[data-target][data-action]")
let currentElement = null

elements.forEach((element) => {
  const { target, action } = element.dataset
  if (!target || !action) return
  const targetElement = document.querySelector(`[data-modal=${target}]`)

  element.addEventListener("click", () => {
    if (currentElement && currentElement !== targetElement) currentElement.classList.add("is-hidden")
    currentElement = targetElement

    switch (action) {
      case "toggle":
        if (targetElement.classList.contains("is-hidden")) {
          document.body.classList.add("modal-is-open")
        } else {
          document.body.classList.remove("modal-is-open")
        }
        targetElement.classList.toggle("is-hidden")
        break
      case "open":
        targetElement.classList.remove("is-hidden")
        document.body.classList.add("modal-is-open")
        break
      case "close":
        targetElement.classList.add("is-hidden")
        document.body.classList.remove("modal-is-open")
        break
      default:
        console.log("Action does not exist.")
        return
    }
  })
})

const formUserLogin = document.querySelector("[data-form=user-login]")
const formUserSignup = document.querySelector("[data-form=user-signup]")

formUserLogin.addEventListener("submit", handleLogin)
formUserSignup.addEventListener("submit", handleCreateAccount)

async function handleLogin(event) {
  event.preventDefault()

  const request = await fetch("/login", {
    method: "POST",
    body: new FormData(formUserLogin),
  })

  const response = await request

  if (!response.ok) console.log(await response.json())
  if (response.redirected) window.location.href = response.url
}

async function handleCreateAccount(event) {
  event.preventDefault()

  const request = await fetch("/users", {
    method: "POST",
    body: new FormData(formUserSignup),
  })

  const response = await request

  console.log(response)
  if (!response.ok) {
    console.log(await response.json())
    return
  }
  window.location.href = "/home"
}
