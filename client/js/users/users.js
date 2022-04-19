import { prepareUser } from "./global.js"

export default function setupUserActions(target) {
  const users = document.querySelectorAll(target)
  users.forEach(prepareUser)
}
