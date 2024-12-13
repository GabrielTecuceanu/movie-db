<script lang="ts">
    import {
        apiKey,
        redirectTo,
        imgBaseUrl,
        imgOriginal,
        fetchUsername,
        friendStatus,
    } from "$lib/utils";
    import Cookies from "js-cookie";
    import { onMount } from "svelte";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index";
    import { Separator } from "$lib/components/ui/separator";
    import { page } from "$app/stores";
    import Button from "$lib/components/ui/button/button.svelte";

    const username = $page.params.username;
    let loading = $state(true);
    let user = $state(null);
    let friends = $state(null);

    async function fetchProfile() {
        try {
            let response = await fetch(`${apiKey}/get_user/${username}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });
            if (!response.ok) {
                throw new Error(`Could not get profile: ${response.status}`);
            }

            let data = await response.json();

            data.movie_finished = await Promise.all(
                data.movie_finished.map(async (elem) => {
                    let response = await fetch(
                        `${apiKey}/movie/details/${elem.movie_id}`,
                    );
                    if (!response.ok) {
                        throw new Error(
                            `Could not get movie details: ${response.status}`,
                        );
                    }
                    const data = await response.json();
                    return {
                        ...elem,
                        data,
                        poster: `${imgBaseUrl}/${imgOriginal}${data.poster_path}`,
                    };
                }),
            );

            data.movie_watchlist = await Promise.all(
                data.movie_watchlist.map(async (elem) => {
                    let response = await fetch(
                        `${apiKey}/movie/details/${elem}`,
                    );
                    if (!response.ok) {
                        throw new Error(
                            `Could not get movie details: ${response.status}`,
                        );
                    }
                    const data = await response.json();
                    return {
                        ...elem,
                        data,
                        poster: `${imgBaseUrl}/${imgOriginal}${data.poster_path}`,
                    };
                }),
            );

            data.tv_finished = await Promise.all(
                data.tv_finished.map(async (elem) => {
                    let response = await fetch(
                        `${apiKey}/tv/details/${elem.show_id}`,
                    );
                    if (!response.ok) {
                        throw new Error(
                            `Could not get show details: ${response.status}`,
                        );
                    }
                    const data = await response.json();
                    return {
                        ...elem,
                        data,
                        poster: `${imgBaseUrl}/${imgOriginal}${data.poster_path}`,
                    };
                }),
            );

            data.tv_watchlist = await Promise.all(
                data.tv_watchlist.map(async (elem) => {
                    let response = await fetch(`${apiKey}/tv/details/${elem}`);
                    if (!response.ok) {
                        throw new Error(
                            `Could not get show details: ${response.status}`,
                        );
                    }
                    const data = await response.json();
                    return {
                        ...elem,
                        data,
                        poster: `${imgBaseUrl}/${imgOriginal}${data.poster_path}`,
                    };
                }),
            );
            data.feed = data.feed.reverse();

            let friendsResponse = await fetch(`${apiKey}/friends/get_friends`, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });
            if (!response.ok) {
                throw new Error(`Could not get friends: ${response.status}`);
            }
            const friendsData = await friendsResponse.json();
            console.log(friendsData);
            friends = friendsData;

            return data;
        } catch (e) {
            console.error(e);
        }
    }

    async function fetchFriendRequests() {
        try {
            let response = await fetch(
                `${apiKey}/friends/get_pending_requests`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                },
            );
            if (!response.ok) {
                throw new Error(
                    `Could not get pending requests: ${response.status}`,
                );
            }

            return await response.json();
        } catch (e) {
            console.error(e);
        }
    }

    let isLoggedIn = $state(false);
    let myUsername = $state(null);
    const token = Cookies.get("token");
    if (token) isLoggedIn = true;
    let isFriend: friendStatus = $state(friendStatus.STRANGER);

    let reqs = $state(null);

    // @ts-ignore
    onMount(async () => {
        if (!token) redirectTo("/");
        let profile = await fetchProfile();
        reqs = await fetchFriendRequests();
        user = profile;

        if (isLoggedIn) {
            myUsername = await fetchUsername(token);
            if (myUsername === username) {
                isFriend = friendStatus.ME;
            } else {
                try {
                    let response = await fetch(`${apiKey}/friends/is_friend`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                        },
                        body: JSON.stringify({
                            email: user.email,
                        }),
                    });

                    const data = await response.json();
                    if (data.status === true) isFriend = friendStatus.FRIEND;
                } catch (e) {
                    console.error(e);
                }
            }
        }

        loading = false;
        return () => {};
    });
</script>

{#if user !== null && !loading}
    <div class="min-h-screen mt-48">
        <h1 class="text-6xl text-white mb-16 ml-32">
            Username: {user.username}
        </h1>
        <div class="flex flex-col">
            <div class="mx-auto">
                {#each friends as friend}
                    <p>
                        {friend.sender} is friends with {friend.recipient}
                    </p>
                {/each}
                {#if isLoggedIn}
                    {#if isFriend === friendStatus.STRANGER}
                        <Button
                            class="bg-white text-rich_black hover:text-white"
                            on:click={async () => {
                                let response = await fetch(
                                    `${apiKey}/friends/request`,
                                    {
                                        method: "POST",
                                        headers: {
                                            "Content-Type": "application/json",
                                            Authorization: `Bearer ${token}`,
                                        },
                                        body: JSON.stringify({
                                            email: user.email,
                                        }),
                                    },
                                );
                                if (!response.ok) {
                                    console.error(
                                        "Could not send friend request",
                                    );
                                }
                            }}>Add friend</Button
                        >
                    {:else if isFriend === friendStatus.FRIEND}
                        <Button
                            class="bg-white text-rich_black hover:text-white"
                            on:click={async () => {
                                let response = await fetch(
                                    `${apiKey}/friends/remove`,
                                    {
                                        method: "POST",
                                        headers: {
                                            "Content-Type": "application/json",
                                            Authorization: `Bearer ${token}`,
                                        },
                                        body: JSON.stringify({
                                            email: user.email,
                                        }),
                                    },
                                );
                                if (!response.ok) {
                                    console.error("Could not remove friend");
                                }
                                isFriend = friendStatus.STRANGER;
                            }}>Remove friend</Button
                        >
                    {:else}
                        <div class="flex flex-row mb-8">
                            {#each reqs as req}
                                <div class="flex flex-col w-fit space-y-2">
                                    <Button
                                        class="bg-white text-rich_black hover:text-white"
                                        on:click={async () => {
                                            let response = await fetch(
                                                `${apiKey}/friends/respond`,
                                                {
                                                    method: "POST",
                                                    headers: {
                                                        "Content-Type":
                                                            "application/json",
                                                        Authorization: `Bearer ${token}`,
                                                    },
                                                    body: JSON.stringify({
                                                        email: req.sender,
                                                        response: "accept",
                                                    }),
                                                },
                                            );
                                            if (!response.ok) {
                                                console.error(
                                                    "Could not accept friend",
                                                );
                                            }
                                            reqs = reqs.filter(
                                                (r) => r.sender !== req.sender,
                                            );
                                        }}
                                    >
                                        Accept friend request from {req.sender}</Button
                                    >

                                    <Button
                                        class="bg-white text-rich_black hover:text-white"
                                        on:click={async () => {
                                            let response = await fetch(
                                                `${apiKey}/friends/respond`,
                                                {
                                                    method: "POST",
                                                    headers: {
                                                        "Content-Type":
                                                            "application/json",
                                                        Authorization: `Bearer ${token}`,
                                                    },
                                                    body: JSON.stringify({
                                                        email: req.sender,
                                                        response: "reject",
                                                    }),
                                                },
                                            );
                                            if (!response.ok) {
                                                console.error(
                                                    "Could not reject friend",
                                                );
                                            }
                                            reqs = reqs.filter(
                                                (r) => r.sender !== req.sender,
                                            );
                                        }}
                                    >
                                        Reject friend request from {req.sender}</Button
                                    >
                                </div>
                            {/each}
                        </div>
                        <div class="flex flex-col space-y-2">
                            {#each user.feed as item}
                                <p>{item}</p>
                                <Separator />
                            {/each}
                        </div>
                    {/if}
                {/if}
            </div>
            <div class="mx-auto">
                <div class="flex flex-row mt-8 space-x-4">
                    {#if user.movie_watchlist !== null && user.movie_watchlist.length != 0}
                        <ScrollArea class="h-fit rounded-md border w-[23vw]">
                            <div class="p-4">
                                <h4
                                    class="mb-4 text-sm font-medium leading-none"
                                >
                                    Movie Watchlist
                                </h4>
                                {#each user.movie_watchlist as movie}
                                    <Separator class="my-2" />
                                    <div class="flex flex-row space-x-4">
                                        <img
                                            src={movie.poster}
                                            alt={movie.data.name}
                                            class="h-48 w-fit"
                                        />

                                        <div class="flex flex-col">
                                            <a
                                                href="/movie/{movie.data.id}"
                                                class="text-4xl"
                                                >{movie.data.title}</a
                                            >
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        </ScrollArea>
                    {/if}
                    {#if user.movie_finished !== null && user.movie_finished.length != 0}
                        <ScrollArea class="h-fit rounded-md border w-[23vw]">
                            <div class="p-4">
                                <h4
                                    class="mb-4 text-sm font-medium leading-none"
                                >
                                    Finished movies
                                </h4>

                                {#each user.movie_finished as movie}
                                    <Separator class="my-2" />
                                    <div class="flex flex-row space-x-4">
                                        <img
                                            src={movie.poster}
                                            alt={movie.data.title}
                                            class="h-48 w-fit"
                                        />

                                        <div class="flex flex-col">
                                            <a
                                                href="/movie/{movie.movie_id}"
                                                class="text-4xl"
                                                >{movie.data.title}</a
                                            >
                                            <p>Rating: {movie.rating}</p>
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        </ScrollArea>
                    {/if}
                    {#if user.tv_watchlist !== null && user.tv_watchlist.length != 0}
                        <ScrollArea class="h-fit rounded-md border w-[23vw]">
                            <div class="p-4">
                                <h4
                                    class="mb-4 text-sm font-medium leading-none"
                                >
                                    Show Watchlist
                                </h4>
                                {#each user.tv_watchlist as show}
                                    <Separator class="my-2" />
                                    <div class="flex flex-row space-x-4">
                                        <img
                                            src={show.poster}
                                            alt={show.data.name}
                                            class="h-48 w-fit"
                                        />

                                        <div class="flex flex-col">
                                            <a
                                                href="/tv/{show.data.id}"
                                                class="text-4xl"
                                                >{show.data.name}</a
                                            >
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        </ScrollArea>
                    {/if}
                    {#if user.tv_finished !== null && user.tv_finished.length != 0}
                        <ScrollArea class="h-fit rounded-md border w-[23vw]">
                            <div class="p-4">
                                <h4
                                    class="mb-4 text-sm font-medium leading-none"
                                >
                                    Finished Shows
                                </h4>
                                {#each user.tv_finished as show}
                                    <Separator class="my-2" />
                                    <div class="flex flex-row space-x-4">
                                        <img
                                            src={show.poster}
                                            alt={show.data.name}
                                            class="h-48 w-fit"
                                        />

                                        <div
                                            class="flex flex-col text-ellipsis"
                                        >
                                            <a
                                                href="/tv/{show.show_id}"
                                                class="text-4xl"
                                                >{show.data.name}</a
                                            >
                                            <p>Rating: {show.rating}</p>
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        </ScrollArea>
                    {/if}
                </div>
            </div>
        </div>
    </div>
{/if}
