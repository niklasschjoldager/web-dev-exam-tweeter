import Button from "../components/Button"
import defaultProfileImage from "../assets/default-profile-image.png"
import Header from "../components/Header"

export default function Home() {
  return (
    <div className="flex-grow w-full h-full mx-auto lg:px-4 sm:flex sm:justify-center lg:w-full xl:max-w-7xl isolate">
      <div className="isolate hidden minHminW:block min-w-[69px] md:min-w-[89px] xl:min-w-[275px] h-screen sticky z-10 left-0 top-0">
        <Header />
      </div>
      <main className="isolate sm:max-w-[600px] w-full min-w-0 pb-44 minHminW:pb-4 sm:border-l sm:border-r sm:border-gray-200">
        <div className="sticky top-0 px-4 py-1 bg-white/[0.97] z-50 min-h-[56px] flex items-center">
          <div className="flex items-center justify-between w-full">
            <div className="flex gap-4">
              <button className="minHminW:hidden">
                <img className="object-cover w-8 h-8 rounded-full" src={defaultProfileImage} alt="#" />
              </button>
              <h1 className="text-lg font-bold">Home</h1>
            </div>
            <div className="flex gap-4">
              {/* {{ iconButton(text="Latest tweets", color="black-200", icon='<svg className="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>Sparkles</title><path d="M259.92 262.91L216.4 149.77a9 9 0 00-16.8 0l-43.52 113.14a9 9 0 01-5.17 5.17L37.77 311.6a9 9 0 000 16.8l113.14 43.52a9 9 0 015.17 5.17l43.52 113.14a9 9 0 0016.8 0l43.52-113.14a9 9 0 015.17-5.17l113.14-43.52a9 9 0 000-16.8l-113.14-43.52a9 9 0 01-5.17-5.17zM108 68L88 16 68 68 16 88l52 20 20 52 20-52 52-20-52-20zM426.67 117.33L400 48l-26.67 69.33L304 144l69.33 26.67L400 240l26.67-69.33L496 144l-69.33-26.67z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"/></svg>') }} */}
            </div>
          </div>
        </div>

        <section>
          <div className="max-w-sm p-8 mx-auto">
            <h2 className="mb-2 text-3xl font-black">Welcome to your timeline!</h2>
            <p className="mb-8 text-sm text-gray-400">
              This is the best place to see what’s happening on Tweeter for you. The more people and interests you
              follow, the better your timeline becomes. We have some suggestions to help you get started.
            </p>
            <Button variant="primary" size="lg">
              Let's go
            </Button>
          </div>
        </section>
      </main>
      <div className="isolate hidden w-auto grow lg:block xl:w-full max-w-[400px]">
        <aside className="flex flex-col items-center w-full h-full gap-8 py-4 pl-8">
          {/* Sidebar component */}
          <div className="w-full overflow-hidden bg-gray-100 border border-gray-200 rounded-2xl">
            <h2 className="px-4 pt-3 mb-3 text-xl font-bold">Who to follow</h2>

            {/* {% for user in who_to_follow %}
                  {{ userItem(logged_in_user_id=logged_in_user["id"], **user) }}
                {% endfor %} */}
            <a
              className="flex w-full px-4 py-3 text-sm transition-colors text-primary-200 hover:bg-black-200/5 focus:bg-black-200-5 "
              href="#"
            >
              Show more
            </a>
          </div>
          {/* Sidebar component end */}
        </aside>
      </div>

      {/* Mobile navigation component */}
      <div className="fixed bottom-0 left-0 right-0 flex flex-col drop-shadow-md minHminW:hidden">
        <div className="px-4 bg-white border-t border-gray-200">
          <nav className="max-w-[600px] lg:max-w-[1000px] mx-auto flex w-full relative">
            <button
              className="absolute right-0 flex items-center justify-center gap-2 font-bold text-white transition-colors rounded-full shadow-lg -top-20 w-14 h-14 lg:w-auto lg:px-8 bg-primary-200 hover:bg-primary-100 focus:bg-primary-100"
              type="button"
            >
              <svg
                className="w-7 h-7"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                />
              </svg>
              <span className="sr-only lg:not-sr-only">Tweet</span>
            </button>

            {/* {% for link in mobile_navigation %}
                  <a className="flex items-center justify-center flex-grow gap-4 p-3 group" href="/{{ link['url'] }}">
                    {% set iconText = link['url'] %}
                    {% if link["url"] == currentUrl %}
                      {% set iconImage = '<img className="w-7 h-7" src="/static/icons/' + link['icons']['active']  + '" alt="' + link['name'] + ' icon"/>' %}
                      {{ iconButton(text=iconText, icon=iconImage, color="black-200") }}
                    {% else %}
                      {% set iconImage = '<img className="w-7 h-7" src="/static/icons/' + link['icons']['default']  + '" alt="' + link['name'] + ' icon"/>' %}
                      {{ iconButton(text=iconText, icon=iconImage, color="black-200") }}
                    {% endif %}
                    <span className="sr-only">{{ link["name"] }}</span>
                  </a>
                {% endfor %} */}
          </nav>
        </div>
      </div>
      {/* Mobile navigation component end */}
    </div>
  )
}
