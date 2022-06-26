import coverImage from "../assets/frontpage-cover.jpg"
import Button from "../components/Button"
import Link from "../components/Link"

export default function Index() {
  return (
    <>
      <main className="flex-grow mt-6 md:mt-0 md:flex md:flex-row-reverse">
        <div className="flex-grow flex flex-col items-start max-w-xl px-8 mx-auto mb-10 md:max-w-none md:my-auto lg:min-w-[45vw] lg:w-2/5">
          <div className="pt-8 md:pt-0 pb-14">
            <svg className="w-12 h-12 fill-primary-200" viewBox="0 0 24 24" aria-hidden="true">
              <g>
                <path d="M23.643 4.937c-.835.37-1.732.62-2.675.733.962-.576 1.7-1.49 2.048-2.578-.9.534-1.897.922-2.958 1.13-.85-.904-2.06-1.47-3.4-1.47-2.572 0-4.658 2.086-4.658 4.66 0 .364.042.718.12 1.06-3.873-.195-7.304-2.05-9.602-4.868-.4.69-.63 1.49-.63 2.342 0 1.616.823 3.043 2.072 3.878-.764-.025-1.482-.234-2.11-.583v.06c0 2.257 1.605 4.14 3.737 4.568-.392.106-.803.162-1.227.162-.3 0-.593-.028-.877-.082.593 1.85 2.313 3.198 4.352 3.234-1.595 1.25-3.604 1.995-5.786 1.995-.376 0-.747-.022-1.112-.065 2.062 1.323 4.51 2.093 7.14 2.093 8.57 0 13.255-7.098 13.255-13.254 0-.2-.005-.402-.014-.602.91-.658 1.7-1.477 2.323-2.41z"></path>
              </g>
            </svg>
          </div>
          <h1 className="mb-12 font-bold text-7xl">Happening now</h1>
          <h2 className="mb-10 text-4xl font-bold">Join Tweeter today.</h2>
          <Button variant="primary" className="mb-2 w-80">
            Sign up with phone or email
          </Button>
          <p className="mb-12 text-xs w-80">
            By signing up, you agree to the <Link to="#">Terms of Service</Link> and <Link to="#">Privacy Policy</Link>,
            including <Link to="#">Cookie Use.</Link>
          </p>
          <h3 className="mb-6 font-bold">Already have an account?</h3>
          <Button variant="primary-outlined" className="w-80">
            Sign in
          </Button>
        </div>

        <div>
          <img className="object-cover w-full min-h-[46vh] xs:min-h-0 h-full" src={coverImage} alt="#" />
        </div>
      </main>

      <footer className="p-3">
        <nav aria-label="Footer" role="navigation">
          <ul className="flex flex-wrap justify-center gap-x-3">
            {/* {% for link in footer_links %}
                  <li>
                    <a className="text-xs text-gray-400 hover:underline" href="#">{{ link }}</a>
                  </li>
                {% endfor %} */}
          </ul>
        </nav>
      </footer>
    </>
  )
}
