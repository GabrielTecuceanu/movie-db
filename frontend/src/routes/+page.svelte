<script>
  import { onMount } from "svelte";
  import { cubicInOut } from "svelte/easing";
  import {
    apiKey,
    imgBaseUrl,
    imgOriginal,
    topGradientSoftness,
    bottomGradientSoftness,
    getMovieGenres,
    getTVGenres,
    redirectTo,
  } from "$lib/utils";
  import { fade } from "svelte/transition";
  import { Badge } from "$lib/components/ui/badge/index.js";
  import { ScrollArea } from "$lib/components/ui/scroll-area/index";
  import * as Table from "$lib/components/ui/table";
  import * as Tooltip from "$lib/components/ui/tooltip";

  const displayCount = 7;
  let films = null;
  let displayFilms = null;
  let shows = null;
  let displayShows = null;
  let people = null;
  let displayPeople = null;
  let currentIndex = 0;

  let mostPopularFilm = null;
  let primaryImageUrl = null;

  let primaryImageSize = 50;
  let windowHeight;
  let windowWidth;
  const updateWindowSize = () => {
    windowHeight = window.innerHeight;
    windowWidth = window.innerWidth;
  };

  function cycleFilm() {
    currentIndex = (currentIndex + 1) % films.length;
    mostPopularFilm = films[currentIndex];
    primaryImageUrl = mostPopularFilm.backdropUrl;
  }

  let mediaGenres = new Map();
  let interval;
  onMount(async () => {
    updateWindowSize();
    window.addEventListener("resize", updateWindowSize);

    let movieGenresArray = await getMovieGenres();
    let tvGenresArray = await getTVGenres();
    movieGenresArray.forEach((element) => {
      mediaGenres.set(element.id, element.name);
    });
    tvGenresArray.forEach((element) => {
      mediaGenres.set(element.id, element.name);
    });

    fetch(`${apiKey}/movie/popular/1`)
      .then((response) => {
        if (!response.ok)
          throw new Error(`Could not get popular movies: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        films = data.results
          .filter(
            (film) => film.backdrop_path !== null && film.poster_path !== null,
          )
          .map((film) => {
            return {
              ...film,
              backdropUrl: `${imgBaseUrl}/${imgOriginal}${film.backdrop_path}`,
              posterUrl: `${imgBaseUrl}/${imgOriginal}${film.poster_path}`,
              genre_ids:
                film.genre_ids !== null
                  ? film.genre_ids.map((genre) => mediaGenres.get(genre))
                  : null,
            };
          });
        primaryImageUrl = films[currentIndex].backdropUrl;
        mostPopularFilm = films[currentIndex];
        displayFilms = films.slice(0, displayCount);
      })
      .catch((error) => {
        console.log("Error fetching data:", error.message);
      });

    interval = setInterval(cycleFilm, 8000);

    fetch(`${apiKey}/tv/popular/1`)
      .then((response) => {
        if (!response.ok)
          throw new Error(`Could not get popular shows: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        shows = data.results
          .filter((show) => show.poster_path !== null)
          .map((show) => {
            return {
              ...show,
              posterUrl: `${imgBaseUrl}/${imgOriginal}${show.poster_path}`,
              genre_ids: show.genre_ids.map((genre) => mediaGenres.get(genre)),
            };
          });
        displayShows = shows.slice(0, displayCount);
      })
      .catch((error) => {
        console.log("Error fetching data:", error.message);
      });

    fetch(`${apiKey}/person/popular`)
      .then((response) => {
        if (!response.ok)
          throw new Error(`Could not get popular people: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        people = data.results.map((person) => {
          return {
            ...person,
            posterUrl: `${imgBaseUrl}/${imgOriginal}${person.profile_path}`,
          };
        });
        displayPeople = people.slice(0, displayCount);
      })
      .catch((error) => {
        console.log("Error fetching data:", error.message);
      });

    return () => {
      window.removeEventListener("resize", updateWindowSize);
    };
  });
</script>

{#if mostPopularFilm != null}
  {#key mostPopularFilm}
    <div
      class="absolute grid top-0 left-0 w-full h-fit bg-cover bg-center bg-no-repeat"
      style="height: {primaryImageSize}rem;
         font-family: 'Open Sans';
         background-image: url('{primaryImageUrl}');"
      transition:fade={{
        duration: 500,
        easing: cubicInOut,
      }}
    >
      <div
        class="absolute w-full bg-easing-b-smooth_fade"
        style="bottom: 0rem;
    height: {bottomGradientSoftness * primaryImageSize}rem;"
      ></div>

      <div
        class="absolute left-0 top-0 bg-gradient-to-r from-rich_black to-rich_black/0 w-1/3"
        style="height: {primaryImageSize}rem;"
      ></div>

      <div
        class="absolute right-0 top-0 bg-gradient-to-l from-rich_black to-rich_black/0 w-1/3"
        style="height: {primaryImageSize}rem;"
      ></div>
    </div>
  {/key}

  <div
    class="relative left-[15vw] drop-shadow-lg w-1/3 flex flex-col bottom-0"
    style="height: 45rem;"
  >
    <a
      class=" text-xl sm:text-2xl md:text-4xl lg:text-6xl"
      style="font-weight: 700;
                 margin-top: {45}vh;"
      href="/movie/{mostPopularFilm.id}"
      target="_blank"
    >
      {mostPopularFilm.original_title}
    </a>
    <p
      class="relative text-ellipsis line-clamp-4 text-justify
          w-fit mt-2
          text-sm sm:text-base md:text-lg lg:text-xl"
      style="font-weight: 400;"
    >
      {mostPopularFilm.overview}
    </p>
  </div>
{/if}

<div class="relative flex flex-col mx-[15vw]">
  {#if films !== null && films.length > 0}
    <h1
      class="w-fit h-fit mb-3 sm:text-xl md:text-2xl lg:text-4xl"
      style="font-family: 'Open Sans';
             font-weight: 600;"
    >
      No big screen can tame these films:
    </h1>
    <div class="flex flex-row overflow-hidden mb-[4vh]">
      {#each displayFilms as film}
        <Tooltip.Root>
          <Tooltip.Trigger
            class="transition max-w-[8vw] mr-auto rounded-sm border-2 border-transparent hover:border-munsell_blue"
          >
            <button
              on:click={() => {
                redirectTo(`/movie/${film.id}`);
              }}
              class="h-full w-full"
            >
              <img src={film.posterUrl} alt={film.name} class="h-full w-full" />
            </button>
          </Tooltip.Trigger>
          <Tooltip.Content>
            <p>{film.title}</p>
          </Tooltip.Content>
        </Tooltip.Root>
      {/each}
    </div>
  {/if}

  {#if shows !== null && shows.length > 0}
    <h1
      class="w-fit h-fit mb-3 sm:text-xl md:text-2xl lg:text-4xl"
      style="font-family: 'Open Sans';
         font-weight: 600;"
    >
      What to watch on TV:
    </h1>
    <div class="flex flex-row overflow-hidden mb-[4vh]">
      {#each displayShows as show}
        <Tooltip.Root>
          <Tooltip.Trigger
            class="transition max-w-[8vw] mr-auto rounded-sm border-2 border-transparent hover:border-uranium_blue"
          >
            <button
              on:click={() => {
                redirectTo(`/tv/${show.id}`);
              }}
              class="h-full w-full"
            >
              <img class="h-full w-full" src={show.posterUrl} alt={show.name} />
            </button>
          </Tooltip.Trigger>
          <Tooltip.Content>
            <p>{show.name}</p>
          </Tooltip.Content>
        </Tooltip.Root>
      {/each}
    </div>
  {/if}

  {#if people !== null && people.length > 0}
    <h1
      class="w-fit h-fit mb-3 sm:text-xl md:text-2xl lg:text-4xl"
      style="font-family: 'Open Sans';
     font-weight: 600;"
    >
      These people are the town's talk:
    </h1>
    <div class="flex flex-row overflow-hidden mb-[4vh]">
      {#each displayPeople as people}
        <Tooltip.Root>
          <Tooltip.Trigger
            class="transition max-w-[8vw] mr-auto rounded-sm border-2 border-transparent hover:border-uranium_blue"
          >
            <button
              on:click={() => {
                redirectTo(`/person/${people.id}`);
              }}
              class="h-full w-full"
            >
              <img
                class="h-full w-full"
                src={people.posterUrl}
                alt={people.name}
              />
            </button>
          </Tooltip.Trigger>
          <Tooltip.Content>
            <p>{people.name}</p>
          </Tooltip.Content>
        </Tooltip.Root>
      {/each}
    </div>
  {/if}
</div>
