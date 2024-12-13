<script lang="ts">
    import {
        apiKey,
        imgBaseUrl,
        imgSizeSmall,
        redirectTo,
        getMovieGenres,
        getTVGenres,
        getCookie,
        topGradientSoftness,
        fetchUsername,
    } from "$lib/utils";
    import { onMount } from "svelte";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Button } from "$lib/components/ui/button/index.js";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index";
    import { Separator } from "$lib/components/ui/separator";
    import { Auth } from "$lib/components/auth/index";
    import Cookies from "js-cookie";

    import Search from "lucide-svelte/icons/search";

    let { showGradient = true } = $props();

    let searchQuery = $state("");
    let timeout;
    let searchResult = $state([]);
    let showResults = $state(false);
    let mediaGenres = new Map();

    function handleInputChange(event) {
        clearTimeout(timeout);

        timeout = setTimeout(async () => {
            if (searchQuery.trim()) {
                try {
                    const response = await fetch(
                        `${apiKey}/search/multi/${searchQuery}/1`,
                    );

                    if (!response.ok) {
                        throw new Error(
                            `Could not get query: ${response.status}`,
                        );
                    }

                    const data = await response.json();
                    searchResult = data.results.map((element) => {
                        let name = null;
                        let imageUrl = `${imgBaseUrl}/${imgSizeSmall}`;
                        let releaseDate = null;
                        let genres = [];
                        switch (element.media_type) {
                            case "movie":
                                name = element.title;
                                releaseDate = element.release_date;
                                if (element.poster_path === null) {
                                    imageUrl = null;
                                } else {
                                    imageUrl = `${imageUrl}/${element.poster_path}`;
                                }
                                genres = element.genre_ids;
                                break;
                            case "tv":
                                name = element.name;
                                releaseDate = element.first_air_date;
                                if (element.poster_path === null) {
                                    imageUrl = null;
                                } else {
                                    imageUrl = `${imageUrl}/${element.poster_path}`;
                                }
                                genres = element.genre_ids;
                                break;
                            case "person":
                                name = element.name;
                                if (element.profile_path === null) {
                                    imageUrl = null;
                                } else {
                                    imageUrl = `${imageUrl}/${element.profile_path}`;
                                }
                                break;
                            default:
                                imageUrl = null;
                                break;
                        }
                        return {
                            name: name,
                            imageUrl: imageUrl,
                            releaseDate: releaseDate,
                            type: element.media_type,
                            genres: genres.map((id) => mediaGenres.get(id)),
                            id: element.id,
                        };
                    });
                } catch (e) {
                    console.log(e);
                }
            } else {
                searchResult = [];
            }
        }, 1000);
    }

    let loading = $state(true);
    let isLoggedIn = $state(false);
    let username = $state(null);
    const token = Cookies.get("token");
    if (token) isLoggedIn = true;

    let authPanel: Auth = $state();
    let showAuth = $state(false);
    function openAuth() {
        showAuth = true;
        authPanel.open();
    }

    let searchBar = $state(null);
    // @ts-ignore
    onMount(async () => {
        let movieGenresArray;
        getMovieGenres().then((result) => {
            movieGenresArray = result;
            movieGenresArray.forEach((element) => {
                mediaGenres.set(element.id, element.name);
            });
        });
        let tvGenresArray;
        getTVGenres().then((result) => {
            tvGenresArray = result;
            tvGenresArray.forEach((element) => {
                mediaGenres.set(element.id, element.name);
            });
        });

        document.addEventListener("click", (event) => {
            if (searchBar && !searchBar.contains(event.target))
                showResults = false;
        });

        if (getCookie("token") !== null) {
            isLoggedIn = true;
            fetchUsername(token).then((result) => {
                username = result;
            });
        }

        loading = false;
        return () => {};
    });
</script>

{#if !loading}
    <header
        class="relative z-10 w-full mx-auto px-10 pt-8 z-30 flex items-start"
    >
        {#if showGradient}
            <div
                class="absolute top-[0vh] left-0 bg-easing-t-smooth_fade w-full pointer-events-none"
                style="height: {topGradientSoftness * 10}px"
            ></div>
        {/if}

        <div class="relative top-0 mx-auto text-left">
            <a
                href="/"
                style="font-family: 'Open Sans';
        font-weight: 700;">Taped</a
            >
        </div>

        <div bind:this={searchBar} class="relative flex-1 grow-0">
            <Search class="absolute left-2.5 top-2.5 h-4 w-4" />
            <Input
                type="search"
                class="transition text-white border-none bg-background/5 focus:bg-background/40 w-full rounded-lg pl-8
            w-[35vw]"
                bind:value={searchQuery}
                on:input={handleInputChange}
                on:focus={() => (showResults = true)}
            />

            {#if showResults && searchResult.length > 0}
                <ScrollArea
                    class="absolute w-full left-0 select-none rounded-md backdrop-blur-lg flex max-h-72 flex-col overflow-y-auto"
                    style="font-family: 'Open Sans';"
                >
                    {#each searchResult as result}
                        <div
                            tabindex="0"
                            role="button"
                            class="cursor-pointer transition-all flex flex-row p-3 bg-rich_black/70 hover:bg-rich_black/40 text-white"
                            onclick={() =>
                                redirectTo(`/${result.type}/${result.id}`)}
                            onkeydown={(event) => {
                                if (event.key === "Enter") {
                                    redirectTo(`/${result.type}/${result.id}`);
                                }
                            }}
                        >
                            {#if result.imageUrl === null}
                                <div
                                    style="width: 64px;
                                height: 96px"
                                >
                                    {#if result.media_type === "person"}
                                        <svg
                                            class="relative m-auto w-full h-full"
                                            aria-hidden="true"
                                            xmlns="http://www.w3.org/2000/svg"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                        >
                                            <path
                                                stroke="currentColor"
                                                stroke-width="1"
                                                d="M7 17v1a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1a3 3 0 0 0-3-3h-4a3 3 0 0 0-3 3Zm8-9a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                                            />
                                        </svg>
                                    {:else}
                                        <svg
                                            class="relative m-auto w-full h-full text-white"
                                            aria-hidden="true"
                                            xmlns="http://www.w3.org/2000/svg"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                        >
                                            <path
                                                stroke="currentColor"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="1"
                                                d="M14 6H4a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1Zm7 11-6-2V9l6-2v10Z"
                                            />
                                        </svg>
                                    {/if}
                                </div>
                            {:else}
                                <img
                                    class="object-scale-down"
                                    src={result.imageUrl}
                                    alt={result.name}
                                    style="width: 64px;
                                height: 96px"
                                />
                            {/if}
                            <div class="w-full px-4 my-auto flex flex-col">
                                <p style="font-weight: 700;">
                                    {result.name}
                                </p>
                                {#if result.genres !== null && result.genres.length > 0}
                                    <div class="flex flex-row w-fit">
                                        {#each result.genres as genre}
                                            <Badge
                                                class="text-white mr-1"
                                                variant="outline">{genre}</Badge
                                            >
                                        {/each}
                                    </div>
                                {/if}
                                <p style="font-weight: 400;">
                                    {result.releaseDate}
                                </p>
                            </div>
                        </div>
                        <Separator class="opacity-10" />
                    {/each}
                </ScrollArea>
            {/if}
        </div>

        <div class="relative top-0 mx-auto">
            <DropdownMenu.Root preventScroll={false}>
                <DropdownMenu.Trigger asChild let:builder>
                    <Button
                        builders={[builder]}
                        size="icon"
                        class="transition-colors overflow-hidden rounded-full bg-transparent border-2 border-transparent hover:border-white"
                    >
                        <svg
                            class="w-6 h-6 text-white"
                            aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg"
                            width="24"
                            height="24"
                            fill="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                fill-rule="evenodd"
                                d="M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4h-4Z"
                                clip-rule="evenodd"
                            />
                        </svg>
                    </Button>
                </DropdownMenu.Trigger>
                <DropdownMenu.Content
                    align="end"
                    class="bg-transparent text-white border-0 backdrop-blur-lg"
                >
                    {#if isLoggedIn == true}
                        <DropdownMenu.Item
                            on:click={() => {
                                redirectTo(`/profile/${username}`);
                            }}>My Account</DropdownMenu.Item
                        >
                        <DropdownMenu.Separator />
                        <DropdownMenu.Item
                            on:click={() => {
                                Cookies.remove("token");
                                window.location.reload();
                            }}>Logout</DropdownMenu.Item
                        >
                    {:else}
                        <DropdownMenu.Item
                            on:click={() => {
                                authPanel.setLogin();
                                openAuth();
                            }}>Log in</DropdownMenu.Item
                        >
                        <DropdownMenu.Item
                            on:click={() => {
                                authPanel.setSignUp();
                                openAuth();
                            }}>Sign up</DropdownMenu.Item
                        >
                    {/if}
                </DropdownMenu.Content>
            </DropdownMenu.Root>
        </div>

        <div class={showAuth == false ? "hidden" : ""}>
            <Auth
                bind:this={authPanel}
                cancel={() => {
                    showAuth = false;
                }}
            ></Auth>
        </div>
    </header>
{/if}
