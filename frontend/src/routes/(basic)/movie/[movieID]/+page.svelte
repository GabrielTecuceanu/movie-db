<script lang="ts">
    import { onMount } from "svelte";
    import {
        apiKey,
        imgBaseUrl,
        imgOriginal,
        formatCurrency,
        mediaStatus,
    } from "$lib/utils";
    import { page } from "$app/stores";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import Separator from "$lib/components/ui/separator/separator.svelte";
    import CollapsibleText from "$lib/components/ui/collapsible-text/index";
    import { Showcase } from "$lib/components/ui/showcase/index";
    import { Stars } from "$lib/components/ui/star-rating/index";
    import { ClickableStar } from "$lib/components/ui/clickable-star/index";
    import { Button, buttonVariants } from "$lib/components/ui/button/index";
    import { Textarea } from "$lib/components/ui/textarea";
    import Cookies from "js-cookie";

    let isLoggedIn = $state(false);
    const token = Cookies.get("token");
    if (token) isLoggedIn = true;
    let initialUserData = $state({
        rating: 0,
        review: "",
    });
    let userData = $state({
        rating: 0,
        review: "",
    });

    const movieID = $page.params.movieID;
    let movie = $state(null);
    let images = $state(null);
    let recs = $state(null);

    async function fetchMovieDetails() {
        try {
            const response = await fetch(`${apiKey}/movie/details/${movieID}`);
            if (!response.ok) {
                throw new Error(
                    `Could not get movie details: ${response.status}`,
                );
            }

            const data = await response.json();
            let backdropUrl = `${imgBaseUrl}/${imgOriginal}${data.backdrop_path}`;
            let posterUrl = `${imgBaseUrl}/${imgOriginal}${data.poster_path}`;
            movie = {
                ...data,
                backdropUrl: backdropUrl,
                posterUrl: posterUrl,
                runtime: `${Math.floor(data.runtime / 60)}h ${data.runtime % 60}min`,
                budget: formatCurrency(data.budget),
                revenue: formatCurrency(data.revenue),
            };
        } catch (e) {
            console.error(e);
        }
    }

    async function fetchMovieMedia() {
        try {
            const response = await fetch(`${apiKey}/movie/${movieID}/images`);
            if (!response.ok) {
                throw new Error(
                    `Could not get movie images: ${response.status}`,
                );
            }

            const data = await response.json();
            images = data.backdrops.map((url) => {
                return {
                    img: `${imgBaseUrl}/${imgOriginal}${url.file_path}`,
                    alt: `Image of ${movie.title}`,
                    redirect: null,
                    tooltip: null,
                };
            });
        } catch (e) {
            console.error(e);
        }
    }

    async function fetchSimilar() {
        try {
            const response = await fetch(
                `${apiKey}/movie/${movieID}/recommendations`,
            );
            if (!response.ok) {
                throw new Error(
                    `Could not get movie recommednations: ${response.status}`,
                );
            }

            const data = await response.json();
            recs = data.results.map((rec) => {
                return {
                    ...rec,
                    img: `${imgBaseUrl}/${imgOriginal}${rec.poster_path}`,
                    tooltip: rec.title,
                    redirect: `/${rec.media_type}/${rec.id}`,
                };
            });
        } catch (e) {
            console.error(e);
        }
    }

    let status: mediaStatus = $state(mediaStatus.NONE);
    let ratingStars = $state(null);
    async function fetchStatus() {
        if (!isLoggedIn) return;
        try {
            let response = await fetch(`${apiKey}/watchlist/movie/${movieID}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });
            if (!response.ok) {
                throw new Error(
                    `Could not get movie watchlist status: ${response.status}`,
                );
            }
            let data = await response.json();
            if (data.success == true) {
                status = mediaStatus.WATCHLIST;
                return;
            }

            response = await fetch(`${apiKey}/finished/movie/${movieID}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });
            if (!response.ok) {
                throw new Error(
                    `Could not get movie finished status: ${response.status}`,
                );
            }
            data = await response.json();
            if (data.success == true) {
                status = mediaStatus.FINISHED;
                userData.rating = data.movie.rating;
                userData.review = data.movie.review;
                initialUserData.rating = data.movie.rating;
                initialUserData.review = data.movie.review;
                return;
            }
        } catch (e) {
            console.error(e);
        }
    }

    async function addToWatchlist() {
        try {
            let response = await fetch(
                `${apiKey}/watchlist/movie/add/${movieID}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                },
            );
            if (!response.ok) {
                throw new Error(
                    `Could not add movie to watchlist: ${response.status}`,
                );
            }
        } catch (e) {
            console.error(e);
            return;
        }
        status = mediaStatus.WATCHLIST;
    }

    async function removeFromWatchlist() {
        try {
            let response = await fetch(
                `${apiKey}/watchlist/movie/remove/${movieID}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                },
            );
            if (!response.ok) {
                throw new Error(
                    `Could not remove movie from watchlist: ${response.status}`,
                );
            }
        } catch (e) {
            console.error(e);
            return;
        }
        status = mediaStatus.NONE;
    }

    async function addToFinished() {
        try {
            let response = await fetch(
                `${apiKey}/finished/movie/add/${movieID}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                },
            );
            if (!response.ok) {
                throw new Error(
                    `Could not mark movie as finished: ${response.status}`,
                );
            }
        } catch (e) {
            console.error(e);
            return;
        }
        status = mediaStatus.FINISHED;
    }

    async function removeFromFinished() {
        try {
            let response = await fetch(
                `${apiKey}/finished/movie/remove/${movieID}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                },
            );
            if (!response.ok) {
                throw new Error(
                    `Could not mark movie as finished: ${response.status}`,
                );
            }
            initialUserData.review = "";
        } catch (e) {
            console.error(e);
            return;
        }
        status = mediaStatus.NONE;
        ratingStars.setValue(0);
    }

    let displayReview = $state(false);
    let loading = $state(true);
    // @ts-ignore
    onMount(async () => {
        await fetchMovieDetails();
        await fetchMovieMedia();
        await fetchSimilar();
        await fetchStatus();
        loading = false;

        return () => {};
    });
</script>

{#if movie !== null && loading == false}
    <Showcase
        backdropUrl={movie.backdropUrl}
        posterUrl={movie.posterUrl}
        posterAlt={movie.title}
        carousel1={images}
        carousel1Basis={3}
        carousel1Title={"Media"}
        carousel2={recs}
        carousel2Title={"Similar"}
        carousel2Basis={5}
    >
        <div class="flex flex-col grow-1">
            <div class="flex flex-row space-x-2 items-end mb-2">
                <h1 class="text-4xl" style="font-weight: 700">
                    {movie.title}
                </h1>
                <p class="text-muted-foreground">
                    {#if movie.status === "Released"}
                        released {movie.release_date}
                    {:else}
                        in {movie.status}
                    {/if}
                </p>
            </div>
            <p class="text-xl mb-1">{movie.tagline}</p>
            {#if isLoggedIn}
                <div class="mb-2">
                    <Stars
                        bind:this={ratingStars}
                        startingValue={userData.rating}
                        onSubmit={async (score: number) => {
                            if (status !== mediaStatus.FINISHED)
                                addToFinished();
                            try {
                                const response = await fetch(
                                    `${apiKey}/finished/movie/${movieID}/rate/${score}`,
                                    {
                                        method: "POST",
                                        headers: {
                                            "Content-Type": "application/json",
                                            Authorization: `Bearer ${token}`,
                                        },
                                    },
                                );
                                if (!response.ok) {
                                    const errorData = await response.json();
                                    throw new Error(
                                        `Could not rate movie: ${response.status} --- ${errorData}`,
                                    );
                                }
                                userData.rating = score;
                                const data = await response.json();
                            } catch (e) {
                                userData.rating = 0;
                                console.error(e);
                                throw e;
                            }
                        }}
                    />
                </div>
            {/if}
            <div class="flex flex-row mb-2">
                {#each movie.genres as genre}
                    <Badge class="text-white mr-1" variant="outline"
                        >{genre.name}
                    </Badge>
                {/each}
            </div>
            <div class="flex flex-row space-x-1 mb-3">
                <p>
                    Rating: {Math.round((movie.vote_average / 2) * 100) / 100}
                </p>
                <svg
                    class="w-6 h-6 text-white"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    fill="none"
                    viewBox="0 0 24 24"
                >
                    <path
                        stroke="currentColor"
                        stroke-width="2"
                        d="M11.083 5.104c.35-.8 1.485-.8 1.834 0l1.752 4.022a1 1 0 0 0 .84.597l4.463.342c.9.069 1.255 1.2.556 1.771l-3.33 2.723a1 1 0 0 0-.337 1.016l1.03 4.119c.214.858-.71 1.552-1.474 1.106l-3.913-2.281a1 1 0 0 0-1.008 0L7.583 20.8c-.764.446-1.688-.248-1.474-1.106l1.03-4.119A1 1 0 0 0 6.8 14.56l-3.33-2.723c-.698-.571-.342-1.702.557-1.771l4.462-.342a1 1 0 0 0 .84-.597l1.753-4.022Z"
                    />
                </svg>
                <p>from {movie.vote_count} votes</p>
            </div>

            <Separator class="opacity-50 mb-3"></Separator>
            <CollapsibleText
                textContent={movie.overview}
                maxWords={100}
                readMoreLabel="more"
                readLessLabel="less"
                additional="text-xl"
            />
            <div
                class="mt-auto"
                style="margin-bottom:{isLoggedIn ? 'auto' : 'none'}"
            >
                <p class="text-lg">Budget: {movie.budget}</p>
                <p class="text-lg">Revenue: {movie.revenue}</p>
            </div>
            {#if isLoggedIn}
                {#if !displayReview}
                    <div class="w-fit mt-auto flex flex-row space-x-4">
                        {#if status === mediaStatus.NONE}
                            <ClickableStar
                                additional="ADD TO WATCHLIST"
                                enable={() => {
                                    addToWatchlist();
                                }}
                                enabledByDefault={true}
                                filledByDefault={false}
                                confetti={false}
                                rounded={false}
                                changeOnClick={false}
                            />
                        {:else if status === mediaStatus.WATCHLIST}
                            <ClickableStar
                                additional="REMOVE FROM WATCHLIST"
                                enable={() => {
                                    removeFromWatchlist();
                                }}
                                enabledByDefault={true}
                                filledByDefault={false}
                                confetti={false}
                                rounded={false}
                                changeOnClick={false}
                            />
                            <ClickableStar
                                additional="MARK AS FINISHED"
                                enable={() => {
                                    addToFinished();
                                }}
                                enabledByDefault={true}
                                filledByDefault={false}
                                confetti={false}
                                rounded={false}
                                changeOnClick={false}
                            />
                        {:else}
                            <ClickableStar
                                additional="UNMARK AS FINISHED"
                                enable={() => {
                                    removeFromFinished();
                                }}
                                enabledByDefault={true}
                                filledByDefault={false}
                                confetti={false}
                                rounded={false}
                                changeOnClick={false}
                            />

                            <ClickableStar
                                additional="REVIEW"
                                enable={() => {
                                    displayReview = !displayReview;
                                    userData.review = initialUserData.review;
                                }}
                                enabledByDefault={true}
                                filledByDefault={false}
                                confetti={false}
                                rounded={false}
                                changeOnClick={false}
                            />
                        {/if}
                    </div>
                {:else}
                    <div class="gap-2 space-y-2">
                        <Textarea
                            placeholder="Write your review here..."
                            bind:value={userData.review}
                            style="font-family: 'Open Sans';"
                            class="min-h-64"
                        ></Textarea>
                        <Button
                            variant="outline"
                            type="submit"
                            style="font-family: 'Open Sans';"
                            class="text-rich_black"
                            on:click={async () => {
                                try {
                                    const response = await fetch(
                                        `${apiKey}/finished/movie/${movieID}/review`,
                                        {
                                            method: "POST",
                                            headers: {
                                                "Content-Type":
                                                    "application/json",
                                                Authorization: `Bearer ${token}`,
                                            },
                                            body: JSON.stringify({
                                                review: userData.review,
                                            }),
                                        },
                                    );
                                    if (!response.ok) {
                                        const errorData = await response.json();
                                        throw new Error(
                                            `Could not review movie: ${response.status}, ${errorData}`,
                                        );
                                    }
                                    initialUserData.review = userData.review;
                                    displayReview = false;
                                } catch (e) {
                                    userData.review = initialUserData.review;
                                    console.error(e);
                                }
                            }}
                            >Finish writing
                        </Button>
                        <Button
                            variant="outline"
                            type="submit"
                            style="font-family: 'Open Sans';"
                            class="text-rich_black"
                            on:click={() => {
                                displayReview = false;
                                userData.review = initialUserData.review;
                            }}>Close</Button
                        >
                    </div>
                {/if}
            {/if}
        </div>
    </Showcase>
{/if}
