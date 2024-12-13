<script lang="ts">
    import { onMount } from "svelte";
    import { apiKey, imgBaseUrl, imgOriginal } from "$lib/utils";
    import { page } from "$app/stores";

    import CollapsibleText from "$lib/components/ui/collapsible-text/index";
    import ClickableStar from "$lib/components/ui/clickable-star/ClickableStar.svelte";
    import Showcase from "$lib/components/ui/showcase/Showcase.svelte";
    import Cookies from "js-cookie";

    let isLoggedIn = $state(false);
    const token = Cookies.get("token");
    if (token) isLoggedIn = true;

    const personID = $page.params.personID;
    let person = $state(null);
    let credits = $state(null);
    let images = $state(null);
    let recs = $state(null);

    async function fetchPersonDetails() {
        try {
            const response = await fetch(
                `${apiKey}/person/details/${personID}`,
            );
            if (!response.ok) {
                throw new Error(
                    `Could not get person details: ${response.status}`,
                );
            }

            const data = await response.json();
            person = {
                ...data,
                backdropUrl: `${imgBaseUrl}/${imgOriginal}${credits[0].backdrop_path}`,
                posterUrl: `${imgBaseUrl}/${imgOriginal}${data.profile_path}`,
            };
        } catch (e) {
            console.error(e);
        }
    }

    async function fetchPersonMedia() {
        try {
            const response = await fetch(`${apiKey}/person/${personID}/images`);
            if (!response.ok) {
                throw new Error(
                    `Could not get show images: ${response.status}`,
                );
            }

            const data = await response.json();
            images = data.profiles.map((url) => {
                return {
                    img: `${imgBaseUrl}/${imgOriginal}${url.file_path}`,
                    alt: `Image of ${person.name}`,
                    redirect: null,
                    tooltip: null,
                };
            });
            images.shift();
        } catch (e) {
            console.error(e);
        }
    }

    async function fetchPersonCredits() {
        try {
            const response = await fetch(
                `${apiKey}/person/${personID}/credits`,
            );
            if (!response.ok) {
                throw new Error(
                    `Could not get person movie credits: ${response.status}`,
                );
            }

            const result = await response.json();
            const creditsData = result;
            credits = creditsData.cast
                .filter((credit) => credit.poster_path !== null)
                .map((credit) => {
                    return {
                        ...credit,
                        img: `${imgBaseUrl}/${imgOriginal}${credit.poster_path}`,
                        tooltip: credit.original_title,
                        redirect: `/${credit.media_type}/${credit.id}`,
                    };
                });
        } catch (e) {
            console.error(e);
        }
    }

    let favourite: ClickableStar = $state();
    async function fetchIsFavouritePerson() {
        try {
            const response = await fetch(
                `${apiKey}/favourite/people/${personID}`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                },
            );
            const data = await response.json();
            if (!response.ok)
                throw new Error(
                    `Could not add person to favourite: ${response.status} ${response.statusText} => ${data.error}`,
                );

            if (data.success === true) favourite.toggleFill();
        } catch (e) {
            console.error(e);
        }
    }

    // @ts-ignore
    onMount(async () => {
        await fetchPersonCredits();
        await fetchPersonDetails();
        await fetchPersonMedia();
        if (isLoggedIn) fetchIsFavouritePerson();

        return () => {};
    });
</script>

{#if person !== null}
    <Showcase
        backdropUrl={person.backdropUrl}
        posterUrl={person.posterUrl}
        posterAlt={person.name}
        carousel1={images}
        carousel1Title={"Media"}
        carousel2={credits}
        carousel2Title={"Credited in"}
    >
        <div
            class="flex grow-1 flex-col space-y-2 lg:text-[100%] md:text-[90%] sm:text-[80%] text-[70%]"
        >
            <div class="flex flex-row flex-wrap place-items-center">
                <h1
                    class="text-[3em] text-nowrap flex-nowrap mr-4"
                    style="font-weight: 700"
                >
                    {person.name}
                </h1>
                <ClickableStar
                    bind:this={favourite}
                    additional={"Follow"}
                    additionalTextOnEnable={"Followed"}
                    enable={async () => {
                        try {
                            const response = await fetch(
                                `${apiKey}/favourite/people/add/${personID}`,
                                {
                                    method: "POST",
                                    headers: {
                                        "Content-Type": "application/json",
                                        Authorization: `Bearer ${token}`,
                                    },
                                },
                            );
                            if (!response.ok)
                                throw new Error(
                                    `Could not add person to favourite: ${response.status}`,
                                );
                        } catch (e) {
                            console.error(e);
                        }
                    }}
                    disable={async () => {
                        try {
                            const response = await fetch(
                                `${apiKey}/favourite/people/remove/${personID}`,
                                {
                                    method: "POST",
                                    headers: {
                                        "Content-Type": "application/json",
                                        Authorization: `Bearer ${token}`,
                                    },
                                },
                            );
                            if (!response.ok)
                                throw new Error(
                                    `Could not remove person from favourite: ${response.status}`,
                                );
                        } catch (e) {
                            console.error(e);
                        }
                    }}
                    enabledByDefault={isLoggedIn}
                />
            </div>
            {#if person.birthday !== null}
                <p class="text-[1em]">
                    Born {person.birthday}, {person.place_of_birth}
                </p>
            {/if}
            {#if person.deathday !== null}
                <p class="text-[1em]">Died {person.deathday}</p>
            {/if}
            {#if person.biography !== ""}
                <CollapsibleText
                    textContent={person.biography}
                    maxWords={100}
                    readMoreLabel="more"
                    readLessLabel="less"
                    additional="text-[1.3em] max-w-[800px]"
                />
            {/if}
        </div>
    </Showcase>
{/if}
